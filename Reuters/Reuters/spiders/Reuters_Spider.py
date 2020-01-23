
"""
# (1) Extend the original file to pull up 3000+ pages (original code supported 2 pages)

# Next step:
# Write the CSV file into Pandas dataframe and start manipulating it
# Count all of the words and their frequencies in a giant dictionary
# Classify them in types (economics, markets, company-specific, etc)
# (Can I also write something about sentiment?)
# (Do some NLP magic with them)

########################################################################

# Useful NLP articles to read:
https://towardsdatascience.com/using-word2vec-to-analyze-news-headlines-and-predict-article-success-cdeda5f14751
https://www.learndatasci.com/tutorials/sentiment-analysis-reddit-headlines-pythons-nltk/
https://blog.quiltdata.com/repeatable-nlp-of-news-headlines-using-apache-airflow-newspaper3k-quilt-t4-vega-a0447af57032
https://www.tutorialspoint.com/create-word-cloud-using-python
https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk
https://www.dataquest.io/blog/tutorial-text-analysis-python-test-hypothesis/


########################################################################


# Extra work: All of this work was for just the business news section
# You can also extend it to the market news section (if the xpath structure is similar)
# Link here: https://www.reuters.com/news/archive/marketNews
# You would essentially be repeating the same project twice (once for business news
# and once again for market news)


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
    n_pages = 100
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