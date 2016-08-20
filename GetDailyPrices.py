import urllib2
import string
import urllib
import wget	
import requests
import os
import json
from config import *
import datetime
import time
import random
from datetime import timedelta
import re
from datetime import datetime
import os.path
import csv


def CurrentAndDeltaDate(num_years):
	today_date = datetime.today()
	past_date = timedelta(days=-num_years*365)
	hist = today_date + past_date
	c = hist.strftime("%Y")
	a = hist.strftime("%m")
	b = hist.strftime("%d")

	f = today_date.strftime("%Y")
	d = today_date.strftime("%m")
	e = today_date.strftime("%d")
	date_str = "&c="+c+"&a="+a+"&b="+b+"&f="+f+"&d="+d+"&e="+e
	return date_str


def ReadUSCompanies(usoutputfolder):
	for char in string.ascii_uppercase:
		print char
		harvest_url = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter='+char+'&render=download'
		print harvest_url
		output = char+".csv"
		output = os.path.join(usoutputfolder, output)
		r = requests.get(harvest_url, stream=True)
		with open(output, 'wb') as f:
				for chunk in r.iter_content(chunk_size=1024):
						if chunk: # filter out keep-alive new chunks
							f.write(chunk)
							f.flush()
		

def PopulateUS(usoutputfolder, collection=None):
	start = False
	for root, dirs, files in os.walk(usoutputfolder):
			path = root.split('/')
			#print (len(path) - 1) *'---' , os.path.basename(root)
			for file in files:
				#print root, dirs, path, file
				print file
				start = ExtractUS(os.path.join(root, file), collection, start)
		


def WriteTicker(current_tick_fnm, current_tick):

	with open(current_tick_fnm, 'w+') as f:
			f.write(current_tick)


def GetLastTicker(current_ticker_fnm):
	try:
		current_file = open(current_ticker_fnm, 'r')
	except IOError:
		ticker = None
		print "failed to open file."
	else:		
		ticker = current_file.read()
		ticker = ticker.strip("\n").strip().strip(" ")
		current_file.close()
	return ticker



def BuildUS(company, collection):


	valid = Validate(company)
	company = YahooLookup(company['ticker'], yahoo_string, yahoo_keys, company)
	index =  (company["exchange"]).strip(',').rstrip().replace('\n', '')
	try:
		company['index'] = [yahoo_exchange[index]]

	except KeyError:
		pass
	else:
		
		#print company['ticker']
		WriteTicker(current_ticker_fnm, company['ticker'])	
	return company	

def ReplaceMBtoMillion(value):
	
	scale = 1
	if value != 'N/A':
		if 'M' in str(value):
			value = value.replace('M', '')
			scale = 1
			value = scale * float(value)
		if 'B' in str(value):
			value = value.replace('B', '')
			scale = 1000
			value = scale * float(value)
		return "{:.2f}".format(float(value))
	else:
		return value
	
		
	

def GetPriceCloses(ticker, exchange, folder):
	result = ""
	url = "http://ichart.finance.yahoo.com/table.csv?s="+ticker+"&c=2008"
	count = 0
	while True:
		try:	
			r = requests.get(url, stream=True)
			virtual_file = ""
			for chunk in r.iter_content(chunk_size=1024): 
				if chunk: # filter out keep-alive new chunks
					virtual_file += chunk + "\n"

			result = virtual_file.replace('"', '').strip('\r\n')
			
			if not IsRubbish(result) :
				
				break
			else:
				count+=1

			if count > 5:
				
				break;
				break;

			#print count
		except requests.exceptions.ReadTimeout as e:
			print "Time out"
			time.sleep(sleep_sec)
		
		except requests.exceptions.ConnectionError as e:
			print "Connection fail"
			time.sleep(sleep_sec)


	if len(result) > 0:
		#print ticker
		with open(os.path.join(folder,  ticker.replace("^", "").replace("/", "") + "_"+ yahoo_exchange[exchange.replace("/", "")] + ".txt"), "w") as file_write:
			file_write.write(result)
		


	#print result




def WriteCompanySummary(company, folder):

	with open(os.path.join(folder, company["ticker"].replace("^", "").replace("/", "") + "_" + yahoo_exchange[company["exchange"].replace("^", "").replace("/", "")] + ".txt"), 'wb') as f:  # Just use 'w' mode in 3.x
		w = csv.DictWriter(f, company.keys())
		w.writeheader()
		w.writerow(company)
	


def ExtractUS(pathfilename, collection, start):
	file = open(pathfilename, 'r')
	next(file)
	#start = False
	count = 0
	total = 0

	current_ticker = GetLastTicker(current_ticker_fnm)
	#print current_ticker, start
	for line in file:
		#time.sleep(random.randint(0,1))
		total+=1
		#current_ticker = GetLastTicker(current_ticker_fnm)

		#print current_ticker
		line_split = line.replace('"','').split(",")
		#print line_split
		company ={}
		company['ticker'] = line_split[0].strip()
		company['currency'] = 'USD'
		company['name'] = line_split[1].strip()
		company['sector'] = line_split[7].strip()
		company['sector_extra'] = line_split[6].strip()
		company['ipo_date'] = line_split[5].strip()
		company['data_date'] = (datetime.today()).strftime("%d %B %Y")
		print company['name']
		if current_ticker == None or start:
			#print "Building"
			company = BuildUS(company, collection)
			company['market_cap'] = ReplaceMBtoMillion(company['market_cap'])
			company['market_cap2'] = ReplaceMBtoMillion(company['market_cap2'])
			count+=1
			start = True
			if "exchange" in company:
					exchange = yahoo_exchange[company["exchange"]]
			else:
				exchange = "EXCHANGE"

				#print exchange
			GetPriceCloses(company['ticker'], exchange, "prices/daily")
			WriteCompanySummary(company, "summary")
		else:
			#print company['ticker'], current_ticker
			if str(company['ticker']) == str(current_ticker):
				#print "Starting from ", current_ticker
				company = BuildUS(company, collection)
				start = True
				count+=1
				company['market_cap'] = ReplaceMBtoMillion(company['market_cap'])
				company['market_cap2'] = ReplaceMBtoMillion(company['market_cap2'])
				

				if "exchange" in company:
					exchange = yahoo_exchange[company["exchange"]]
				else:
					exchange = "EXCHANGE"

				#print exchange
				GetPriceCloses(company['ticker'], exchange, "companyprices")
				WriteCompanySummary(company, "summary")

	print "Added: ", count, " of: ", total		
	file.close()
	return start

