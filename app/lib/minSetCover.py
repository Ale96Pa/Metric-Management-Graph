import networkx as nx
import csv

from lib.draw import drawGraph



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
		
		#print(valMax,index)
	
		I = I.union(set({index}))
		X = X.difference(set(S[index]))
		
	return I

def exeMinSetCoverV1(MGM):
	listOfMetrics = [node for node in MGM.nodes() if 'M' in node]
	listOfClusters = []
	listOfInputs = []
	listOfCovMetrics	=	[]

	for node in MGM.nodes():
		if 'M' in node and MGM.out_degree(node) > 0:
			listOfCovMetrics.append(node)
		elif 'CL' in node:
			listOfClusters.append(node)
		elif 'I' in node:
			listOfInputs.append(node)
	
	subMGM = MGM.subgraph(listOfCovMetrics+listOfClusters)
	
	#SICCOME POSSO AVERE METRICHE CHE NON SONO COLLEGATE A NULLA
	#PRENDO SOLO LE METRICHE CON UN ARCO USCENTE
	#PERCIò creo X e S

	S = makeSForAlgo(listOfClusters,subMGM)
	X = makeXForAlgo(listOfCovMetrics,subMGM)
	
	I = greedyMinSetCover(X, S)

	listOfCovCluster = [listOfClusters[el] for el in I]

	print('[V1] METRICS COV: {}'.format(len(listOfCovMetrics)), '\t/\tALL METRICS: {}'.format(len(listOfMetrics)))
	print('[V1] MIN CLUSTERS COV: {}'.format(len(listOfCovCluster)), '\t/\tALL CLASTERS: {}'.format(len(listOfClusters)))

	
	covGraph_v1 = MGM.subgraph(listOfCovMetrics+listOfCovCluster)

	return listOfCovCluster,covGraph_v1

def exeMinSetCoverV2(MGM,listOfCovCluster):
	listOfClusters = []
	listOfInputs = []
	listOfCovMetrics	=	[]

	for node in MGM.nodes():
		if 'M' in node and MGM.out_degree(node) > 0:
			listOfCovMetrics.append(node)
		elif 'CL' in node:
			listOfClusters.append(node)
		elif 'I' in node:
			listOfInputs.append(node)
	
	subMGM = MGM.subgraph(listOfCovMetrics+listOfCovCluster+listOfInputs)

	
	listOfCovInput = []
	for covCluster in listOfCovCluster:
		for el in subMGM.out_edges(covCluster):
			listOfCovInput.append(el[1])
	
	listOfCovInput    =   list(set(listOfCovInput))

	covGraph_v2 = MGM.subgraph(listOfCovMetrics+listOfCovCluster+listOfCovInput)

	if len(listOfCovInput) > 9:
		print('[V2] MIN INPUTS COV: {}'.format(len(listOfCovInput)), '\t/\tALL INPUTS: {}'.format(len(listOfInputs)))
	else:
		print('[V2] MIN INPUTS COV: {}'.format(len(listOfCovInput)), '\t\t/\tALL INPUTS: {}'.format(len(listOfInputs)))

	return listOfCovInput,covGraph_v2

def getMinimumCostEdge(listOfWeightEdgeAttr, source):
	minW = 999999
	minTarget = None
	for edgeAttr in listOfWeightEdgeAttr:
		tmp_min = listOfWeightEdgeAttr[(edgeAttr[0],edgeAttr[1])]
		if source == edgeAttr[0] and tmp_min < minW:
			minW		=	tmp_min
			minTarget	=	edgeAttr[1]
			
	return minTarget

def getSumMinimumCostEdge(listOfWeightEdgeAttr, source):
	minW = 999999
	minSumTarget = None
	for edgeAttr in listOfWeightEdgeAttr:
		tmp_min = listOfWeightEdgeAttr[(edgeAttr[0],edgeAttr[1])]
		if source == edgeAttr[0] and tmp_min < minW:
			minW			=	tmp_min
			minSumTarget	=	tmp_min
			
	return minSumTarget

def getMinimumCompEdge(edges, source,nodesAttr):
	minW = 999999
	minTarget = None
	for edge in edges:
		tmp_min = int(nodesAttr[edge[1]]['computation'])
		if source == edge[0] and tmp_min < minW:
			minW		=	tmp_min
			minTarget	=	edge[1]
			
	return minTarget

