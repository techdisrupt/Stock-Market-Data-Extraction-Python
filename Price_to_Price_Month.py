import os
import pandas as pd



def GetClosePrices(filenamepath):
	#print filenamepath
	monthly = None
	with open(filenamepath, 'r') as file_open:

		if "404 Not Found" not in file_open.read():
			df = pd.read_csv(filenamepath, error_bad_lines=False)
			#print list(df.columns.values)
			#print df.head()
			#print df.dtypes
			#print df.Date
			#raw_input()
			try:
				df.Date = pd.to_datetime(df.Date, format="%Y-%m-%d", errors="coerce")
				df.groupby(pd.Grouper(key='Date', sort=True))
				df.groupby(pd.TimeGrouper(freq='M', key='Date'))
				daily = df.set_index(['Date'])
				monthly = daily.Open.resample("M", how="mean").dropna()
				#print df.dtypes
			except KeyError:
				pass
			except AttributeError:
				pass
			#print pd.to_datetime(df.Date, unit='d')
			#print type(monthly)
			#print(monthly.head())
	return monthly
			

def ExtractFile(filename, output_folder):
	
	monthly = GetClosePrices(filename)
	#print type(monthly), type(pd.core.series.Series)
	if isinstance(monthly, pd.core.series.Series):
		ticker = filename.split("_")[0].split("/")[1] + '_'+ filename.split("_")[1].split('.txt')[0]
		print ticker
		monthly.to_csv(os.path.join(output_folder, ticker + ".txt"))
		


def GetListFiles(folder):
	file_list = []
	for root, dirs, files in os.walk(folder):
		path = root.split('/')
		#print (len(path) - 1) *'---' , os.path.basename(root)
		for file in files:
			#print root, dirs, path, file
			#print file
			#print os.path.join(root, file)
			file_list.append(os.path.join(root, file))
	return file_list	
	


if __name__ == '__main__':

	file_list = sorted(GetListFiles("companyprices"))
	for filename in file_list:
		ExtractFile(filename, "monthlies")
		
	

	pass
