import scrapy
import csv
from datetime import datetime, timedelta

class KemenkeuSpider(scrapy.Spider):
    name = "kemenkeu"

    start_time = '20180930'
    end_time = '20181030'
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

        if( self.inTimeToSearch(self.start_time, self.end_time) ):
            self.start_time = self.inCreaseTimeByOneDay(self.start_time)
            formdata = self.formDataDate(self.start_time)
            yield scrapy.FormRequest("http://www.fiskal.kemenkeu.go.id/dw-kurs-db.asp",
                                   formdata=formdata,
                                   callback=self.parse)

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

    def inTimeToSearch(self, start_time, end_time):
        start_time = datetime.strptime(start_time, self.STR_DATE_FORMAT)
        end_time = datetime.strptime(end_time, self.STR_DATE_FORMAT)

        return start_time <= end_time

    def inCreaseTimeByOneDay(self, time):
        next_time = datetime.strptime(time, self.STR_DATE_FORMAT)
        next_time = next_time + timedelta(days=1)

        return next_time.strftime(self.STR_DATE_FORMAT)
