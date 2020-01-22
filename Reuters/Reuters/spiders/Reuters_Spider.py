from scrapy import Spider
from Reuters.items import ReutersItem

class ReutersSpider(Spider):
    name = 'reuters_spider'
    
    n_pages = 100
    allowed_domains = ["https://www.reuters.com/"]
    start_urls = ['https://www.reuters.com/news/archive/businessNews?view=page&page={}&pageSize=10'.format(i) for i in range(1,n_pages+1)]
    
    def parse(self, response):
        titles_xpath = '//article[@class="story "]//div[@class="story-content"]//h3[@class="story-title"]/text()'
        titles = [response.xpath(titles_xpath).getall()[i] for i in range(10)]
        titles = list(map(lambda x: x.strip('\n\t'), titles))
        
        summaries_xpath = '//article[@class="story "]//div[@class="story-content"]//p/text()'
        summaries = response.xpath(summaries_xpath).getall()
        
        # There should be 10 titles and 10 summaries per page
        assert len(titles) == len(summaries)
        n_stories = len(titles)
        
        for i in range(n_stories):
            item = ReutersItem()
            item['title'] = titles[i]
            item['description'] = summaries[i]
            
            #print('\n')
            #print('#'*50)
            #print('Title:',titles[i])
            #print('Body:',summaries[i])
            #print('\n')
            
            yield item
        