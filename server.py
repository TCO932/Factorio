from flask import Flask, request, render_template_string
from threading import Thread
from factorio import getResources, getFactoryCount, getRecipes
# http://10.1.1.1:5000/login?username=alex&password=pw1

app = Flask('')

@app.route('/')
def home():
    return render_template_string('hello')

@app.route('/recipes')
def getRec():
    recipes = getRecipes()
    
    html = '<table><tr><td>Item</td><td>Amount</td></tr>'
    for key, val in recipes.items():
        html += f'<tr><td>{key}</td><td>{val}</td></tr>'
    html += '</table>'
    return render_template_string(html)

@app.route('/resources')
def getRes():
    item_name = request.args.get('item')
    if (item_name is None): return "Item Name is undefined"
    resources = getResources(item_name)
    
    html = '<table><tr><td>Item</td><td>Amount</td></tr>'
    for key, val in resources.items():
        html += f'<tr><td>{key}</td><td>{val}</td></tr>'
    html += '</table>'
    return render_template_string(html)

@app.route('/factory')
def getFac():
    item_name = request.args.get('item')
    if (item_name is None): return "Item Name is undefined"
    factories = getFactoryCount(item_name)
    
    html = '<table><tr><td>Item</td><td>Assembling machine amount</td></tr>'
    for key, val in factories.items():
        html += f'<tr><td>{key}</td><td>{val}</td></tr>'
    html += '</table>'
    return render_template_string(html)

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()