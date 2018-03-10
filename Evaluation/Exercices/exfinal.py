import requests
import json
from pprint import pprint
import re

url = "https://api.qwant.com/api/search/news?count=10&q=sport&t=news&safesearch=1&locale=fr_FR"
var_headers = {
    'Origin': 'https://www.qwant.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,ca;q=0.6,de;q=0.5,pt;q=0.4,sk;q=0.3,vi;q=0.2,ru;q=0.1,it;q=0.1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Referer': 'https://www.qwant.com/',
    'Connection': 'keep-alive',
    'DNT': '1',
}
response = requests.get(url, headers=var_headers)
response_json = json.loads(response.text)

#titre de la page?
#image: bof.

var_list = []
for x in response_json["data"]["result"]["items"]:
    if(len(x["media"]))>0:
        var_image = x["media"][0]["pict"]["url"]
    var_list.append(
    {
        "url": x["url"],
        "domain": x["domain"],
        "category": x["category"],
        "title_article": re.sub('<[^<]+?>', '', x["title"]),
        "image": var_image,
        "description": re.sub('<[^<]+?>', '', x["desc"]),
        "description_short": re.sub('<[^<]+?>', '', x["desc_short"])

    }
    )
pprint(var_list)
