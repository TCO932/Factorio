from flask import Flask, request, render_template_string
from threading import Thread
from factorio import getResources, getFactoryCount, getRecipes, getDetailedcraft
# http://10.1.1.1:5000/login?username=alex&password=pw1

app = Flask('')

@app.route('/')
def home():
    return render_template_string('hello')

@app.route('/recipes')
def getRec():
    return getRecipes()

@app.route('/resources')
def getRes():
    item_name = request.args.get('item')
    if (item_name is None): return "Item Name is undefined"
    return getResources(item_name)

@app.route('/factory')
def getFac():
    item_name = request.args.get('item')
    if (item_name is None): return "Item Name is undefined"
    return getFactoryCount(item_name)

@app.route('/detailedCraft')
def detailedCraft():
    item_name = request.args.get('item')
    speed = request.args.get('speed')
    assembling_machine = request.args.get('assembling_machine')
    productivity = request.args.get('productivity')
    
    if (item_name is None): return "Item Name is undefined"
        
    return getDetailedcraft(item_name, speed, assembling_machine, productivity)

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()