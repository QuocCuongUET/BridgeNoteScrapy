from sqlalchemy.orm import sessionmaker
from models.foreign_currency_rates import db_connect, create_table, ForeignCurrencyRates

class BridgenotescrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class WriteToMySqlDBPipeline(object):

    def __init__(self):
        engine = db_connect()

        create_table(engine)

        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):

        session = self.Session()

        obj = self.createForeignCurrencyRates(item)

        try:
            session.add(obj)

            session.commit()
        except:
            session.rollback()

            raise
        finally:
            session.close()

        return item


    def createForeignCurrencyRates(self, data):

        return  ForeignCurrencyRates(
                    transfer_date               = data['transfer_date'],
                    based_currency_id           = data['based_currency_id'],
                    transfer_currency_id        = data['transfer_currency_id'],
                    rate_currency_transfer      = data['rate_currency_transfer'],
                    rate_tax_currency_transfer  = data['rate_tax_currency_transfer'],
                    update_user_id              = data['update_user_id'],
                    created_at                  = data['created_at']
                )
