
"""
Don't forget - you need to make a powerpoint presentation (10 min)

Using k-means unsupervised learning: other considerations
    (2) How to choose the value k?
    (3) Don't we need to randomly initialize the k centers, and repeatedly pick random starting points?

Questions to ask: How can we automate something that humans do on a daily basis, for a company?
    This is how you add value and increase revenues for a corporation (and get hired as a data scientist)

Discussion for further uses:
    - To do meaningful NLP analysis, I need to split, train, test, etc:
        https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk
        https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk
    - Using sentiment in financial news articles to automate trading strategies
    - Using sentiment in customer emails to automate customer service process
        (does this email from a customer require a human representative to intervene?)
    - Assess if a news article is fake or not.  Requires a training set of real and fake articles
        and training a supervised machine learning model on them
    - Assess whether or not a news source if politically biased or not, and to what extent
    - Which industries are using NLP?  What projects / business applications are associated with NLP?

Extra work: All of this work was for just the business news section
    You can also extend it to the market news section (if the xpath structure is similar)
    Link here: https://www.reuters.com/news/archive/marketNews

"""

# cd C:\\MAIN\\NYCDSA\\Web_Scraping_Project\\Reuters
# scrapy crawl reuters_spider

from Reuters.items import ReutersItem
from scrapy import Spider, Request
from datetime import datetime
from ftfy import fix_text

class ReutersSpider(Spider):
    name = 'reuters_spider'
    
    # Each start_url is like this: https://www.reuters.com/news/archive/businessNews?view=page&page=2&pageSize=10
    # and each contains a list of 10 archived article URLs
    # If n_pages = 20, we iterate up to https://www.reuters.com/news/archive/businessNews?view=page&page=20&pageSize=10
    # and we can grab information on 20x10 = 200 archived article URLs
    n_pages = 1000
    start_urls = ['https://www.reuters.com/news/archive/businessNews?view=page&page={}&pageSize=10'.format(i) for i in range(1,n_pages+1)]
    
    # Using the archive page xpaths for the 200 archived article URLs, we can open the original articles fully
    def parse(self, response):
        
        # A list of 10 full article URLs like this: https://www.reuters.com/article/us-usa-economy/u-s-weekly-jobless-claims-rise-modestly-labor-market-solid-idUSKBN1ZM1YW
        domain_prefix = 'https://www.reuters.com'
        domain_suffixes = response.xpath('//article[@class="story "]//div[@class="story-content"]/a/@href').extract()
        full_article_URLs = [domain_prefix + i for i in domain_suffixes]
        
        # Make a scrapy request to each of these full article URLs
        for url in full_article_URLs:
            yield Request(url=url, callback=self.parse_full_article)
    
    # Now we are on a page like this: https://www.reuters.com/article/us-usa-economy/u-s-weekly-jobless-claims-rise-modestly-labor-market-solid-idUSKBN1ZM1YW
    # Using the xpaths, grab this article's timestamp, title, and body
    def parse_full_article(self, response):
        
        # Timestamp is a Python datetime object
        timestamp_string = response.xpath('//div[@class="ArticleHeader_date"]/text()').getall()[0]
        timestamp = convert_timestamp_to_datetime(timestamp_string)
        
        # Title is a string such as: "U.S. weekly jobless claims rise modestly; labor market solid"
        title = response.xpath('//h1[@class="ArticleHeader_headline"]/text()').getall()[0]
        
        # Body is a list of strings, where each element is a paragraph of the article
        # So if an article has 7 paragraphs, body will return a list of 7 strings
        # fix_text resolves issues with parsing curly brackets or other non-standard characters
        body = response.xpath('//div[@class="StandardArticleBody_body"]/p/text()').getall()
        body = list(map(lambda x: fix_text(x), body))
        
        # Classification is a string such as: "Business News"
        classification = response.xpath('//div[@class="ArticleHeader_channel"]/a/text()').getall()[0]
        
        # Construct an item using these 4 fields and yield it
        item = ReutersItem()
        item['timestamp'] = timestamp
        item['title'] = title
        item['body'] = body
        item['classification'] = classification
        yield item
     
# Converts "January 23, 2020 /  1:47 PM / Updated an hour ago" to datetime.datetime(2020, 1, 23, 13, 47)
def convert_timestamp_to_datetime(timestamp_string):
    timestamp_list = timestamp_string.split("/")
    timestamp_list = list(map(lambda x: x.strip(), timestamp_list))
    article_timestamp = datetime.strptime(timestamp_list[0] + " " + timestamp_list[1], '%B %d, %Y %I:%M %p')
    print("Type of timestamp:",type(article_timestamp))
    return article_timestamp        