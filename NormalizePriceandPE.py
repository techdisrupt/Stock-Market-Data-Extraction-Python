import quandl
import requests
import pandas as pd
import os, glob, time




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
				tickers.append(file.split("_")[0].strip('.txt'))
	return tickers


def convertToNormal(folder, out_folder, ticker):
	selected = glob.glob(folder + '/' + ticker + '*.txt')
	print selected
	df = pd.read_csv(selected[0], error_bad_lines=False, warn_bad_lines=False)
	max_price = max(df['price'])
	max_pe = max(df['pe'])
	print max_price, max_pe
	df['price'] = df['price'] / max_price
	df['pe'] = df['pe'] / max_pe
	df['date'] = pd.to_datetime(df.date, format="%Y-%m-%d", errors="coerce")	
	df = df.sort_values('date').dropna()
	df.to_csv(os.path.join(out_folder, ticker+".txt"), index = False)


	#print df.head()



if __name__ == '__main__':
	
	tickers = findTickers("price_pe")
	

	


	for i, ticker in enumerate(tickers):
		print "Trying to match the following: ", ticker
		convertToNormal("price_pe", "normalized", ticker)



	
		if i % 100 == 0:
			print "Pausing..."
			time.sleep(1)
		
		
	

