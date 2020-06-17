from flask import Flask, request, render_template, Markup
from flask_cors import CORS
from pipeline import Pipeline
from configuration import cfg



app = Flask(__name__)
CORS(app)

pipeline = Pipeline(cfg)


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    """Simple UI to test server"""
    if request.method == 'POST':
        text = request.form.get('text')
        dep = request.form.get('dep')
        visu = pipeline(text, format='html')
        if dep:
            return render_template('demo.html', ent=Markup(visu[0]), dep=Markup(visu[1]))
        return render_template('demo.html', ent=Markup(visu[0]))
    return render_template('demo.html')


@app.route('/debug', methods=['GET', 'POST'])
def debug():
    if request.method == 'POST':
        text = request.form.get('text')
        doc = pipeline(text, format='json')
        return doc
    return render_template('debug.html')


@app.route('/', methods=['POST'])
def process():
    """TODO : should run pipeline on value `text` in input JSON, and return doc JSON."""
    text = request.json.get('text')
    return pipeline(text, format='json')


@app.route('/config', methods=['GET'])
def get_config():
    """TODO : pipeline configuration should be readable"""
    return
