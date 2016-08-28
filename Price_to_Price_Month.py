import os
import pandas as pd



def GetClosePrices(filenamepath):
	print filenamepath
	df = None
	with open(filenamepath, 'r') as file_open:

		if "404 Not Found" not in file_open.read():
			df = pd.read_csv(filenamepath, error_bad_lines=False).dropna()
			#print list(df.columns.values)
			#print df
			#print df.dtypes
			#print df.Date
			#raw_input()
			##try:
			df.Date = pd.to_datetime(df.Date, format="%Y-%m-%d", errors="coerce")
			#df.Date = pd.to_datetime(df.Date)

			df = df.set_index(['Date'])
			#ddf.groupby(pd.Grouper(key='Date', sort=True))
			#df = df.groupby(pd.TimeGrouper(freq='M', key='Date'))

			#df = df.groupby(pd.TimeGrouper('M'))
			df = df.resample("M").mean().dropna()

			#print "dummy"
			#print df.head().round(2)
			#df = df.sort(['Date'], ascending=['0'])
			#print df.head().round(2)
			#raw_input()
			#print df.columns

			#except KeyError:
				#pass
			#except AttributeError:
			#	pass
		else:
			print "Empty file	"
		
	return df
			

def ExtractFile(filename, output_folder):
	
	df_monthly = GetClosePrices(filename)
	if df_monthly is not None:
		ticker = filename.split("/")[-1].replace('.txt', '') 
		df_monthly.to_csv(os.path.join(output_folder, ticker + ".txt"))
	


def GetListFiles(folder):
	file_list = []
	for root, dirs, files in os.walk(folder):
		path = root.split('/')
		for file in files:
		
			file_list.append(os.path.join(root, file))
	return file_list	
	


if __name__ == '__main__':

	file_list = sorted(GetListFiles("prices/daily"))
	for filename in file_list:
		print filename
		#raw_input()
		ExtractFile(filename, "prices/monthly")
		
	

	pass
