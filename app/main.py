import configparser
import networkx as nx

from lib.convertXlsToCSV import convertXlsToCSV
from lib.fromCsvToGraph import genXmlGraph
from lib.fromCsvToGraph import genPosNodes
from lib.fromCsvToGraph import drawGraph

from lib.minSetCover import exeMinSetCoverV1
from lib.minSetCover import exeMinSetCoverV2


config = configparser.ConfigParser()
config.read('config.ini')

########################################################################################
#STEP 1 convert XLS DB TO CSV

pathDbFiles			=	config['DB']['pathDbFiles']
xlsDbPathFile		=	config['DB']['pathDbFiles']+config['DB']['xlsFileName']
sheetNames			=	config['DB']['sheetsName'].split(',')
outputPathDbFiles	=	config['DB']['pathDbFiles']


#convertXlsToCSV(sheetNames,xlsDbPathFile,outputPathDbFiles)

########################################################################################
#STEP 2 convert CSV files in XML file for networkx lib

fileNodes		=	[pathDbFiles+a for a in config['GRAPH']['nodeNames'].split(',')]
fileEdges		=	[pathDbFiles+a for a in config['GRAPH']['edgeNames'].split(',')]
fileGraphName	=	config['GRAPH']['xmlGraphName']


#genXmlGraph(fileNodes, fileEdges, fileGraphName)

########################################################################################
#STEP 3 make position node file to see a good graph
delta			=	[int(x) for x in config['GRAPH']['delta'].split(',')]
pos			    =	[int(x) for x in config['GRAPH']['pos'].split(',')]
filePosName	    =	config['GRAPH']['filePosName']

#genPosNodes(fileNodes, delta, pos, filePosName)

########################################################################################
#STEP 4 draw the graph

outputPath		=	config['GRAPH']['outputPath']
outputFigGraph	=	outputPath+'MGM_w.pdf'

MGM = nx.read_graphml(fileGraphName)

drawGraph(MGM, outputFigGraph)


########################################################################################
#STEP 5 - test MinSetCov v1

outputFile		=	outputPath+'MinSetCov_v1.pdf'

#listOfCovCluster	=	exeMinSetCoverV1(fileNodes, MGM, outputFile)



########################################################################################
#STEP 6 - test MinSetCov v2

outputFile_v2		=	outputPath+'MinSetCov_v2.pdf'

#exeMinSetCoverV2(fileNodes, listOfCovCluster, MGM,outputFile_v2,True)

########################################################################################
print('ok')

