from scrapy import Spider
from Reuters.items import ReutersItem

class ReutersSpider(Spider):
    name = 'reuters_spider'
    allowed_domains = ["https://www.reuters.com/"]
    start_urls = ["https://www.reuters.com/news/archive/businessNews?view=page&page=2&pageSize=10", "https://www.reuters.com/news/archive/businessNews?view=page&page=3&pageSize=10"]
    # When the basic code, convert it it something fancier, like this:
    # start_urls = ['https://www.the-numbers.com/movie/budgets/all/' + str(100*i+1) for i in range(56)]
    
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
            
            print('\n')
            print('#'*50)
            print('Title:',titles[i])
            print('Body:',summaries[i])
            print('\n')
            
            yield item
        