def Validate(company):
	valid = True
	if company['ticker'] == blank:
		valid = False
	return valid
	


def QueryCompanies(collection, comp_name):
	results = collection.find({'name': {"$regex":  comp_name, "$options": 'i' }})
	#results = collection.find()
	"""for result in results:
		print result
	"""

def IsRubbish(result):
	rubbish = False
	if "<" in str(result) or ">" in str(result) or "*" in str(result):
		rubbish = True
	if len(result) > 100:
		rubbish = True
	
	return rubbish




def YahooLookup(symbol, yahoo_string, yahoo_keys, company_dict):
	entity_list = yahoo_string.strip('+').split('+')
	#print entity_list
	for i in xrange(0, len(entity_list)):
		entity = entity_list[i]
		key = yahoo_keys[i]

		url = "http://finance.yahoo.com/d/quotes.csv?s="+symbol+"&f=" + entity
		
		count = 0
		while True:
			try:	
				r = requests.get(url, stream=True)
				virtual_file = ""
				for chunk in r.iter_content(chunk_size=1024): 
					if chunk: # filter out keep-alive new chunks
						virtual_file += chunk + "\n"
	
				result = virtual_file.replace('"', '').strip('\r\n')
				
				if not IsRubbish(result) :
					
					break
				else:
					count+=1


				if count > 5:
					
					break;
					break;

				#print count
			except requests.exceptions.ReadTimeout as e:
				print "Time out"
				time.sleep(sleep_sec)
			
			except requests.exceptions.ConnectionError as e:
				print "Connection fail"
				time.sleep(sleep_sec)
		"""virtual_file = ""
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				virtual_file += chunk + "\n"
	
		columns = []
		result = virtual_file.replace('"', '').strip('\r\n')
	
		print result
		"""
		try:
			if key in company_dict:
				if Empty(company_dict[key]):
					company_dict[key] = result
			else:
				company_dict[key] = result
				
		except IndexError:
			print "Error at: ", symbol
			
	return company_dict



def AddCompanyToDB(collection, company):
	ticker = company['ticker']
	fail = True
	while fail:
		try:
			value_db = collection.find_one({'ticker': ticker})
		except pymongo.errors.AutoReconnect:
			print "###################################"
			print "Failed to find Mongo...trying again"
			print "###################################"
			time.sleep(0)
		else:
			fail = False
		

	if value_db != None:
		for entity in company:

			try:
				value = company[entity]
				value_coll = value_db[entity]
			except KeyError:
				pass
			else:
				if value_coll == 'N/A' or value_coll == '':
					if value != 'N/A' and value != '' or not entity in value_db:
						print "updating ", entity, value
						collection.update({'ticker': ticker},{'$set': {entity:value}}, upsert=False)
						print "Updating"
				if not entity in value_db:
					collection.update({'ticker': ticker},{'$set': {entity:value}}, upsert=True)
					
					print "Adding field: ", entity, value
					
		value_db = collection.find_one({'ticker': ticker})
		#print value_db
		#raw_input()	
	else:

		print "Inserting..."
		collection.insert(company)
	print company['ticker'], company['name']
	

def SortByField(collection, field1, field2=None):
	results = collection.find().sort([(field1, pymongo.ASCENDING), (field2, pymongo.ASCENDING)])
	for result in results:
		print result['dividend_yield'], result['symbol'], result['name']



	
def Empty(my_input):
	if my_input == '' or my_input == 'N/A' or my_input == '-' or my_input == '' or my_input == None or my_input == 0.0:
		empty = True
	else:
		empty = False
	return empty


def TickerExists(ticker, dict_index):
	result = [item for item in dict_index if ticker in item]
	if result == []:
		return False
	else:
		return True


def ReturnIndex(dict_index, ticker):
	found_index = []
	for index in dict_index:
		if TickerExists(ticker, dict_index[index]):
			found_index.append(index)
	return found_index


if __name__ == '__main__':


	usoutputfolder = "uscomp"
	
	sleep_sec = 10
	count = 0
	#client = MongoClient('mongodb://test:poppy123@ds031701.mongolab.com:31701/heroku_app33514681')
	dict_index = {}
	dict_index['NYSE'] = []
	dict_index['NASDAQ'] = []
	

	yahoo_keys = sorted(yahoo_code.keys())
	yahoo_string = ""
	for key in yahoo_keys:
		yahoo_string += "+" + yahoo_code[key]

	#db = client['heroku_app33514681']
	#comp_collection = db['UScompanies']
	#divi_collection = db['USdividends']
	#comp_collection.remove()
	#divi_collection.remove()
	

	#GetPriceCloses("AAPL", "NASDAQ", "companyprices")

	PopulateUS(usoutputfolder, None)


	
	

	

