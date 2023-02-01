import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy as sp
from app.lib.parser import fromNetxToCyTo

import configparser


mpl.use('Agg')




def drawGraph(G,outputFileName,pos,config,catColor=False,saveFig=True,show=False,fontSize=5,nodeSize=400):

	categories		= 	config['GRAPH']['categories'].split(',')
	categoryColors	=	config['GRAPH']['categoryColors'].split(',')


	fromNetxToCyTo(G,outputFileName.split('.')[0]+'.json',pos)
	
	plt.figure(figsize=(21,30), frameon=False)

	options = {
		"font_size": fontSize,
		"node_size": nodeSize,
		"node_color": "white",
		"edgecolors": "black",
		"linewidths": 1,
		"width": 1
	}
	
	
	nx.draw_networkx(G, pos, **options)
	
	#Draw weight
	#da decommentare quando non testi sui grafi random

	#labels = nx.get_edge_attributes(G,'weight')
	#nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

	
	
	#DRAW COMPUTATION ATTR
	pos_attrs = {}
	for node, coords in pos.items():
		if 'S' in node:
			pos_attrs[node] = (coords[0]+ 1, coords[1])

	#da decommentare quando non testi sui grafi random
	#node_labels = nx.get_node_attributes(G,'computation')
	#nx.draw_networkx_labels(G, pos_attrs, labels = node_labels, font_color='brown')




	if catColor:
		coloredNode = [[],[],[],[]]
		dictNodeCat	=	nx.get_node_attributes(G, 'category')
		for node in dictNodeCat:
			for category in categories:
				if category == dictNodeCat[node]:
					index	=	categories.index(category)
					coloredNode[index].append(node)
					
		#da decommentare quando non testi sui grafi random
		#nx.draw_networkx_nodes(G, pos, nodelist=coloredNode[0], node_color="tab:blue")
		#nx.draw_networkx_nodes(G, pos, nodelist=coloredNode[1], node_color="tab:red")
		#nx.draw_networkx_nodes(G, pos, nodelist=coloredNode[2], node_color="tab:green")
		#nx.draw_networkx_nodes(G, pos, nodelist=coloredNode[3], node_color="tab:gray")
		labels = {n: n for n in G if 'M' in n}
		#nx.draw_networkx_labels(G, pos, labels,font_color="white",font_size=fontSize)





	# Set margins for the axes so that nodes aren't clipped
	ax = plt.gca()
	ax.margins()

	plt.axis("off")
	
	if saveFig:
		plt.savefig(outputFileName)
	
	if show:
		plt.show()