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
	path="../views/test_tpl.html"
	css_url = url_for('static', filename='css/style.css')
	print(css_url + "           hieoieoeh")
	js_url = url_for('static', filename='js/main.js')
	context= { "title" : "Test Example", "description" : "First test of jinja2.", "results": results, "css_url": css_url, "js_url": js_url }
	outputText = render(path, context)
	return outputText

if __name__== "__main__":
	app.run(debug=True)