from flask import Flask
from flask import render_template
from markupsafe import escape
import os

projectPath = 'static/projects/'
	
listOfProject = [name for name in os.listdir(projectPath) if os.path.isdir(projectPath+name)]

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html',listOfProject=listOfProject)

@app.route("/project/<projectName>")
def get_project(projectName):

	projectName = escape(projectName)
	projectNameFile = 'projects/'+projectName+'/'+projectName+'_main_graph.json'
	project = projectPath+projectName

	if os.path.isdir(project):
		return render_template('project.html',listOfProject=listOfProject,projectName=projectName, projectNameFile=projectNameFile)
	else:
		return render_template('404.html',listOfProject=listOfProject)