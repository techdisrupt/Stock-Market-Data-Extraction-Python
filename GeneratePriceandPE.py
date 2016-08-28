import quandl
import requests
import pandas as pd
import os, glob, time

#print dir(quandl)

API_KEY = "VNBM61bWK3XD1xqdxNiC"

def findTickers(outputfolder):
	tickers = []
	for root, dirs, files in os.walk(outputfolder):
		path = root.split('/')
		#print (len(path) - 1) *'---' , os.path.basename(root)
		for file in files:
			
			

			filename = os.path.join(root, file)
			print filename
			#print root, dirs, path, file
			#print filename.split("_"), filename

			if ".txt" in file:
				tickers.append(file.split("_")[0])
	return tickers


def getData(url, ticker, folder, type_data):
	r = requests.get(url, stream=True)
	virtual_file = ""
	for chunk in r.iter_content(chunk_size=1024): 
		if chunk: # filter out keep-alive new chunks
			#virtual_file += chunk + "\n"
			virtual_file += chunk
	#result = virtual_file.replace('"', '').strip('\r\n')
	result = virtual_file
	with open(os.path.join(folder, ticker + "_"+type_data+".txt"), "w") as writer:
		writer.write(result)
	return result

def getFromFolder(ticker, folder, type_data=None):
	df = None
	selected = glob.glob(folder + '/' + ticker + '_*.txt')
	if len(selected) > 0:
		result_file = selected[0]
		print result_file 
		try:
			df = pd.read_csv(result_file, error_bad_lines=False, warn_bad_lines=False)
		except pd.io.common.EmptyDataError:
			df = None
	return (df, df.shape[0] if df is not None else 0)


def Match(df_prices, df_eps, df_pe, ticker, folder):
	
	
	if df_prices[1] > 1:
		
		if df_pe[1] > 1:

			
			count = 0
			df = pd.DataFrame(columns=('date', 'price', 'pe', 'ticker'))
			print df_pe[0].columns.values
			print ticker
			print "compare prices, PE"
			for i, pe_row in df_pe[0].iterrows():
				if pe_row['dimension'] == 'ARQ':
					#print pe_row['calendardate'], pe_row['pe']
					for j, price_row in df_prices[0].iterrows():
						#print pe_row['calendardate'], price_row['Date']
						#raw_input()
						if price_row['Date'] == pe_row['calendardate']:
							#print pe_row['calendardate'], price_row['Close'], pe_row['pe'], ticker
							#raw_input()		
							print "Appending...", pe_row['calendardate'], price_row['Date']
							df = df.append({'date': pe_row['calendardate'], 'price':price_row['Close'], 'pe': pe_row['pe'], 'ticker': ticker}, ignore_index=True)
							#df.loc[count] = [pe_row['calendardate'], price_row['Close'], pe_row['pe'], ticker]
							#count+=1
						
			df = df.sort_values('date', ascending=False).dropna()

			#print df.head()
			#raw_input()

			df.to_csv(os.path.join(folder, ticker+".txt"), index = False)
			
				
		elif df_eps[1] > 1:
			count = 0
			df = pd.DataFrame(columns=('date', 'price', 'pe', 'ticker'))
			print ticker	
			print "compare prices, EPS"
			for i, eps_row in df_eps[0].iterrows():
				#print pe_row['calendardate'], pe_row['pe']
				for j, price_row in df_prices[0].iterrows():
					if price_row['Date'] == eps_row['PER_END_DATE']:
						print eps_row['PER_END_DATE'], price_row['Close'], pe_row['pe'], ticker
						df.loc[count] = [eps_row['PER_END_DATE'], price_row['Close'], float(price_row['Close'])/float(eps_row['EPS_BASIC_CONT_OPER']), ticker]
						count+=1
			df = df.sort_values('date', ascending=False).dropna()
			df.to_csv(os.path.join(folder, ticker+".txt"), index = False)
			
		else:
			pass
			#print "No Match"	

	

if __name__ == '__main__':
	EPS_FOLDER = "eps_year"
	PE_FOLDER = "pe"
	PRICE_FOLDER = "prices/monthly"
	OUTPUT_FOLDER = "price_pe"
	tickers = findTickers("prices/monthly")

	try:
		with open('current_ticker_Price_PE.txt', 'r') as file:
			current_tick = file.read()
	except IOError:
		current_tick = None
		pass

	start = False
	for i, ticker in enumerate(tickers):
		print "Trying to match the following: ", ticker

		if ticker == current_tick or start or current_tick == None:
			start = True
		df_prices = getFromFolder(ticker, PRICE_FOLDER)
		df_eps = getFromFolder(ticker, EPS_FOLDER)
		df_pe = getFromFolder(ticker, PE_FOLDER)
		Match(df_prices, df_eps, df_pe, ticker, OUTPUT_FOLDER)

		with open('current_ticker_Price_PE.txt', 'w') as file:
			file.write(ticker)

		if i % 100 == 0:
			print "Pausing..."
			time.sleep(1)
		
		

		

