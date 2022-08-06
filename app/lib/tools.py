import networkx as nx
import random
			

def genPosNodes(G,delta,pos,filePosName):
	print('Start the positioning of nodes according to AS algo')
	f = open(filePosName, "w")
	f.write('pos = {\n')
	
	find = 0
	i=1
	for el in G.nodes:
		if 'CL' in el and find == 0:
			find = 1
			i=1
			delta.pop(0)
			pos.pop(0)
		if 'I' in el and find == 1:
			find = 2
			i=1
			delta.pop(0)
			pos.pop(0)
		if 'S' in el and find == 2:
			find = 3
			i=1
			delta.pop(0)
			pos.pop(0)
		
		aaaa=str((i*4)+((i-1)*delta[0]))
		posizione="'{}': ({}, {}),\n".format(str(el),str(pos[0]),aaaa)
		if el == list(G.nodes)[-1]:
			posizione="'{}': ({}, {})\n}}".format(str(el),str(pos[0]),aaaa)
		print(posizione)
		f.write(posizione)

		i+=1



	#f.write("'NULLO': (55, 210)\n}")
	f.close()
	print('END - the positioning of nodes')


def makeRandSubGraph(MGM,listOfMetrics):

	listOthersNode  = [ node for node in MGM.nodes() if 'M' not in node]
	subGraph    =   MGM.subgraph(listOfMetrics+listOthersNode)

	list_of_dangl_CL = [node for node in subGraph.nodes if subGraph.in_degree(node) > 0 and 'CL' in node]
	listOthersNode  =[ node for node in MGM.nodes() if 'M' not in node and 'CL' not in node]
	subGraph    =   subGraph.subgraph(listOfMetrics+list_of_dangl_CL+listOthersNode)


	list_of_dangl_IN = [node for node in subGraph.nodes if subGraph.in_degree(node) > 0 and 'I' in node]
	listOthersNode  =[ node for node in MGM.nodes() if 'M' not in node and 'CL' not in node and 'I' not in node]
	subGraph    =   subGraph.subgraph(listOfMetrics+list_of_dangl_CL+list_of_dangl_IN+listOthersNode)

	list_of_dangl_SRC = [node for node in subGraph.nodes if subGraph.in_degree(node) > 0 and 'S' in node]
	subGraph    =   subGraph.subgraph(listOfMetrics+list_of_dangl_CL+list_of_dangl_IN+list_of_dangl_SRC)

	return subGraph

def makeCategorySubGraph(MGM, category):
	listOfMetrics   = [node[0] for node in MGM.nodes(data="category") if node[1] in category]
	subGraph	=	 makeRandSubGraph(MGM,listOfMetrics)
	return subGraph