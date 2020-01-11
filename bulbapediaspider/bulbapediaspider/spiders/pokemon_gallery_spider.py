from bulbapediaspider.items import PokemonImage
import datetime
import os
import scrapy


class PokemonGallerySpider(scrapy.Spider):
    name = "bulbapedia-gallery-sider"
    data_dir = "/home/aj/PokeRap/Pokemon"
    pokemon_list = os.listdir(data_dir)
    start_urls = []
    for pokemon in pokemon_list:
        if pokemon == 'data':
            continue
        start_urls.append("https://archives.bulbagarden.net/wiki/Category:" + pokemon)
    

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    def parse(self, response):
        name = response.xpath('//h1[@id="firstHeading"]/text()').get().split(':')[1]
        page_links_text = response.xpath('//div[@id="mw-category-media"]/text()').getall()
        next_page_url = 'https://archives.bulbagarden.net'
        image_links = response.xpath('//div[@id="mw-category-media"]//a[contains(@class, "image")]/@href').getall()
        image_links = ['https://archives.bulbagarden.net' + img_link for img_link in image_links]
        for link in image_links:
            yield scrapy.Request(link, self.parse_image_file, dont_filter=True, meta={'pokemon_name':name})
        if not ') (next page)' in page_links_text:
            gallery_ending = response.xpath('//div[@id="mw-category-media"]/a[contains(text(), "next page")]/@href').get()
            next_page_url = next_page_url + gallery_ending
            yield scrapy.Request(next_page_url, self.parse)
        else:
            print("Completed pokemon: " + str(name))

    def parse_image_file(self, response):
        name = response.meta['pokemon_name']
        image_link = response.xpath('//div[@id="file"]/a/@href').getall()
        image_link = [img_link.replace("//archives.", "https://archives.") for img_link in image_link]
        yield PokemonImage(pokemon_name=name, image_urls=image_link)