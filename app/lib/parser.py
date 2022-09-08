import csv
import networkx as nx
import json


def getGraphFromCSV(fileNodes,fileEdges,fileGraphName):
	G = nx.DiGraph()
	for file in fileNodes:
		with open(file, 'r') as db:
			csvreader = csv.reader(db)
			for row in csvreader:
				if 'M' in row[0]:
					G.add_node(row[0], category=row[1], name=row[2])
				if 'S' in row[0]:
					G.add_node(row[0], computation=row[5], name=row[1])
				elif 'I' in row[0]:
					G.add_node(row[0], name=row[1])

	
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

def fromNetxToCyTo(G,outfileName, pos):
	jsonGrpah = nx.cytoscape_data(G) 
	cc = 1
	state = 0
	for xx in jsonGrpah['elements']['nodes']:
		iid = xx['data']['id']
		if  'I' in iid and state == 0:
			cc=1
			state = 1
		if  'S' in iid and state == 1:
			cc=1
			state = 2
		if  'CL' in iid and state == 2:
			cc=1
			state = 3
		if 'M' in iid:
			x = pos[iid][0]+(100)
			y = pos[iid][1]+(50*cc)
			cc+= 1
		elif 'CL' in iid:
			x = pos[iid][0]+(400)
			y = pos[iid][1]+(100*cc)
			cc+=1
		elif 'I' in iid:
			x = pos[iid][0]+(700)
			y = pos[iid][1]+(85*cc)
			cc+=1
		elif 'S' in iid:
			x = pos[iid][0]+(1000)
			y = pos[iid][1]+(70*cc)
			cc+=1
		xx.update({'position':{'x': x, 'y': y}})

	#ADD ID TO EDGES - MISSING IN ORIGINAL LIBRARY
	for xx in jsonGrpah['elements']['edges']:
		source = xx['data']['source']
		target = xx['data']['target']
		iid = source+target
		xx['data'].update({'id':iid})
		

	with open(outfileName, "w") as outfile:
		json.dump(jsonGrpah, outfile)

