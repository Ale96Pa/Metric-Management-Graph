import networkx as nx
import csv
from lib.draw import drawGraph
from lib.position import pos

#create X from edge to respect the paper S is a subSet of X
def makeXForAlgo(listoOfNodes,Graph):
	X = []
	for node in listoOfNodes:
		#uso > 0 di zero perché devo prendermi solo le metriche 
		# da cui parte almeno 1 arco
		if len(Graph.out_edges(node)) > 0:
			X.append(node)

	return set(X)

#create S
def makeSForAlgo(listoOfNodes,Graph):
	S = []
	for node in listoOfNodes:
		tmpList = []
		for el in Graph.in_edges(node):
			tmpList.append(el[0])
		S.append(tmpList)
	return S

def greedyMinSetCover(X,S):
	I = set({})
	while X != set():
		valMax = 0
		index = 0
		for s in S:
			d = len(set(s).intersection(X))
			if d > valMax:
				valMax = d
				index = S.index(s)
		
		print(valMax,index)
	
		I = I.union(set({index}))
		X = X.difference(set(S[index]))
		
	return I

def exeMinSetCoverV1(fileNodes,MGM,outputFileName,draw=False):
	listOfMetrics = []
	listOfClusters = []
	listOfInputs = []

	for file in fileNodes:
		with open(file, 'r') as db:
			csvreader = csv.reader(db)
			for row in csvreader:
				if 'METRICS.csv' in file:
					listOfMetrics.append(row[0])
				elif 'CLUSTERS.csv' in file:
					listOfClusters.append(row[0])
				else:
					listOfInputs.append(row[0])
	
	subMGM = MGM.subgraph(listOfMetrics+listOfClusters)
   
	listOfClusters = list(set(listOfClusters))
   
	setMetrics	= set(listOfMetrics)
	setClusters	= set(listOfClusters)
	setInputs	= set(listOfInputs)
	
	#SICCOME POSSO AVERE METRICHE CHE NON SONO COLLEGATE A NULLA
	#PRENDO SOLO LE METRICHE CON UN ARCO USCENTE
	#PERCIò creo X e S

	S = makeSForAlgo(listOfClusters,subMGM)
	X = makeXForAlgo(listOfMetrics,subMGM)
	
	I = greedyMinSetCover(X, S)

	listOfCovCluster = [listOfClusters[el] for el in I]

	print(len(listOfClusters),len(listOfCovCluster))

	eff = (len(listOfCovCluster)/len(listOfClusters))*100

	print('Col {}% di cluster riesco a coprire il 100% di metriche che hanno almeno un arco uscente '.format(str(eff)))
	
	covGraph_v1 = MGM.subgraph(listOfMetrics+listOfCovCluster)
	if draw:
		drawGraph(covGraph_v1, outputFileName, pos,True)

	return listOfCovCluster

def exeMinSetCoverV2(fileNodes,listOfCovCluster,MGM,outputFileName,draw=False):
	listOfMetrics = []
	listOfClusters = []
	listOfInputs = []

	for file in fileNodes:
		with open(file, 'r') as db:
			csvreader = csv.reader(db)
			for row in csvreader:
				if 'METRICS.csv' in file:
					listOfMetrics.append(row[0])
				elif 'CLUSTERS.csv' in file:
					listOfClusters.append(row[0])
				else:
					listOfInputs.append(row[0])
	
	subMGM = MGM.subgraph(listOfMetrics+listOfCovCluster+listOfInputs)
	listOfInputs	=	list(set(listOfInputs))
	
	listOfCovInput = []
	for covCluster in listOfCovCluster:
		for el in subMGM.out_edges(covCluster):
			listOfCovInput.append(el[1])
	
	listOfCovInput    =   list(set(listOfCovInput))

	covGraph_v2 = MGM.subgraph(listOfMetrics+listOfCovCluster+listOfCovInput)
	if draw:
		drawGraph(covGraph_v2, outputFileName, pos,True)

	print(len(listOfCovInput),len(listOfInputs))