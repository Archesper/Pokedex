from flask import Flask, render_template, jsonify, url_for
from os import path
import webview, requests, pokepy, json

app = Flask(__name__)
api = pokepy.V2Client()

@app.route('/')
def index():
    if path.exists('pokédex.json'):
        with open('pokédex.json', 'r+') as pokédex:
            context = json.load(pokédex)
    else:
        context = requests.get('http://127.0.0.1:5000/pokedex').json()
        with open('pokédex.json', 'w+') as pokédex:
            json.dump(context, pokédex)
    return render_template('index.html', context=context)

@app.route('/pokemon/<name>')
def pokémon(name):
    artwork = f'https://img.pokemondb.net/artwork/{name}.jpg'
    return render_template('pic.html', url=artwork)

@app.route('/pokedex')
def pokedex():
    species_endpoint = 'https://pokeapi.co/api/v2/pokemon-species?limit=251'
    context = []
    response = requests.get(species_endpoint)
    species_list = [object['name'] for object in response.json()['results']]
    for species in species_list:
        data = api.get_pokemon(species)
        species_dict = {
            'name' : species.capitalize(),
            'artwork': f'https://img.pokemondb.net/artwork/{species}.jpg',
            'types' : [type_resource.type.name.capitalize() for type_resource in data.types],
            'id' : '{:0>3}'.format(data.id)
        }
        context.append(species_dict)
    with open('pokédex.json', 'w+') as pokédex:
        json.dump(context, pokédex)
    return jsonify(context)

if __name__ == "__main__":
    """webview.create_window('Pokédex', app, width=1200, height=600, resizable=False)
    webview.start()"""
    app.run()
    