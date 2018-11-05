import scrapy
import csv
from datetime import datetime, timedelta

class KemenkeuSpider(scrapy.Spider):
    name = "kemenkeu"

    def start_requests(self):
        return [scrapy.FormRequest( 'http://www.fiskal.kemenkeu.go.id/dw-kurs-db.asp',
                                    formdata = {'strDate': '20181029', 'id': '10/29/2018'},
                                    callback = self.parse)]

    def parse(self, response):
        table = response.css('div.table-responsive > table')

        data_trs = table.css('tr')
        for tr in data_trs:
            td = tr.css('td::text');
            # data = {
            #     'No':        td[0].extract(),
            #     'Mata Uang': td[1].extract(),
            #     'Nilai':     td[2].extract(),
            #     'Perubahan': td[3].extract(),
            # }
            # yield data

            data = [td[0].extract(), td[1].extract(), td[2].extract(), td[3].extract()]
            yield self.writeCSV(data)

    def writeCSV(self, data):
        with open('kemenkeu.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(data)
