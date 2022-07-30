import csv
from collections import OrderedDict

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy as sp

from lib.position import pos 



#prima genero l'xml, poi il posizionamento per disegnare e poi lo istanzio

def genXmlGraph(fileNodes,fileEdges,fileGraphName):
	f = open(fileGraphName, "w")
	f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns"\n')
	f.write('\t\txmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
	f.write('\t\txsi:schemaLocation="http://graphml.graphdrawing.org/xmlns\n')
	f.write('\t\thttp://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
	f.write('\t<key id="d1" for="edge" attr.name="weight" attr.type="int"/>\n')
	f.write('\t<graph id="G" edgedefault="directed">\n')

	print('Start - from CSV to xml NODES')
	for file in fileNodes:
		demolist = []
		with open(file, 'r') as db:
			csvreader = csv.reader(db)
			
			for row in csvreader:
				print(row[0])
				demolist.append(row[0])

			demoFinalList = OrderedDict.fromkeys(demolist)
			

			for el in demoFinalList:
				print(el)
				node = '\t\t<node id="{}"/>\n'.format(el)
				f.write(node)

	print('END - from CSV to xml NODES')
	print('Start - from CSV to xml EDGES')
	for file in fileEdges:
		demolist = []
		with open(file, 'r') as db:
			csvreader = csv.reader(db)

			for row in csvreader:
				print(row[0],row[1])
				if 'LINK_MT_CL.csv' in file:
					edge = '\t\t<edge source="{}" target="{}"/>\n'.format(row[1],row[0])
				else:
					edge = '\t\t<edge source="{}" target="{}"/>\n'.format(row[0],row[1])
					if 'LINK_IN_SRC.csv' in file:
						edge = '\t\t<edge source="{}" target="{}"><data key="d1">{}</data></edge>\n'.format(row[0],row[1],row[2])

				
				f.write(edge)

			
	f.write('\t</graph>\n')
	f.write('\t</graphml>\n')

	f.close()
	print('END - from CSV to xml EDGES')


def genPosNodes(fileNodes,delta,pos,filePosName):
	print('Start the positioning of nodes according to AS algo')
	f = open(filePosName, "w")
	f.write('pos = {\n')
	for file in fileNodes:
		demolist = []
		with open(file, 'r') as db:
			csvreader = csv.reader(db)
			
			for row in csvreader:
				#print(row[0])
				demolist.append(row[0])

			demoFinalList = OrderedDict.fromkeys(demolist)
			
			i = 1
			demoFinalList = list(demoFinalList)

			for el in demoFinalList:
				aaaa=str((i*4)+((i-1)*delta[0]))
				posizione="'{}': ({}, {}),\n".format(str(el),str(pos[0]),aaaa)
				if 'SOURCES.csv' in file and el == demoFinalList[-1]:
					posizione="'{}': ({}, {})\n}}".format(str(el),str(pos[0]),aaaa)
				print(posizione)
				f.write(posizione)

				i+=1
			delta.pop(0)
			pos.pop(0)


	#f.write("'NULLO': (55, 210)\n}")
	f.close()
	print('END - the positioning of nodes')


def drawGraph(graph,outputFileName,saveFig=True,fontSize=5,nodeSize=400):
	plt.figure(figsize=(21,30), frameon=False)

	options = {
		"font_size": fontSize,
		"node_size": nodeSize,
		"node_color": "white",
		"edgecolors": "black",
		"linewidths": 1,
		"width": 1
	}
	
	nx.draw_networkx(graph, pos, **options)
	
	labels = nx.get_edge_attributes(graph,'weight')
	nx.draw_networkx_edge_labels(graph,pos,edge_labels=labels)

	# Set margins for the axes so that nodes aren't clipped
	ax = plt.gca()
	ax.margins()

	plt.axis("off")
	if saveFig:
		plt.savefig(outputFileName)
	plt.show()

