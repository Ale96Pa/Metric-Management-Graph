import pandas as pd

sheets = ['METRICS','CLUSTERS','INPUTS',
			'SOURCES','LINK_MT_CL','CLUSTERS','LINK_IN_SRC']

xlsFileName = 'DB.xlsx'
dbPath = 'DB/'



def convertXlsToCSV(sheets=sheets,xlsFileName=xlsFileName,dbPath=dbPath):
	print('Start to convert Xls to CSV')
	df_sheet_multi = pd.read_excel(xlsFileName, sheet_name=sheets)

	for name in sheets:
		filename=dbPath+name+'.csv'
		df_sheet_multi[name].to_csv(filename, header=False, index=False)
		print('The file: {} was created!'.format(filename))
	print('END - to convert Xls to CSV')

