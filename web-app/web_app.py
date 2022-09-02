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

@app.route("/project/<projectName>")
def get_project(projectName):

	projectName = escape(projectName)
	mgm = MGM('static/projects/'+projectName+'/config.ini')

	projectNameFile = 'projects/'+projectName+'/output/'+projectName+'-CORRECT.json'
	project = projectPath+projectName
	f = None
	f = request.args.get('f')


	if os.path.isdir(project) and f == None:
		return render_template('project.html',
		listOfProject=listOfProject,
		projectName=projectName, 
		projectNameFile=projectNameFile,
		func='main'
		)
	elif f is not None:
		if f == 'id1':
			print('id1')
			mgm.minSetCover(mgm.G_c)
			projectNameFile = 'projects/'+projectName+'/output/'+projectName+'-minSetCov_COVERED.json'
			return render_template('project.html',
			listOfProject=listOfProject,
			projectName=projectName, 
			projectNameFile=projectNameFile,
			projectNameFileNew=projectNameFile,
			func='id1'
			)
		elif f=='id2':
			print('id2')
			capacity = int(request.args.get('c'))
			mgm.maxSetCovByAttributeOnEdge(mgm.G_c,capacity)
			projectNameFile = 'projects/'+projectName+'/output/'+projectName+'-minSetCov_COVERED.json'
			projectNameFileNew = 'projects/'+projectName+'/output/'+projectName+'-minSetCovByAttributeOnEdge_COVERED.json'
			return render_template('project.html',
			listOfProject=listOfProject,
			projectName=projectName, 
			projectNameFile=projectNameFile,
			projectNameFileNew=projectNameFileNew,
			func='id2'
			)
		elif f=='id3':
			print('id3')
			mgm.minCapacitySetCover(mgm.G_c)
			projectNameFile = 'projects/'+projectName+'/output/'+projectName+'-minSetCov_COVERED.json'
			projectNameFileNew = 'projects/'+projectName+'/output/'+projectName+'-minSetCovByAttributeOnEdge_COVERED.json'
			return render_template('project.html',
			listOfProject=listOfProject,
			projectName=projectName, 
			projectNameFile=projectNameFile,
			projectNameFileNew=projectNameFileNew,
			func='id3'
			)
		elif f=='minSetCovByMetric':
			print('minSetCovByMetric')
			projectNameFile = 'projects/'+projectName+'/output/'+projectName+'-minSetCov_COVERED.json'
			projectNameFileNew = 'projects/'+projectName+'/output/'+projectName+'-minCapacitySetCover_COVERED.json'
			return render_template('project.html',
			listOfProject=listOfProject,
			projectName=projectName, 
			projectNameFile=projectNameFile,
			projectNameFileNew=projectNameFileNew,
			func='minSetCovByMetric'
			)
			
	else:
		return render_template('404.html',listOfProject=listOfProject)