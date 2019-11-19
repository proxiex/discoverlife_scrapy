import scrapy
from discoverlife.items import DiscoverlifeItem

class DiscoverlifeSpider(scrapy.Spider):
    name = "discoverlife2"
    start_urls = ["https://www.discoverlife.org/moth/data/table2_33.9_-83.3.html"]

    def parse(self, response):
        # get photo num summary from tables
        photo_num  = response.xpath('//table[@border="1"]/tr[@bgcolor]/td[@bgcolor and @align="right"]/text()').extract()
        # fetch links to each species
        link = response.xpath('//table[@border="1"]/tr[@bgcolor]/td[1]/a/@href').extract()
       
        for i, num in enumerate(photo_num):
            num = int(num.split('\xa0')[0].replace(',', ''))
            # check if total is less than 100, else collect and follow link to species list
            if num > 99:
                moth_name = link[i].split('=')[1] # extract species name from link
                details_link = f'https://www.discoverlife.org/mp/20p?&res=640&selected=1&name={moth_name}&see=name&xml=Moth;'
                yield response.follow(details_link, callback=self.get_links)
    
    def get_links(self, response):
        # get links to species details page and follow
        for url in response.xpath('//td[@valign="top"]/a[2]/@href').extract():
            yield response.follow('https://www.discoverlife.org'+url, callback=self.paser_details)


    def paser_details(self, response):
        try:
            item = DiscoverlifeItem()
            xpath_ = '//table/tr[td/b="{}"]/td/following-sibling::td[1]/text()'.format

            item['image_urls'] = ['https://www.discoverlife.org' + response.xpath('//div[@align="center"]/a[1]/img/@src').extract()[0]]
            item['common_name'] = response.xpath(xpath_('title')).extract()[1].split(',')[1].strip()
            item['latitude'] = response.xpath(xpath_('latitude')).extract()[0]
            item['longitude'] = response.xpath(xpath_('longitude')).extract()[0]
            item['date'] = response.xpath(xpath_('date1 yyyymmdd')).extract()[0]

            bio = response.xpath('//table/tr/td/a/text()').extract()
            item['biological_name'] = bio[0] if len(bio) > 1 else None

            item['url'] = response.url

            yield item
        except Exception as e:
            print('An Error occured :: ', e)


  