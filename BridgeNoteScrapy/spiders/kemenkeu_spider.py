import scrapy
import csv
from datetime import datetime, timedelta

class KemenkeuSpider(scrapy.Spider):
    name = "kemenkeu"

    start_time = '20180927'
    STR_DATE_FORMAT = "%Y%m%d"
    ID_DATE_FORMAT = "%m/%d/%Y"
    URL_INDO = "http://www.fiskal.kemenkeu.go.id/dw-kurs-db.asp"

    def start_requests(self):
        return [scrapy.FormRequest( self.URL_INDO,
                                    formdata = self.formDataDate(self.start_time),
                                    callback = self.parse)]

    def parse(self, response):
        table = response.css('div.table-responsive > table')

        data_trs = table.css('tr')
        for tr in data_trs:
            td = tr.css('td::text');

            data = [td[0].extract(), td[1].extract(), td[2].extract(), td[3].extract()]
            yield self.writeCSV(data)

    def writeCSV(self, data):
        with open('kemenkeu.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(data)

    def formDataDate(self, time):
        str_time = datetime.strptime(time, self.STR_DATE_FORMAT)

        return {
            "strDate" : datetime.strftime(str_time, self.STR_DATE_FORMAT),
            "id"      : datetime.strftime(str_time, self.ID_DATE_FORMAT)
        }
