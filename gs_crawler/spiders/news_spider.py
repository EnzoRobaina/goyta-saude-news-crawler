import scrapy
import json

class NewsSpider(scrapy.Spider):
    name = 'news'
    start_urls = [
        'https://www.campos.rj.gov.br/fcategoria.php?id_categoria=4',
        'https://www.campos.rj.gov.br/fcategoria.php?id_categoria=4&PGpagina=2&PGporPagina=15'
    ]
      
    def parse(self, response):
        data = []
        for n in response.css('li.item-destaque'):
            thumb = n.css('img.thumbnail::attr(src)').extract_first()
            if(thumb):
                thumb = thumb.replace('width=80&height=60','')
            data.append({
                'a': 'https://www.campos.rj.gov.br/' + n.css('a.title-header::attr(href)').extract_first(),
                'thumb': thumb,
                'titulo': n.css('b::text').extract_first(),
                'texto': n.css('p.data-contente-destaque::text').extract_first()
            })
        return scrapy.Request('http://127.0.0.1:8000/postnoticias/', method='POST', body=json.dumps(data), headers={'Authorization': 'Basic ' + 'YWRtaW46YWRtaW5hZG1pbg==', 'Content-Type':'application/json'}, callback=self.post_cb)
                                                                                                                                    
    def post_cb(self, response):
        print(response.status)