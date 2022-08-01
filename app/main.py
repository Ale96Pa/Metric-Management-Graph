import networkx as nx
import configparser

from lib.convertXlsToCSV import convertXlsToCSV
from lib.parser import getGraphFromCSV

from lib.tools import genPosNodes
from lib.position import pos

from lib.draw import drawGraph



from lib.minSetCover import exeMinSetCoverV1
from lib.minSetCover import exeMinSetCoverV2
from lib.minSetCover import exeMinSetCoverV3


config = configparser.ConfigParser()
config.read('config.ini')

########################################################################################
#STEP 1 convert XLS DB TO CSV

pathDbFiles			=	config['DB']['pathDbFiles']
xlsDbPathFile		=	pathDbFiles+config['DB']['xlsFileName']
sheetNames			=	config['DB']['sheetsName'].split(',')
outputPathDbFiles	=	pathDbFiles


#convertXlsToCSV(sheetNames,xlsDbPathFile,outputPathDbFiles)

########################################################################################
#STEP 2 convert CSV files in GRAPH Obj for networkx

fileNodes		=	[pathDbFiles+a for a in config['GRAPH']['nodeNames'].split(',')]
fileEdges		=	[pathDbFiles+a for a in config['GRAPH']['edgeNames'].split(',')]
fileGraphName	=	config['GRAPH']['graphMLName']


MGM	=	getGraphFromCSV(fileNodes, fileEdges, fileGraphName)


########################################################################################
#STEP 3 make position node file to see a good graph

delta			=	[int(x) for x in config['GRAPH']['delta'].split(',')]
position			    =	[int(x) for x in config['GRAPH']['position'].split(',')]
filePosName	    =	config['GRAPH']['filePosName']

#genPosNodes(MGM, delta, position, filePosName)

########################################################################################
#STEP 4 draw the graph

outputPath		=	config['GRAPH']['outputPath']
outputFigGraph	=	outputPath+'MGM_COLORED.pdf'

#drawGraph(MGM, outputFigGraph, pos, catColor=True)


########################################################################################
#STEP 5 - test MinSetCov METRIC -> CLUSTER 

outputFile		=	outputPath+'MinSetCov-Colored_v1.pdf'

listOfCovCluster	=	exeMinSetCoverV1(MGM, outputFile)



########################################################################################
#STEP 6 - test MinSetCov METRIC -> COVERED(CLUSTERS) -> INPUT

outputFile_v2		=	outputPath+'MinSetCov-Colored_v2.pdf'

listOfCovInput      =   exeMinSetCoverV2(MGM,listOfCovCluster, outputFile_v2)

########################################################################################
#STEP 7 - test MinSetCov METRIC -> COVERED(CLUSTERS) -> INPUT -> source with MIN WEIGHT()

outputFile_v3		=	outputPath+'MinSetCov-Colored_v3.pdf'

exeMinSetCoverV3(MGM,listOfCovCluster,listOfCovInput,outputFile_v3,True)


########################################################################################
print('ok')

