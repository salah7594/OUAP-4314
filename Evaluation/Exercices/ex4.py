"""
J'ai essayé de lancer le requests.get avec ma classe updatedRequestHTTP/RequestHTTP, mais cela ne fonctionnait pas.
Donc j'ai juste fait l'exercice avec un appel classique de requests.
"""

from ex3 import updatedRequestHTTP
import requests
import json
from pprint import pprint

api_call = "https://api.qwant.com/api/search/all?count=10&q=half-life&t=all&device=smartphone&safesearch=1&locale=fr_FR"
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

url_qwant = 'https://api.qwant.com/api/search/ia?safesearch=1&locale=fr_FR&q=juventus&t=all&lang=fr_fr&device=smartphone'

barbara = updatedRequestHTTP()
#response = barbara.woof(api_call, headers=var_headers)
#print(response.text)

#response_json = json.loads(response.text)
#pprint(response_json)

response = requests.get('https://api.qwant.com/api/search/all?count=10&q=juventus&t=all&device=smartphone&safesearch=1&locale=fr_FR', headers=var_headers)
print(response.status_code)
response_json = json.loads(response.text)
#pprint(response_json["data"]["result"]["items"][0])

for x in response_json["data"]["result"]["items"]:
    print(x["url"])
