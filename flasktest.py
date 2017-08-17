from flask import Flask, url_for
import jinja2 
import os

def get_db():
    from pymongo import MongoClient
    client = MongoClient('mongodb://fftcgscript:nextat765@ds161022.mlab.com:61022/fftcg')
    db = client.fftcg
    return db
def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

app = Flask(__name__)

@app.route('/')
def index():
	db=get_db()
	results=db.cards.find()

	db.close

	
	bsc_url = url_for('static', filename='css/bootstrap.min.css')
	css_url = url_for('static', filename='css/style.css')
	bsj_url = url_for('static', filename='js/jbootstrap.min.js')
	jquery_url = url_for('static', filename='js/jquery-3.2.1.min.js')
	js_url = url_for('static', filename='js/main.js')
	image_path =url_for('static', filename='images/')
	print(image_path)
	path="views/test_tpl.html"
	context= { "title" : "FFTCG Price Search", "description" : "FFTCG Price Search.", "results": results, "css_url":css_url, "bsc_url": bsc_url, "js_url": js_url, "jquery_url":jquery_url, "bsj_url": bsj_url,  "image_path":image_path}
	outputText = render(path, context)
	return outputText

if __name__== "__main__":
	app.run(debug=True)