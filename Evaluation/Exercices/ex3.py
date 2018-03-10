import requests
from bs4 import BeautifulSoup
from ex1 import RequestHTTP
import random
from urllib.parse import urlparse
from pprint import pprint
import re

#url = "http://motherfuckingwebsite.com/"

class updatedRequestHTTP(RequestHTTP):
    def __init__(self):
       
        self.list_headers = ["Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)",
                        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1",
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                        "Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36"]

    def fetch_soup(self, url):
   
        #print(self.list_headers)
        var_header = {'User-Agent': random.choice(self.list_headers)}
        response = self.woof(url, headers=var_header)
        soup = BeautifulSoup(response.text, "lxml")
        print("si, claro")
        return soup

    def fetch_stuff(self, soup, url):

        everything = {}
        everything["title"] = soup.find_all("title")
        everything["h1"] = soup.find_all("h1")
        everything["img"] = [x["src"] for x in soup.find_all("img")]

        domain = urlparse(url).netloc
        everything["outside_world"] = [x["href"] for x in soup.find_all("a") if not domain in x["href"]]
        everything["p"] = [self.clean(x.text) for x in soup.find_all("p")]
        #everything["p"] = [x.text for x in soup.find_all("p")]
        return everything

    def clean(self, string):
        
        string = re.sub('<[^<]+?>', '', string)
        string = string.strip()
        string = re.sub("\s+", " ", string)
        return string

    def fetch_sitemap(self, soup):

        everything = {}
        var_list = []
        for x in soup.find_all("url"):
             var_list.append({
                    "loc": x.find("loc").text,
                    "changefreq": x.find("changefreq").text,
                    "priority": x.find("priority").text,
                    "lastmod": x.find("lastmod").text
                    })
        everything["all"] = var_list
        return everything

if __name__ == "__main__":

    url = "http://www.yourhtmlsource.com/myfirstsite/basicimages.html"
    minsk = updatedRequestHTTP()
    var_soup = minsk.fetch_soup(url)
    pprint(minsk.fetch_stuff(var_soup, url))

    print("\nSitemap parsing:")
    url_sitemap = "https://www.qwant.com/sitemap.xml"
    rangoon = updatedRequestHTTP()
    var_soup = rangoon.fetch_soup(url_sitemap)
    pprint(rangoon.fetch_sitemap(var_soup))

