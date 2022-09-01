import networkx as nx
import configparser
import random
import time
import json


from lib.convertXlsToCSV import convertXlsToCSV
from lib.parser import getGraphFromCSV
from lib.parser import fromNetxToCyTo

from lib.tools import genPosNodes
from lib.tools import makeSubGraphByMetrics
from lib.tools import makeCategorySubGraph
from lib.position import pos

from lib.draw import drawGraph



from lib.minSetCover import exeMinSetCoverV1
from lib.minSetCover import exeMinSetCoverV2
from lib.minSetCover import exeMinSetCoverV3
from lib.minSetCover import MGMminSetCover
from lib.minSetCover import minSetCovByINPUT
from lib.minSetCover import minSetCovBySOURCE
from lib.minSetCover import maxSetCovByATTR
from lib.minSetCover import minCapacitySetCover
from lib.minSetCover import correctnessMGM

start = time.time()
config = configparser.ConfigParser()
config.read('config.ini')
print('START - MAIN')

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
position		=	[int(x) for x in config['GRAPH']['position'].split(',')]
filePosName	    =	config['GRAPH']['filePosName']

#genPosNodes(MGM, delta, position, filePosName)

########################################################################################
#STEP 4 draw the graph

outputPath		=	config['GRAPH']['outputPath']
outputFigGraph	=	outputPath+'MGM_COLORED.pdf'

#drawGraph(MGM, outputFigGraph, catColor=True)


########################################################################################
#STEP 5 apply CORRECTNESS
outputFigGraphCorr	=	outputPath+'MGM_CORRECTNESS.pdf'

MGM = correctnessMGM(MGM,outputFigGraphCorr)

########################################################################################
#STEP 5 - test MinSetCov METRIC -> CLUSTER 

outputFile		=	outputPath+'MGM_MinSetCov-Colored_v1.pdf'
#listOfCovCluster,covGraph_v1	=	exeMinSetCoverV1(MGM)
#drawGraph(covGraph_v1, outputFile,catColor=True)


########################################################################################
#STEP 6 - test MinSetCov METRIC -> COVERED(CLUSTERS) -> INPUT

outputFile_v2		=	outputPath+'MGM_MinSetCov-Colored_v2.pdf'
#listOfCovInput,covGraph_v2      =   exeMinSetCoverV2(MGM,listOfCovCluster)
#drawGraph(covGraph_v2, outputFile_v2,catColor=True)

########################################################################################
#STEP 7 - test MinSetCov METRIC -> COVERED(CLUSTERS) -> INPUT -> source with MIN WEIGHT()

outputFile_v3		=	outputPath+'MGM_MinSetCov-Colored_v3.pdf'
#listOfMinCostSources,covGraph_v3   =   exeMinSetCoverV3(MGM,listOfCovCluster,listOfCovInput)
#drawGraph(covGraph_v3, outputFile_v3,catColor=True)

########################################################################################
########################################################################################
#T450 - find the smallest set of inputs that covers all METRIC

outputFileSmallestInMetric  =   outputPath+'MGM_MinSetCover_TOTAL-Colored.pdf'
MGMminSetCover(MGM, outputFileSmallestInMetric)


########################################################################################
#T451 - Take a subSet of Metric and run the min-set-cover-metric

listOfMetrics   = [node for node in MGM.nodes() if 'M' in node and random.random() > 0.65]
subGraph    =   makeSubGraphByMetrics(MGM,listOfMetrics)

outputFileSmallestInMetric  =   outputPath+'MGM_MinSetCover_SUBSET_Metrics-Colored.pdf'
#MGMminSetCover(subGraph, outputFileSmallestInMetric)

#######################################################################################
#T452 - Take a subSet of CATEGORY Metric and run the min-set-cover-metric

category	=	['Vulnerability Metrics','Situation Metrics']
subGraph	=	makeCategorySubGraph(MGM, category)

outputFileSmallestInMetric  =   outputPath+'MGM_MinSetCover_CATEGORY_Metrics-Colored.pdf'
#MGMminSetCover(subGraph, outputFileSmallestInMetric)

#######################################################################################
#T453 - Take a subSet of INPUTS (or 1 INPUT) - what are all the metrics which I can cover?

listOfInput	=	[node for node in MGM.nodes() if 'I' in node and random.random() > 0.65]

outputFileminSetCovByInput	=	outputPath+'MGM_MinSetCover_ByINPUT-COLORED.pdf'
#minSetCovByINPUT(MGM,listOfInput,outputFileminSetCovByInput)

#######################################################################################
#T454 - Take a subSet of SOURCE (or 1 SOURCE) - what are all the metrics which I can cover?

listOfSources	=	[node for node in MGM.nodes() if 'S' in node and random.random() > 0.65]
listOfSources    =   ['S001', 'S003', 'S004', 'S012', 'S020', 'S021', 'S022', 'S030', 'S032', 'S033', 'S036', 'S039']

outputFileminSetCovBySOURCE	=	outputPath+'MGM_MinSetCover_BySOURCE-COLORED.pdf'
#minSetCovBySOURCE(MGM, listOfSources, outputFileminSetCovBySOURCE)

#######################################################################################
#T455 - Given in input a Graph and a MAXIMUM COST return all metric covered

maximumCost =   15

outputFileMetricsToMaxCost  =   outputPath+'MGM_MaxSetCover_ByCOST-COLORED.pdf'
#maxSetCovByATTR(MGM,maximumCost,outputFileMetricsToMaxCost,attr='weight')

#######################################################################################
#T456 - What is the minimum computational capacity to cover a list of metrics?

outputFileMinCAPACITY  =   outputPath+'MGM_MinCAPACITY-COLORED.pdf'
minCapacitySetCover(MGM,outputFileMinCAPACITY)





print('END - MAIN')
end = time.time()
print(end - start)
