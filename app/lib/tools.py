import networkx as nx
			

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


