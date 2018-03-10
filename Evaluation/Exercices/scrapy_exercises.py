"""
1. Comparer response.css('title') et response.css('title::text')
> Le premier retourne le tag <title></title> dans le résultat, tandis que le deuxième ne retourne que le contenu '\n\n\t\tleboncoin, site de petites annonces gratuites\n\n'

2. ['https:'+x for x in response.css('a::attr(href)').extract() if not x.startswith('http') and x]

3. 
- scrapy crawl leboncoin -o lbc.csv: comma separated
- scrapy crawl leboncoin -o lbc.json: json dict-like formatting
- scrapy crawl leboncoin -o lbc.jl: json dictionary but each item on a single line
- scrapy crawl leboncoin -o lbc.xml: xml tree format


"""
