from scrapy.exceptions import CloseSpider
import re
from datetime import datetime
import scrapy
import pycountry_convert as pc


class PostsSpider(scrapy.Spider):

    page_number = 0
    name = 'posts'

    global artist
    artist = input(f'Artist Name:')
    start_urls = [
        f'https://ra.co/dj/{artist}/past-events?'
    ]

    def parse(self, response):

        if len(response.css('li.Column-sc-18hsrnn-0.inVJeD')) == 0:
            raise CloseSpider('No more events')

        for link in response.css('li.Column-sc-18hsrnn-0.inVJeD div h3 a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_act)

        next_page = f'https://ra.co/dj/{artist}/past-events?page={str(PostsSpider.page_number)}'

        PostsSpider.page_number += 1
        print(PostsSpider.page_number)
        yield response.follow(next_page, callback=self.parse)


    def parse_act(self, response):
        date = response.xpath('//*[@id="__next"]/div[2]/header/div/div[2]//div/ul/li[2]/div/div[2]/a/span/text()').get()
        event = response.xpath('//*[@id="__next"]/div[2]/header/div//div/div/div[2]/h1/span/text()').get()
        promotors = response.xpath('//*[@id="__next"]/div[2]/header/div/div[2]/div[2]/div/ul/li[3]/div/div[2]/a/span/text()').getall()
        location = response.xpath('//*[@id="__next"]/div[2]/header/div//div[1]/div/div/div[1]/nav/ul/li[1]/div/a/span/text()').get()
        country = response.xpath('//*[@id="__next"]/div[2]/header/div//div[1]/div/div/div[1]/nav/ul/li[1]/div/a').attrib['href']
        venue = response.xpath('//*[@id="__next"]/div[2]/header/div/div[2]//div/ul/li[1]/div//span/text()')[1].get()
        acts = response.xpath('//*[@id="__next"]/div[2]/section[1]/div/section[1]/div/div/div[2]/ul/li[1]/div/span/a/span/text()').getall()

        date = re.sub(r'^.*?, ', '', date)

        promotors = ', '.join(promotors)

        if len(date) == 4:
            date = f'31-12-{date}'

        elif len(date) >= 15:
            date = date[5:]

        elif date[-4: -2] == '20':
            date = datetime.strptime(date, '%b %d, %Y').strftime('%d-%m-%Y')
        else:
            date = datetime.strptime(date, '%d %b').strftime('%d-%m') + '-2023'

        acts = ', '.join(acts)

        country_alpha2 = country.split('/')[-2].upper()
        try:
            country = pc.country_alpha2_to_country_name(country_alpha2)
        except:
            country = country_alpha2

        # try:
        region = pc.convert_continent_code_to_continent_name(pc.country_alpha2_to_continent_code(country_alpha2))
        # except:
        #     region = 'unrecognized'

        item = {
            'date': date,
            'Event': event,
            'promotors': promotors,
            'Location': location,
            'Country': country,
            'region': region,
            'Venue': venue,
            'Acts': acts
        }

        yield item