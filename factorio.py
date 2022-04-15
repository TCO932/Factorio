from collections import Counter
import json
from pprint import pprint

def getRecipes():
    with open('crafts.json') as json_file:
        recipes = json.load(json_file)
    return recipes

def getFactoryCount(item_name):
    with open('crafts.json') as json_file:
        recipes = json.load(json_file)

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
    with open('crafts.json') as json_file:
        recipes = json.load(json_file)
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


# item = "war_science"
# science = dict(getResources(item))
# pprint(science)
# s = getFactoryCount(item)
# pprint(s)
