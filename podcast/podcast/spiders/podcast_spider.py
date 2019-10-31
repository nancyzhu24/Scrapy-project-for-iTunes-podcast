import scrapy
import json
from podcast.items import PodcastItem

categories=[1301,1303, 1304, 1305, 1307, 1309, 1310, 1311, 1314, 1315,1316, 1318, 1321, 1323, 1324, 1325]
start_urls=['https://itunes.apple.com/us/rss/toppodcasts/limit=200/genre=' + str(category) + '/explicit=true/json' for category in categories]


class ImgtSpider(scrapy.Spider):
    name = "podcast_spider"
    
    #step 1 get json from RSS feed
    def start_requests(self):
       
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_podcast)
    
    #step 2 extract podcast title, artist,category,release_date and podcast_url       
    def parse_podcast(self, response):
        data=json.loads(response.text)
        data=data['feed']['entry']
        
        podcast_urls=[data[i]['link']['attributes']['href'] for i in range(len(data)) ]
       
        for i in range(len(podcast_urls)):
            
            
            title=data[i]['im:name']['label'] 
            content=data[i]['summary']['label']
            podcast_url=data[i]['link']['attributes']['href'] 
            artist=data[i]['im:artist']['label'] 
            category=data[i]['category']['attributes']['term'] 
            release_date=data[i]['im:releaseDate']['label'] 
            yield scrapy.Request(url=podcast_url,callback=self.parse_rating,
                             meta={"title":title,
                                   "artist":artist,
                                   "summary":content,
                                   "category":category,
                                   "release":release_date,
                                   "url":podcast_url})
    
    #step 3 extract podcast rating from podcast_url
    def parse_rating(self, response):
        
        item = PodcastItem()
        rating = response.css('figcaption.we-rating-count.star-rating__count::text').extract_first()
        
        item['title']=response.meta["title"]
        item['artist']=response.meta["artist"]
        item['summary']=response.meta["summary"]
        item['category']=response.meta["category"]
        item['release']=response.meta["release"]
        item['rating']=rating
        item['url']=response.meta["url"]
        
            
        yield item
