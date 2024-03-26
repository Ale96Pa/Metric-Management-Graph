import configparser
import time
import os
import networkx as nx
import pickle

from app.lib.convertXlsToCSV import convertXlsToCSV

from app.lib.parser import getGraphFromCSV

from app.lib.tools import genPosNodes
from app.lib.tools import makeSubGraphByMetrics
from app.lib.tools import makeCategorySubGraph

from app.lib.draw import drawGraph

from app.lib.minSetCover import correctnessMGM
from app.lib.minSetCover import MGMminSetCover
from app.lib.minSetCover import minSetCovByINPUT
from app.lib.minSetCover import minSetCovBySOURCE
from app.lib.minSetCover import maxSetCovByATTR
from app.lib.minSetCover import maxSetCovByATTRv2
from app.lib.minSetCover import minCapacitySetCover
from app.lib.minSetCover import maxSetCovByATTRv3


class MGM():
	def __init__(self,config,state=0):
		try:
			self.config = configparser.ConfigParser()
			self.config.read(config)
			self.projectPath    =   self.config['PROJECT']['projectPath']
			self.projectName	=	self.config['PROJECT']['projectName']
			self.pathDbFiles    =   self.projectPath+self.config['DB']['pathDbFiles']
			self.xlsDbPathFile	=	self.pathDbFiles+self.config['DB']['xlsFileName']
			self.sheetNames		=	self.config['DB']['sheetsName'].split(',')
			self.outputPath 	=	self.projectPath+'output/'
			self.pikle			=	self.projectPath+self.projectName+".gpickle"

			if os.path.isfile(self.pikle) and state==0:
				print('EXIST PIKLE')
				with open(self.pikle, 'rb') as f:
					self.G_c = pickle.load(f)

				self.delta			=	[int(x) for x in self.config['GRAPH']['delta'].split(',')]
				self.position		=	[int(x) for x in self.config['GRAPH']['position'].split(',')]
				self.postionOfNodes	=	self.genPosNodes(self.G_c)

				os.makedirs(self.outputPath, exist_ok = True)


			else:
				print('start initialization')

				#Tested and ok
				self.generateCsvFromDB()

				self.fileNodes		=	[self.pathDbFiles+a for a in self.config['GRAPH']['nodeNames'].split(',')]
				self.fileEdges		=	[self.pathDbFiles+a for a in self.config['GRAPH']['edgeNames'].split(',')]
				self.fileGraphName	=	self.projectPath+self.projectName+'.graphml'
				
				#Tested and ok
				self.G = self.getGraphFromCSV()

				#Gen pos of nodes
				self.delta			=	[int(x) for x in self.config['GRAPH']['delta'].split(',')]
				self.position		=	[int(x) for x in self.config['GRAPH']['position'].split(',')]
				self.postionOfNodes	=	self.genPosNodes(self.G)

				
				os.makedirs(self.outputPath, exist_ok = True)

				
				self.outputFigGraph	=	self.outputPath+self.projectName+'-Main_Color.pdf'
				drawGraph(self.G, self.outputFigGraph, self.postionOfNodes, self.config, catColor=True)

				self.G_c	=	self.correctnessMGM(self.G,self.outputPath+self.projectName+'-CORRECT.pdf')

				nx.write_gpickle(self.G_c, self.projectPath+self.projectName+".gpickle")

		except Exception as e:
			print(e)
			return None
	
	def generateCsvFromDB(self):
		try:
			convertXlsToCSV(self.sheetNames,self.xlsDbPathFile,self.pathDbFiles)
			return '200'
		except Exception as e:
			print(e)
			return 'error'
	
	
	def getGraphFromCSV(self):
		try:
			return getGraphFromCSV(self.fileNodes,self.fileEdges,self.fileGraphName)
		except Exception as e:
			print(e)
			return 'error'

	def genPosNodes(self,G):
		try:
			return genPosNodes(G, self.delta, self.position)
		except Exception as e:
			print(e)
			return 'error'
	
	def correctnessMGM(self,G,outputFile):
		try:
			return correctnessMGM(G, outputFile,self.postionOfNodes,self.config)
		except Exception as e:
			print(e)
			return 'error'

	def minSetCover(self,G):
		try:
			return MGMminSetCover(G, self.outputPath+self.projectName+'-minSetCov.pdf',self.postionOfNodes,self.config)
		except Exception as e:
			print(e)
			return 'error'

	def minSetCoverOut(self,G,output):
		try:
			output = self.outputPath+self.projectName+'-minSetCov-'+output+'.pdf'
			return MGMminSetCover(G, output,self.postionOfNodes,self.config)
		except Exception as e:
			print(e)
		return 'error'
	
	def minSetCoverByMetric(self,G,metrics):
		try:
			subGraph    =   self.correctnessMGM(makeSubGraphByMetrics(G,metrics), self.outputPath+self.projectName+'-minSetCovByMetric.pdf')
			return MGMminSetCover(subGraph, self.outputPath+self.projectName+'-minSetCovByMetric.pdf',self.postionOfNodes,self.config)
		except Exception as e:
			print(e)
			return 'error'
	
	def minSetCoverByCategory(self,G,category):
		try:
			subGraph    =   self.correctnessMGM(makeCategorySubGraph(G,category), self.outputPath+self.projectName+'-minSetCovByCategory.pdf')
			return MGMminSetCover(subGraph, self.outputPath+self.projectName+'-minSetCovByCategory.pdf',self.postionOfNodes,self.config)
		except Exception as e:
			print(e)
			return 'error'
	
	def minSetCoverByInput(self,G,inputs):
		try:
			minSetCovByINPUT(G, inputs, self.outputPath+self.projectName+'-minSetCovByInputs.pdf',self.postionOfNodes,self.config)
			return 'ok'
		except Exception as e:
			print(e)
			return 'error'
	def minSetCoverByInputOut(self,G,inputs,output):
		try:
			output = self.outputPath+self.projectName+'-minSetCov-'+output+'.pdf'
			return minSetCovByINPUT(G, inputs, output,self.postionOfNodes,self.config)
		except Exception as e:
			print(e)
			return 'error'

	def minSetCoverBySource(self,G,sources):
		try:
			minSetCovBySOURCE(G, sources, self.outputPath+self.projectName+'-minSetCovBySources.pdf',self.postionOfNodes,self.config)
			return 'ok'
		except Exception as e:
			print(e)
			return 'error'
	def minSetCoverBySourceOut(self,G,sources,output):
		try:
			output = self.outputPath+self.projectName+'-minSetCov-'+output+'.pdf'
			return minSetCovBySOURCE(G, sources, output,self.postionOfNodes,self.config)
		except Exception as e:
			print(e)
			return 'error'
	
	def maxSetCovByAttributeOnEdge(self,G,maxValue,attr='weight'):
		try:
			maxSetCovByATTR(G,self.outputPath+self.projectName+'-minSetCovByAttributeOnEdge.pdf',maxValue,attr,self.postionOfNodes,self.config)
			return 'ok'
		except Exception as e:
			print(e)
			return 'error'

	def maxSetCovByAttributeOnEdgev2(self,G,maxValue,output):
		try:
			output = self.outputPath+self.projectName+'-fixedCostAllMetrics-'+output+'.pdf'
			
			return maxSetCovByATTRv3(G,maxValue,output,self.postionOfNodes,self.config)
		except Exception as e:
			print(e)
			return 'error'
	def maxSetCovByAttributeOnEdgeOut(self,G,maxValue,output,attr='weight'):
		try:
			output = self.outputPath+self.projectName+'-minSetCovByAttributeOnEdge-'+output+'.pdf'
			return maxSetCovByATTR(G,output,maxValue,attr,self.postionOfNodes,self.config)
		except Exception as e:
			print(e)
			return 'error'
	
	def minCapacitySetCover(self,G):
		try:
			minCapacitySetCover(G,self.outputPath+self.projectName+'-minCapacitySetCover.pdf',self.postionOfNodes,self.config)
			return 'ok'
		except Exception as e:
			print(e)
			return 'error'
	def minCapacitySetCoverOut(self,G, output):
		try:
			output = self.outputPath+self.projectName+'-minCapacitySetCover-'+output+'.pdf'
			print(output)
			return minCapacitySetCover(G,output,self.postionOfNodes,self.config)
		except Exception as e:
			print(e)
			return 'error'