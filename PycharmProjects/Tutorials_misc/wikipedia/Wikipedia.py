""" summarizes Wikipedia entries.
https://medium.com/pythoneers/10-useful-automation-scripts-you-need-to-try-using-python-de9c993f1f5
"""

import gensim
import re
from gensim.summarization.summarizer import summarize
import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/Machine_learning'

res = requests.get(url)
soup = BeautifulSoup(res.text,'html.parser')

articles = []
for i in range(len(soup.select('p'))):
    article = soup.select('p')[i].getText().strip()
    articles.append(article)
articlecontent = " ".join(articles)

summary = summarize(articlecontent, ratio = 0.01)
summary = re.sub('\[[^\]]*\]','',summary)
print(summary)