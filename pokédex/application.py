from flask import Flask, render_template, jsonify, url_for
from os import path
import webview
import requests
import pokepy
import json
import utilities
import random
from sys import argv


app = Flask(__name__)
api = pokepy.V2Client()


@app.route('/')
def index():
    types = ['Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 'Poison',
             'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy']
    if path.exists('pokedex.json'):
        with open('pokedex.json', 'r+') as pokedex:
            context = json.load(pokedex)
    else:
        context = pokedex().get_json()
        with open('pokedex.json', 'w+') as pokedex:
            json.dump(context, pokedex)
    return render_template('index.html', context=context, types=types)


@app.route('/pokemon/<name>')
def pokemon(name):
    data = utilities.pokemon_data(name, api)
    return render_template('pokemon.html', forms=data)


@app.route('/pokedex')
def pokedex():
    species_endpoint = 'https://pokeapi.co/api/v2/pokemon-species?limit=893'
    context = []
    response = requests.get(species_endpoint)
    species_list = [object['name'] for object in response.json()['results']]
    for species in species_list:
        default_form = api.get_pokemon_species(
            species).varieties[0].pokemon.name
        data = api.get_pokemon(default_form)
        species_dict = {
            'name': species.capitalize(),
            'artwork': f'https://img.pokemondb.net/artwork/{default_form}.jpg',
            'types': [type_resource.type.name for type_resource in data.types],
            'id': '{:0>3}'.format(data.id)
        }
        context.append(species_dict)
    with open('pokedex.json', 'w+') as pokedex:
        json.dump(context, pokedex)
    return jsonify(context)


def test():
    return 'rgb(255,200,4)'


if __name__ == "__main__":
    if argv[1] == 'web':
        webview.create_window('Pokédex', app, fullscreen=True, resizable=False)
        webview.start()
    elif argv[1] == 'browser':
        app.run()
