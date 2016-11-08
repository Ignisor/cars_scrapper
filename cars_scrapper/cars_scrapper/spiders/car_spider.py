import scrapy
import logging
from scrapy.spider import BaseSpider
from cars_scrapper.items import BrandItem, CarModelItem, CarTypeItem,\
    CarItem, SpecificationItem, SpecificationCategoryItem
from cars_app.models import Brand, CarModel, CarType, Car, Specification, SpecificationCategory
from annoying.functions import get_object_or_None


class ExampleSpider(BaseSpider):
    name = "car_spider"
    allowed_domains = ["www.cars-data.com"]
    start_urls = ['http://www.cars-data.com/en/car-brands-cars-logos.html']

    def parse(self, response):

        # get all brands urls and names
        brands_urls = response.css('div.models > div.col-2.center > a::attr(href)').extract()
        brands_names = response.css('div.models > div.col-2.center > a::attr(title)').extract()

        # scrap only 4 first brands, ignore
        for i in [0, 2, 3]:
            # parse models of the brand from urls
            request = scrapy.Request(brands_urls[i], callback = self.parse_models, dont_filter = True)

            # if brand exist - don't create it
            brand_django_item = get_object_or_None(Brand, name = brands_names[i])
            if brand_django_item is None:
                brand_item = BrandItem(name=brands_names[i])
                request.meta['brand_item'] = brand_item.save()
            else:
                request.meta['brand_item'] = brand_django_item

            yield request

    def parse_models(self, response):

        # try get all models urls an names
        try:
            models_urls = response.css('section.models > div.col-4 > a::attr(href)').extract()
            models_names = response.css('section.models > div.col-4 > a::attr(title)').extract()
        except AttributeError:
            # resend request if bad response
            logging.error("AttributeError: requesting same url again")
            request = scrapy.Request(response.url, callback=self.parse_models, dont_filter = True)
            request.meta['brand_item'] = response.meta['brand_item']

            yield request

        else:
            for i in range(0, len(models_urls)):
                # parse specifications
                request = scrapy.Request(models_urls[i], callback = self.parse_types, dont_filter = True)

                # if model exist - don't create it
                model_django_item = get_object_or_None(CarModel, name=models_names[i])
                if model_django_item is None:
                    model_item = CarModelItem(name=models_names[i], brand = response.meta['brand_item'])
                    request.meta['model_item'] = model_item.save()
                else:
                    request.meta['model_item'] = model_django_item

                yield request

    def parse_types(self, response):

        # try get all specifications urls and names
        try:
            types_urls = response.css('section.models > div.col-4 > a::attr(href)').extract()
            types_names = response.css('section.models > div.col-4 > a::attr(title)').extract()
        except AttributeError:
            # resend request if bad response
            logging.error("AttributeError: requesting same url again")
            request = scrapy.Request(response.url, callback=self.parse_types, dont_filter = True)
            request.meta['model_item'] = response.meta['model_item']

            yield request

        else:
            for i in range(0, len(types_urls)):
                # parse car types
                request = scrapy.Request(types_urls[i], callback = self.parse_cars, dont_filter = True)

                # if type exist - don't create it
                type_django_item = get_object_or_None(CarType, name=types_names[i])
                if type_django_item is None:
                    type_item = CarTypeItem(name=types_names[i], car_model=response.meta['model_item'])
                    request.meta['type_item'] = type_item.save()
                else:
                    request.meta['type_item'] = type_django_item

                yield request

    def parse_cars(self, response):

        # try to get all cars urls and names
        try:
            cars_urls = response.css('section.types > div.col-8 > div.row > div.col-6 > h2 > a::attr(href)').extract()
            cars_names = response.css('section.types > div.col-8 > div.row > div.col-6 > h2 > a::attr(title)').extract()
        except AttributeError:
            # resend request if bad response
            logging.error("AttributeError: requesting same url again")
            request = scrapy.Request(response.url, callback=self.parse_cars, dont_filter = True)
            request.meta['type_item'] = response.meta['type_item']

            yield request

        else:
            for i in range(0, len(cars_urls)):

                # if car exist - don't create it
                car_django_item = get_object_or_None(Car, url=cars_urls[i])
                if car_django_item is None:
                    # parse car
                    request = scrapy.Request(cars_urls[i], callback=self.parse_car, dont_filter = True)
                    request.meta['type_item'] = response.meta['type_item']
                    request.meta['car_name'] = cars_names[i]
                    request.meta['car_url'] = cars_urls[i]

                    yield request

                else:
                    logging.info("{name}({url}) skipped, becaue already exist"\
                                 .format(name = cars_names[i], url = cars_urls[i]))

                    yield None

    def parse_car(self, response):

        # try to get data blocks (categories) (e.g. General Specifications, Drive, Engine, ...)
        try:
            data_blocks = response.css('div.col-9 > div > div.row.box')
        except AttributeError:
            # resend request if bad response
            logging.error("AttributeError: requesting same url again")
            request = scrapy.Request(response.url, callback=self.parse_car, dont_filter = True)
            request.meta['type_item'] = response.meta['type_item']
            request.meta['car_name'] = response.meta['car_name']
            request.meta['car_url'] = response.meta['car_url']

            return request

        else:
            # check is there a car with the same name, and add number in the end if true
            car_name = response.meta['car_name']
            obj = get_object_or_None(Car, name=car_name)
            i = 0
            while obj is not None:
                i += 1
                car_name = response.meta['car_name'] + '({})'.format(i)
                obj = get_object_or_None(Car, name=car_name)
            # end of chek

            car_item = CarItem(name = car_name, url = response.meta['car_url'], car_type = response.meta['type_item'])
            car_django_item = car_item.save()

            # get key-value data from data blocks
            for data_block_num in range(0, len(data_blocks)):
                # get category name of data block
                category_name = data_blocks[data_block_num].css('h2::text').extract()
                category_item = SpecificationCategoryItem(name = category_name[0], car = car_django_item)
                category_django_item = category_item.save()

                # get all data from data block
                data = data_blocks[data_block_num].css('div.col-6::text').extract()

                # convert data to dictionary, remove ':' from key name and encoding everything to ASCII
                for data_num in range(0, len(data), 2):
                    key = data[data_num].encode('ascii', 'ignore')
                    key = key.translate(None, ':')
                    key = key.lstrip().rstrip()
                    value = data[data_num + 1].encode('ascii', 'ignore')
                    value.lstrip().rstrip()

                    spec = Specification(key = key,
                                         value = value,
                                         category = category_django_item,
                                         car = car_django_item)

                    spec.save()

            return car_item