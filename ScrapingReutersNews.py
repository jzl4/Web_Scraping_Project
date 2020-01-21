scrapy shell "https://www.reuters.com/news/archive/businessNews"

######################################################################

# Titles of the stories
titles = [response.xpath('//article[@class="story "]//div[@class="story-content"]//h3[@class="story-title"]/text()').getall()[i] for i in range(10)]
# This returns 10 titles
titles = list(map(lambda x: x.strip('\n\t'), titles))
[print(x) for x in titles]
# Output:
#   Tesla says no unintended acceleration in its vehicles
#   Huawei CFO Meng's lawyer says 'double criminality' at center of U.S. extradition case

######################################################################

# 1-2 sentence summaries of the news stories
# Example:
#   "Tesla Inc said on Monday there is no unintended acceleration in its vehicles, 
#   responding to a petition to the National Highway Traffic Safety Administration to recall
#   500,000 of the electric company's cars over the alleged safety breach."
summaries = response.xpath('//article[@class="story "]//div[@class="story-content"]//p/text()').getall()
for i in range(len(summaries)):
    print(i,':',summaries[i],'\n')

######################################################################

# Time stamps of the news articles
from datetime import date
timestamps = response.xpath('//time[@class="article-time"]/span[@class="timestamp"]/text()').getall()
timestamps = list(map(lambda x: x.replace(' EST',''), timestamps))
# This turns a list such as:
#   6:60pm
#   5:28pm

######################################################################

# (1) Extend the original file to pull up 3000+ pages (original code supported 2 pages)
# (2) Learn how to handle broken links (If we try to pull page 4,000 and it doesn't, how to handle?)
# (2) Learn how to handle problems such as 10 article titles but 9 article bodies?
# (3) You forgot the first page (page 0).  Your stuff starts from page 2, page 3, onwards.
# (3) Add back the first page

# Next step:
# Write the CSV file into Pandas dataframe and start manipulating it
# Count all of the words and their frequencies in a giant dictionary
# Classify them in types (economics, markets, company-specific, etc)
# (Can I also write something about sentiment?)
# (Do some NLP magic with them)

########################################################################

# Extra work!!!!!!!!!  If time permits!

# Solution 1: If you don't have time, just map all of the time stamps from today to simply today
#   Ex: Map 8:31 AM to simply Jan 20th 2020
# And grab the date for prior days (yesterday and earlier)
# Then all of the time stamp data will be EOD / daily frequency, i.e. - Jan 20th, Jan 19th, etc.
# instead of having it on a minute-basis, i.e. - Jan 20th 8 PM, Jan 19th 7:30 PM, etc.
today = date.today()
time1 = "03:17pm"
date_string = str(today) + " " + time1
my_format = '%Y-%m-%d %H:%M%p'
my_date = datetime.strptime(date_string, my_format)

# Solution 2: If you have more time, if you want something more elegant
# you can move up the links of all article summaries from yesteday and earlier
# Go to the actual article's URL, and scrape that as well for the time
# Ex: click the article about Boeing from Jan 3rd, open it up, and see on that article's page
# that it was specifically Jan 3rd 5:07 AM, etc.

# Extra work: All of this work was for just the business news section
# You can also extend it to the market news section (if the xpath structure is similar)
# Link here: https://www.reuters.com/news/archive/marketNews
# You would essentially be repeating the same project twice (once for business news
# and once again for market news)
