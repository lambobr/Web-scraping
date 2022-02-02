import scrapy

class WhiskeySpider(scrapy.Spider):
    name = 'whiskeyv2'
    allowed_domains = ['whiskyshop.com']
    start_urls = ['https://www.whiskyshop.com/catalogsearch/result/index/?item_availability=In+Stock&q=scotch+whisky']

    def parse(self, response):

        products = response.css('div.product-item-info')

        for product in products:
            try:
                yield {     #yield is the return equivalent
                    'product_name' : product.css('a.product-item-link::text').get(),
                    'product_price' : product.css('span.price::text').get(),
                    'product_link' : product.css('a.product-item-link').attrib['href']
                }
            except:
                continue

#run in terminal:
#scrapy crawl whiskeyv2 -o whiskeys.csv
#this will auto save result in csv
#note: py file should be saved in scrapy folder


