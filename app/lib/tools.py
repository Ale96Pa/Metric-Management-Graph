import networkx as nx
import random
			

def genPosNodes(G,delta,pos):
	print('Start the positioning of nodes according to AS algo')
	#1/03/2023 ho cambiato la sequenza del for che prima era I S CL ad CL I S
	d = {}
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
		d[str(el)] = (int(pos[0]),int(aaaa))

		i+=1


	print(d)
	print('END - the positioning of nodes')
	return d

def makeSubGraphByMetrics(MGM,listOfMetrics):

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
	subGraph	=	 makeSubGraphByMetrics(MGM,listOfMetrics)
	return subGraph