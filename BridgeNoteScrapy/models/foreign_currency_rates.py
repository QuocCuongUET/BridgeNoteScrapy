from sqlalchemy import create_engine, Column, Integer, Date, Numeric, TIMESTAMP

class ForeignCurrencyRates(Base):

	__tablename__ = "foreign_currency_rates"

	id   		  		 	= Column('id', Integer, nullable=False, primary_key=True, autoincrement=True)
	transfer_date 		 	= Column('transfer_date', Date, nullable=False)
	based_currency_id 	 	= Column('based_currency_id', Integer, nullable=False)
	transfer_currency_id 	= Column('transfer_currency_id', Integer, nullable=False)
	rate_currency_transfer 	= Column('rate_currency_transfer', Numeric(15,6), nullable=False, default=0.000000)
	rate_tax_currency_transfer 	= Column('rate_tax_currency_transfer', Numeric(15,6), nullable=False, default=0.000000)
	update_user_id   	 	   	= Column('update_user_id', Integer, nullable=False)
	created_at  				= Column('created_at', TIMESTAMP)
	updated_at  				= Column('updated_at', TIMESTAMP)
	deleted_at 					= Column('deleted_at', TIMESTAMP)
