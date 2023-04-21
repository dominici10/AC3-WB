import scrapy
import csv

class ArduinousinainfoSpiderSpider(scrapy.Spider):
    name = "arduinoUsinaInfo_spider"

    def __init__(self, *args, **kwargs):
        super(ArduinousinainfoSpiderSpider, self).__init__(*args, **kwargs)
        self.items = []

    def start_requests(self):
        url = 'https://www.usinainfo.com.br/arduino-74'
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        for product in response.css('#product_list li'):
            title = product.css('.name_product a::text').getall()
            price = product.css('.price::text').getall()
            #if not price:
                #price = 'valor indisponivel'

            item = {
                'id': product,
                'title': title,
                'price': price,
            }
            self.items.append(item)

        next_page = response.xpath('//*[@id="pagination_next_bottom"]/a')
        if next_page:
            yield response.follow(next_page[0], self.parse)

    def closed(self, reason):
        # Exporta o resultado para um arquivo CSV
        filename = 'bases_originais/dados.csv'
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Título', 'Preço'])
            for item in self.items:
                writer.writerow([item['title'], item['price']])

    ##Para rodar e criar um output.json dos resultados da raspagem
    ##scrapy crawl arduinoUsinaInfo_spider -o output.json
    ##Para rodar e criar um output.csv dos resultados da raspagem
    ##scrapy crawl arduinoUsinaInfo_spider -o output.csv
    ##Para rodar e criar um output.xml dos resultados da raspagem
    ##scrapy crawl arduinoUsinaInfo_spider -o output.xml