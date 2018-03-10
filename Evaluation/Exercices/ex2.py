import re
import requests
from ex1 import RequestHTTP
from urllib.parse import urlparse

def compact_space(string):
    string = string.strip()
    string = re.sub("\s+", " ", string)
    return string

print(compact_space("       forgive   me for   i have          sinned "))

url = "http://motherfuckingwebsite.com/"

requesthttp = RequestHTTP()
request_text = requesthttp.woof(url).text
request_text = re.sub('<[^<]+?>', '', request_text)
print(compact_space(request_text))
print("\ndomain: ", urlparse(url).netloc)
