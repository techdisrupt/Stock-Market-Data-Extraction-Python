import quandl
import requests
import pandas as pd
import os, time



#https://www.quandl.com/api/v3/datatables/SHARADAR/SF1.csv?ticker=AAPL&api_key=VNBM61bWK3XD1xqdxNiC

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
	print "Trying (EPS/PE)... ", ticker, folder
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
	
	


if __name__ == '__main__':
	
	tickers = findTickers("prices/daily")
	
	try:
		with open('current_ticker.txt', 'r') as file:
			current_tick = file.read()
	except IOError:
		current_tick = None
		pass
	
	start = False
	for i, ticker in enumerate(tickers):
		print "Ticker: ", ticker
		if ticker == current_tick or start or current_tick == None:
			start = True
			url = "https://www.quandl.com/api/v3/datatables/SHARADAR/SF1.csv?ticker="+ticker+"&api_key="+API_KEY
			getData(url, ticker, "pe", "FULL")
			url = "https://www.quandl.com/api/v3/datasets/ZFA/"+ticker+"_EPS_BASIC_CONSOL_Q.csv?api_key="+API_KEY
			getData(url, ticker, "eps", "EPS")
			with open('current_ticker.txt', 'w') as file:
				file.write(ticker)

			if i % 100 == 0:
				print "Pausing..."
				time.sleep(5)
		#url = "https://www.quandl.com/api/v3/datatables/SHARADAR/SF1.csv?ticker="+ticker+"&api_key="+API_KEY
		#url = "https://www.quandl.com/api/v3/datasets/ZFA/GE_EPS_BASIC_CONT_OPER_Q.csv?api_key="+API_KEY
		#url = "https://www.quandl.com/api/v3/datasets/ZFA/"+ticker+"_EPS_BASIC_CONSOL_Q.csv?api_key="+API_KEY

		#r = requests.get(url, stream=True)
		#virtual_file = ""
		#for chunk in r.iter_content(chunk_size=1024): 
		#	if chunk: # filter out keep-alive new chunks
				#virtual_file += chunk + "\n"
		#		virtual_file += chunk
		#result = virtual_file.replace('"', '').strip('\r\n')
		#result = virtual_file
		#with open(os.path.join("eps", ticker + "_EPS.txt"), "w") as writer:
		#	writer.write(result)


	#print result[0]
	#res = pd.read_csv(os.path.join("eps", ticker + "_EPS.txt"))
	#print res.columns.values
	#print res.head()
	#res.calendardate = pd.to_datetime(res.calendardate, format="%Y-%m-%d", errors="coerce")
	#quart = res.set_index(['calendardate'])
	#monthly = quart.pe.resample("M", how="mean").dropna()
	#print monthly.head()
	#print monthly

