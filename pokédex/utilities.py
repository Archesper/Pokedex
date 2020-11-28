from math import ceil


def custom_capitalize(string):
    words = string.split('-')
    capitalized_words = [word.capitalize() for word in words]
    capitalized_string = '-'.join(capitalized_words)
    return capitalized_string


def stat_repr(value):
    width = ceil(value*0.39)
    if value <= 40:
        color = '#ff0000'
    elif 40 < value <= 60:
        color = '#f21000'
    elif 60 < value <= 80:
        color = '#ff6600'
    elif 80 < value <= 110:
        color = '#fffe00'
    elif 100 < value <= 130:
        color = '#66ff00'
    elif 130 < value <= 160:
        color = '#02ff2a'
    elif 160 < value <= 180:
        color = '#02ffaa'
    else:
        color = '#02ffff'
    return (width, color)


def pretty_id(id):
    return '{:0>3}'.format(id)


def ev_gain(pokemon):
    evs = [
        f'{stat.effort} {custom_capitalize(stat.stat.name).replace("-", " ")}' for stat in pokemon.stats if stat.effort > 0]
    return ', '.join(evs)


def abilitiy_data(pokemon, api_wrapper):
    abilities = pokemon.abilities
    result = list()
    for ability in abilities:
        ability_ressources = api_wrapper.get_ability(ability.ability.name)
        if ability.is_hidden:
            ability_slot = 'Hidden Ability'
        else:
            ability_slot = ability.slot
        ability_description = ability_ressources.effect_entries[-1].short_effect
        result.append(
            {
                'name': custom_capitalize(ability.ability.name).replace('-', ' '),
                'slot': ability_slot,
                'description': ability_description,
            }
        )
    return result


def pokemon_data(pokemon, api_wrapper):
    data = list()
    species_ressources = api_wrapper.get_pokemon_species(pokemon)
    pokemon_varieties = [
        variety.pokemon.name for variety in species_ressources.varieties]
    for name in pokemon_varieties:
        pokemon_ressources = api_wrapper.get_pokemon(name)
        if pokemon_ressources.id > 1:
            previous_pokemon = custom_capitalize(
                api_wrapper.get_pokemon_species(species_ressources.id - 1).name)
        else:
            previous_pokemon = None
        try:
            next_pokemon = custom_capitalize(
                api_wrapper.get_pokemon_species(species_ressources.id + 1).name)
        except:
            next_pokemon = None
        species_dict = {
            'name': custom_capitalize(name),
            'artwork': f'https://img.pokemondb.net/artwork/{name}.jpg',
            'types': [type_resource.type.name for type_resource in pokemon_ressources.types],
            'id': pretty_id(species_ressources.id),
            'stats': [(stat.base_stat, stat_repr(stat.base_stat)[0], stat_repr(stat.base_stat)[1]) for stat in pokemon_ressources.stats],
            'next': (next_pokemon, pretty_id(species_ressources.id + 1)),
            'previous': (previous_pokemon, pretty_id(species_ressources.id - 1)),
            'sprite': pokemon_ressources.sprites.front_default,
            'height': "{:.2f}".format(pokemon_ressources.height*0.1),
            'weight': "{:.2f}".format(pokemon_ressources.weight*0.1),
            'species_title': species_ressources.genera[7].genus,
            'gen': species_ressources.generation.name.split('-')[1].upper(),
            'ev_yield': ev_gain(pokemon_ressources),
            'base_friendship': species_ressources.base_happiness,
            'base_exp': pokemon_ressources.base_experience,
            'catch_rate': species_ressources.capture_rate,
            'growth': custom_capitalize(species_ressources.growth_rate.name).replace('-', ' '),
            'abilities': abilitiy_data(pokemon_ressources, api_wrapper)

        }
        data.append(species_dict)
    return data
