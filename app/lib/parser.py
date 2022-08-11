import csv
import networkx as nx


def getGraphFromCSV(fileNodes,fileEdges,fileGraphName):
	G = nx.DiGraph()
	for file in fileNodes:
		with open(file, 'r') as db:
			csvreader = csv.reader(db)
			for row in csvreader:
				if 'M' in row[0]:
					G.add_node(row[0], category=row[1])
				if 'S' in row[0]:
					G.add_node(row[0], computation=row[5])
				else:
					G.add_node(row[0])

	
	for file in fileEdges:
		with open(file, 'r') as db:
			csvreader = csv.reader(db)
			for row in csvreader:
				if 'LINK_MT_CL' in file:
					G.add_edge(row[1], row[0])
				elif 'LINK_IN_SRC' in file:
					G.add_edge(row[0], row[1], weight=int(row[2]))
				else:
					G.add_edge(row[0], row[1])
					
	nx.write_graphml_lxml(G,fileGraphName)

	return G
	#return a graph object