def exeMinSetCoverV3(MGM, listOfCovCluster, listOfCovInput):
	listOfMetrics = [x for x in MGM.nodes if 'M' in x and MGM.out_degree(x) > 0]
	listOfSources = [x for x in MGM.nodes if 'S' in x]

	subMGM 		= 	MGM.subgraph(listOfMetrics+listOfCovCluster+listOfCovInput+listOfSources)

	listOfWeightEdgeAttr		=	nx.get_edge_attributes(subMGM, 'weight')

	listOfMinCostSources		=	[ getMinimumCostEdge(listOfWeightEdgeAttr,inputCov) for inputCov in listOfCovInput if getMinimumCostEdge(listOfWeightEdgeAttr,inputCov) is not None]
	
	totalCost					=	sum([ getSumMinimumCostEdge(listOfWeightEdgeAttr,inputCov) for inputCov in listOfCovInput if getSumMinimumCostEdge(listOfWeightEdgeAttr,inputCov) is not None])
	
	computationNodes	=	nx.get_node_attributes(subMGM, "computation")
	sumComp				=	sum([int(computationNodes[minSource]) for minSource in listOfMinCostSources])

	covGraph_v3 = MGM.subgraph(listOfMetrics+listOfCovCluster+listOfCovInput+listOfMinCostSources)
	
	print('[V3] MIN SOURCE COST: {}'.format(len(listOfMinCostSources)), '\t/\tALL SOURCE: {}'.format(len(listOfSources)))
	print('[V3] THE TOTAL COST IS: {}'.format(totalCost))
	print('[V3] THE TOTAL COMPUTATIONAL COST IS: {}'.format(sumComp))

	return listOfMinCostSources,covGraph_v3
	
def MGMminSetCover(MGM,outputFile,draw=True,saveFig=True,color=True,show=False):
	print('START TASK: MGMminSetCover()')
	outputFile_BASE	=	outputFile.split('.')[0]+"_START."+outputFile.split('.')[1]

	outputFile_v1	=	outputFile.split('.')[0]+"_v1."+outputFile.split('.')[1]
	listOfCovCluster,covGraph_v1	=	exeMinSetCoverV1(MGM)


	outputFile_v2	=	outputFile.split('.')[0]+"_v2."+outputFile.split('.')[1]
	listOfCovInput,covGraph_v2    =   exeMinSetCoverV2(MGM,listOfCovCluster)
	

	outputFile_COMPLETE	=	outputFile.split('.')[0]+"_COVERED."+outputFile.split('.')[1]
	listOfMinCostSources,covGraph_v3	=	exeMinSetCoverV3(MGM,listOfCovCluster,listOfCovInput)

	if draw:
		drawGraph(MGM, outputFile_BASE,saveFig=saveFig,catColor=color,show=show)
		drawGraph(covGraph_v1, outputFile_v1,saveFig=saveFig,catColor=color,show=show)
		drawGraph(covGraph_v2, outputFile_v2,saveFig=saveFig,catColor=color,show=show)
		drawGraph(covGraph_v3, outputFile_COMPLETE,saveFig=saveFig,catColor=color,show=show)
	
	print('END TASK: MGMminSetCover()')
	print('----------------------------------------')

def getListOfClusters(MGM,listOfInput,checkInputs=True):
	#this function respect that a CLUSTER set is a sub sef of nodes
	listOfCluster	=	[]
	for inpt in listOfInput:
		clusters	= [edge[0] for edge in MGM.in_edges(inpt)]	
		for cluster in clusters:
			outEdges	=	[edge[1] for edge in MGM.out_edges(cluster)]
			if checkInputs == True:
				if set(outEdges).issubset(set(listOfInput)):
					listOfCluster.append(cluster)
			else:
				if set(outEdges).issubset(set(checkInputs)):
					listOfCluster.append(cluster)
	
	return list(set(listOfCluster))

def minSetCovByINPUT(MGM, listOfInput, outputFile):
	listOfCluster	= 	getListOfClusters(MGM,listOfInput)
	listOfMetrics	=	list(set([edge[0] for edge in MGM.in_edges(listOfCluster) ]))
	listOfSources	=	[edge[1] for edge in MGM.out_edges(listOfInput) ]

	subGraph	=	MGM.subgraph(listOfMetrics+listOfCluster+listOfInput+listOfSources)

	MGMminSetCover(subGraph,outputFile)

	results	=	('With: {} inputs I covered: {} metrics\n\n').format(len(listOfInput), len(listOfMetrics))	
	print(results)

