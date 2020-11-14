from flask import Flask, render_template, jsonify, url_for
from os import path
import webview
import requests
import pokepy
import json

app = Flask(__name__)
api = pokepy.V2Client()


@app.route('/')
def index():
    types = ['Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 'Poison',
             'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy']
    if path.exists('pokédex.json'):
        with open('pokédex.json', 'r+') as pokédex:
            context = json.load(pokédex)
    else:
        context = pokedex().get_json()
        with open('pokédex.json', 'w+') as pokédex:
            json.dump(context, pokédex)
    return render_template('index.html', context=context, types=types)


@app.route('/pokemon/<name>')
def pokémon(name):
    artwork = f'https://img.pokemondb.net/artwork/{name}.jpg'
    return render_template('pic.html', url=artwork)


@app.route('/pokedex')
def pokedex():
    species_endpoint = 'https://pokeapi.co/api/v2/pokemon-species?limit=893'
    context = []
    response = requests.get(species_endpoint)
    species_list = [object['name'] for object in response.json()['results']]
    for species in species_list:
        print(species)
        default_form = api.get_pokemon_species(species).varieties[0].pokemon.name
        data = api.get_pokemon(default_form)
        species_dict = {
            'name': species.capitalize(),
            'artwork': f'https://img.pokemondb.net/artwork/{species}.jpg',
            'types': [type_resource.type.name for type_resource in data.types],
            'id': '{:0>3}'.format(data.id)
        }
        context.append(species_dict)
    with open('pokédex.json', 'w+') as pokédex:
        json.dump(context, pokédex)
    return jsonify(context)


if __name__ == "__main__":
    app.run()

