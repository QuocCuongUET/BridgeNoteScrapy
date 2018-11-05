import scrapy
import csv
from datetime import datetime, timedelta
from BridgeNoteScrapy.items import ForeignCurrencyRatesItem
from BridgeNoteScrapy.currency_id import detectCurrencyId

class KemenkeuSpider(scrapy.Spider):
    name = "kemenkeu"

    start_time = '20180930'
    end_time = '20181030'
    STR_DATE_FORMAT = "%Y%m%d"
    ID_DATE_FORMAT = "%m/%d/%Y"
    URL_INDO = "http://www.fiskal.kemenkeu.go.id/dw-kurs-db.asp"
    BASED_CURRENCY_ID_IND = 3

    def start_requests(self):
        return [scrapy.FormRequest( self.URL_INDO,
                                    formdata = self.formDataDate(self.start_time),
                                    callback = self.parse)]

    def parse(self, response):
        table = response.css('div.table-responsive > table')

        data_trs = table.css('tr')
        for tr in data_trs:
            td = tr.css('td::text')

            item = self.createItem(td)

            yield item

        if( self.inTimeToSearch(self.start_time, self.end_time) ):
            self.start_time = self.inCreaseTimeByOneDay(self.start_time)
            formdata = self.formDataDate(self.start_time)
            yield scrapy.FormRequest(self.URL_INDO,
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

    def createItem(self, data):

        transfer_currency_id   = self.dectectCurrency(data[1].extract())
        rate_currency_transfer = self.formatRateCurrency(data[2].extract())

        item = ForeignCurrencyRatesItem()

        item['transfer_date'] = self.start_time

        item['based_currency_id'] = self.BASED_CURRENCY_ID_IND

        item['transfer_currency_id'] = detectCurrencyId(transfer_currency_id)

        item['rate_currency_transfer'] = rate_currency_transfer

        item['rate_tax_currency_transfer'] = 0

        item['update_user_id'] = 0

        item['created_at'] = datetime.now()

        return item

    def dectectCurrency(self, str):

        # Because format str is 'somthing word (USD)'
        return str[-5:][1:4] # HardCode

    def formatRateCurrency(self, str):

        # Format string is same 932,485,392.983
        rate_currency_transfer = str.replace(',', '')
        return round(float(rate_currency_transfer), 6)