def minSetCovBySOURCE(MGM, listOfSources, outputFile, listOfInput=True):
	if listOfInput == True:
		listOfInput		=	list(set([edge[0] for source in listOfSources for edge in MGM.in_edges(source) ]))
	listOfCluster	=	getListOfClusters(MGM,listOfInput)
	listOfMetrics	=	list(set([edge[0] for edge in MGM.in_edges(listOfCluster) ]))
	
	subGraph	=	MGM.subgraph(listOfMetrics+listOfCluster+listOfInput+listOfSources)

	MGMminSetCover(subGraph,outputFile)

def maxSetCovByATTR(MGM,valMax,outputFile,attr):
	listOfInputs				=	[inp for inp in MGM.nodes if 'I' in inp]
	listOfWeightEdgeAttr		=	nx.get_edge_attributes(MGM, attr)

	listOfCovSources	=	[]
	listOfCovInputs		=	[]

	for inp in listOfInputs:
		#RICORDA DI PROVARE QUESTO ALGORITMO 
		#CAPIRE SE PASSA TUTTI GLI INPUT IN MODO CORRETTO
		tmpCovInp	=	listOfCovInputs
		minSource	=	getMinimumCostEdge(listOfWeightEdgeAttr,inp)
		param		=	(inp,minSource)
		attrValue	=	listOfWeightEdgeAttr.get(param)
		
		#first because there are inputs without edge
		#second to not consider duplicate
		#third check if the substracrion is correct
		#fourth check if exist a valid cluster
		if (attrValue is not None and 
				minSource not in listOfCovSources and
					valMax - attrValue >= 0 and
						getListOfClusters(MGM,[inp],tmpCovInp+[inp]) ):
			listOfCovSources.append(minSource)
			listOfCovInputs.append(inp)
			valMax -= attrValue
	
	listOfCovCluster	=	getListOfClusters(MGM,listOfCovInputs)
	listOfCovMetrics	=	list(set([edge[0] for edge in MGM.in_edges(listOfCovCluster) ]))

	subGraph	=	MGM.subgraph(listOfCovMetrics+listOfCovCluster+listOfCovInputs+listOfCovSources)
	MGMminSetCover(subGraph,outputFile)

	
def minCapacitySetCover(MGM, outputFile):
	listOfSources		=	[x for x in MGM.nodes if 'S' in x]
	listOfInput			=	[x for x in MGM.nodes if 'I' in x]

	subGraph	=	MGM.subgraph(listOfInput+listOfSources)
	edges	=	subGraph.edges()

	nodesAttr	=	subGraph.nodes

	listOfCovMinCompSources	=	[]
	for inpt in listOfInput:
		covSources	=	getMinimumCompEdge(edges, inpt,nodesAttr)
		if covSources is not None:
			listOfCovMinCompSources.append(covSources)

	listOfCovMinCompSources	=	list(set(listOfCovMinCompSources))
	
	minSetCovBySOURCE(MGM, listOfCovMinCompSources, outputFile)

def correctnessMGM(MGM,outputFile, catColor=True):
	wrongCL = set()
	wrongIN = set()
	vIN = [node for node in MGM.nodes() if 'I' in node]
	vM	= [node for node in MGM.nodes() if 'M' in node]
	vCL = [node for node in MGM.nodes() if 'CL' in node]
	vSRC = [node for node in MGM.nodes() if 'S' in node]

	for inp in vIN:
		if MGM.out_degree(inp) == 0:
			print(inp,MGM.out_degree(inp))
			wrongIN = wrongIN.union({inp})
			wrongCL = wrongCL.union(set([edge[0] for edge in MGM.in_edges(inp) ]))



	for wrong in wrongIN:
		MGM.remove_node(wrong)
	for wrong in wrongCL:
		MGM.remove_node(wrong)

	for mt in vM:
		if MGM.out_degree(mt) == 0:
			MGM.remove_node(mt)
	
	for cl in vCL:
		if MGM.in_degree(cl) == 0:
			MGM.remove_node(cl)

	for inp in vIN:
		if MGM.in_degree(inp) == 0:
			MGM.remove_node(inp)
	
	for src in vSRC:
		if MGM.in_degree(src) == 0:
			MGM.remove_node(src)

	drawGraph(MGM, outputFile, catColor=catColor)
	return MGM
	
	