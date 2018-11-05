import scrapy
from datetime import datetime, timedelta

class KemenkeuSpider(scrapy.Spider):
	name = 'kemenkeu'

    def start_requests(self):
        return [scrapy.FormRequest(
                    'http://www.fiskal.kemenkeu.go.id/dw-kurs-db.asp',
                    formdata = {'strDate': '20181029', 'id': '10/29/2018'},
                    callback = self.parse)]

    def parse(self, response):
        table = response.css('div.table-responsive > table')

        data_trs = table.css('tr')
        for tr in data_trs:
            td = tr.css('td::text');
            yield td