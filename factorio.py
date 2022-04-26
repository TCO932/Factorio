from collections import Counter
import json
from pprint import pprint

def getRecipes():
    with open('crafts.json') as json_file:
        recipes = json.load(json_file)
    return dict(recipes)
def getSpeeds():
    with open('speeds.json') as json_file:
        speeds = json.load(json_file)
    return dict(speeds)

recipes = getRecipes()
speeds = getSpeeds()

def getRecipes():
    with open('crafts.json') as json_file:
        recipes = json.load(json_file)
    return recipes

def getFactoryCount(item_name):
    full_recipe = dict(getResources(item_name))

    for item_name in full_recipe.keys():
        if (recipes[item_name]["elementary"] == True): continue
        production_speed = recipes[item_name]["quantity"] / recipes[item_name][
            "production_time"]
        full_recipe[item_name] /= production_speed

    return full_recipe


def multResources(full_recipe, amount):
    for key in full_recipe.keys():
        full_recipe[key] *= amount
    return full_recipe


def getResources(item_name):
    if (recipes[item_name]["elementary"] == True): return Counter()
    # Добавляем начальный крафт
    full_recipe = Counter(recipes[item_name]["recipe"])

    # Проходим по компонентам крафта
    for item, amount in recipes[item_name]["recipe"].items():
        recipe = getResources(item)
        for key in recipe.keys():
            # Умножаем на необходимое число для крафта
            recipe[key] *= amount
        full_recipe += recipe

    for item in full_recipe.keys():
        full_recipe[item] /= recipes[item_name]["quantity"]

    return full_recipe

# item_name - name of desired item
# speed = amount per sec
# assembling_machine - type of machine, 
# productivity - True means it uses assembling machine with full slots of productivity 3 module
def getDetailedcraft(item_name, speed, assembling_machine, productivity = False):
    if (recipes[item_name]["elementary"] == True): return []

    asm_mach = speeds["assembling-machines"][assembling_machine]
    asm_mach_speed = asm_mach["speed"]

    # productivity module 3 speed and production impact
    if (productivity == True):
        prod3_speed_impact = asm_mach_speed * asm_mach["slots"] * speeds["modules"]["productivity-module-3"]["speed"]
        asm_mach_speed += prod3_speed_impact

        prod3_prod_impact = asm_mach_speed * asm_mach["slots"] * speeds["modules"]["productivity-module-3"]["productivity"]
        asm_mach_speed += prod3_prod_impact

    craft_speed = recipes[item_name]["quantity"] / recipes[item_name]["production_time"] * asm_mach_speed 

    craft = {
        "item_name": item_name, 
        "speed": speed, 
        "assembling_machine_amount": 
            # количество предметов в сек / скорость завода = количество заводов
            speed / craft_speed
    }
    craft["componets"] = []

    # running throught item components
    for item, amount in recipes[item_name]["recipe"].items():
        craft["componets"].append({
            item: speed * (amount if productivity == False else amount / (1 + asm_mach["slots"] * speeds["modules"]["productivity-module-3"]["productivity"]))
        })
    return craft
# item = "war_science"
# science = dict(getResources(item))
# pprint(science)
# s = getFactoryCount(item)
# pprint(s)
