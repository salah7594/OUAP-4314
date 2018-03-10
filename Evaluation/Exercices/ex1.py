import requests
import argparse
 
class RequestHTTP():
    
    def woof(self, url, timeout=10, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}):

        response = requests.get(url, headers, timeout=timeout)
        if response.status_code != 200:
            print("thank you, come again.", response.status_code)
            return self.woof(url, timeout=10)
        else:
            print("eijklar")
        return response

if __name__ == "__main__":
    test = RequestHTTP()
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="i am helping.")
    args = parser.parse_args()

    print("url", args.url)
    print(test.woof(args.url).status_code)

"""
examples:
    http://httpbin.org/status/404
    http://example.com/
"""

