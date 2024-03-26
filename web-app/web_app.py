from flask import Flask
from flask import render_template
from flask import request
from markupsafe import escape
import os

import sys
sys.path.insert(0, '..')

from app.api import MGM

projectPath = 'static/projects/'
	
listOfProject = [name for name in os.listdir(projectPath) if os.path.isdir(projectPath+name)]


app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html',listOfProject=listOfProject)

@app.route("/project/<projectName>" , methods = ['GET', 'POST'])
def get_project(projectName):
	results = {}
	projectName = escape(projectName)
	mgm = MGM('static/projects/'+projectName+'/config.ini')

	projectNameFile = 'projects/'+projectName+'/output/'+projectName+'-CORRECT.json'
	project = projectPath+projectName
	f = None
	f = request.args.get('f')

	if request.method == 'GET':
		if os.path.isdir(project) and f == None:
			return render_template('project.html',
			listOfProject=listOfProject,
			projectName=projectName, 
			projectNameFile=projectNameFile,
			results = results,
			func='main'
			)
	if request.method == 'POST':
		results = {}
		data = request.json
		s = 0
		nodeM = [x for x in data if 'M' in x]
		if nodeM == []:
			nodeM = [x for x in mgm.G_c.nodes() if 'M' in x]
		nodeC = [x for x in data if 'C' in x]
		if nodeC == []:
			nodeC = [x for x in mgm.G_c.nodes() if 'C' in x]
		nodeI = [x for x in data if 'I' in x]
		if nodeI == []:
			nodeI = [x for x in mgm.G_c.nodes() if 'I' in x]
		else:
			s=1
		nodeS = [x for x in data if 'S' in x]
		if nodeS == []:
			nodeS = [x for x in mgm.G_c.nodes() if 'S' in x]
		else:
			s=2

		func  = data[-1]
		outputFile = 'projects/'+projectName+'/output/'+projectName+'-minSetCov-'+func+'_COVERED.json'
		if func == 'id1':
			G = mgm.G_c.subgraph(nodeM+nodeC+nodeI+nodeS)
			if s==1:
				results = mgm.minSetCoverByInputOut(mgm.G_c,nodeI,func)
			elif s==2:
				results = mgm.minSetCoverBySourceOut(mgm.G_c,nodeS,func)
			else:
				results = mgm.minSetCoverOut(G,func)
			results['func'] = func
			results['output'] = outputFile

		if func == 'id2':
			outputFile = 'projects/'+projectName+'/output/'+projectName+'-minCapacitySetCover-'+func+'_COVERED.json'
			results = mgm.minCapacitySetCoverOut(mgm.G_c,func)
			
			results['func'] = func
			results['output'] = outputFile
		
		if func == 'id3':
			outputFile = 'projects/'+projectName+'/output/'+projectName+'-fixedCostAllMetrics-'+func+'_COVERED.json'
			
			check = data[-3]
			if check == 'on':
				maxvalue = int(data[-2])

				results = mgm.maxSetCovByAttributeOnEdgev2(mgm.G_c,maxvalue,func)
				results['func'] = func
				results['output'] = outputFile
			else:
				results = 'ok'


		return results
	
if __name__ == '__main__':
	app.run(debug=True, port=5000)