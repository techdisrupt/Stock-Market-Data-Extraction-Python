import os
import pandas as pd



def GetFileList(folder):
	files_list = []
	for root, dirs, files in os.walk(folder):
			path = root.split('/')
			for file in files:
				files_list.append(os.path.join(root, file))
				
	return files_list

def CreateMASUM(filename):
	df = None
	with open(filename, "r") as file_open:
		if "code" not in file_open.read():
			df = pd.read_csv(filename, error_bad_lines=False)
			#print df.head()
			#try:
			df.PER_END_DATE = pd.to_datetime(df.PER_END_DATE, format="%Y-%m-%d", errors="coerce")
			df.groupby(pd.Grouper(key='PER_END_DATE', sort=True))
			df.set_index(['PER_END_DATE'])
			#print df.head()
			#print df.columns.values
			df = df.sort_values('PER_END_DATE', ascending=True)
			#print df.head()
			#pd.rolling_sum(df.EPS_BASIC_CONT_OPER, 4)
			df.EPS_BASIC_CONT_OPER = df.EPS_BASIC_CONT_OPER.rolling(window=4).sum()
			df = df.sort_values('PER_END_DATE', ascending=False).dropna()
			print df.head()
			#df = pd.rolling_sum(df.EPS_BASIC_CONT_OPER, 4)
			#except KeyError:
			#	print "Fail"
			#	pass
		else:
			print "No open"
	return df
			

def WriteMASUM(folder, filename, df):
	df.to_csv(os.path.join(folder, filename))
	

if __name__ == '__main__':
	files_list = GetFileList("eps")
	for filename in files_list:
		print filename
		df = CreateMASUM(filename)
		if df is not None:
			WriteMASUM("eps_year", filename.split("/")[-1], df)	
			
	#print files_list
