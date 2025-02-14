from typing import Optional

import requests

base_url = 'https://pokeapi.co/api/v2'

def try_catch(endpoint: str, args: dict) -> dict:
    try:
        response = requests.get( endpoint, params=args)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

def get_pokemon_list_with_images( limit : int, offset: int, id_type: int = None) -> dict:

    url_next = None
    url_previous = None

    if id_type is None:
        response = get_pokemon_list(limit=limit, offset=offset)
        url_next = response['next']
        url_previous = response['previous']
        pokemon_list = response['results']
    else:
        pokemon_list = get_pokemon_type_list(limit=limit, offset=offset, id_type=id_type)

    if not 'error' in pokemon_list:
        for pokemon in pokemon_list:
            pokemon['image'] = get_pokemon_sprite(pokemon['url'])
            pokemon['id'] = pokemon['url'].split('/')[-2]

        if url_next or url_previous:
            return {'pokemon_list': pokemon_list, 'url_next': url_next, 'url_previous': url_previous}

        return pokemon_list

    return pokemon_list

def get_pokemon_list(limit: int, offset: int) -> dict:
    pokemon_list_endpoint = f'{base_url}/pokemon/?limit={limit}'
    args = {'offset': offset} if offset else {}

    response = try_catch(pokemon_list_endpoint, args)

    if 'error' in response:
        return {'error': response['error']}
    else:
        return response

def get_pokemon_sprite(pokemon_url: str ) -> dict:
    response = try_catch(pokemon_url, {})
    if 'error' in response:
        return {'error': response['error']}
    else:
        return response['sprites']['front_default']

def get_pokemon_info(id_pokemon: int = None, name_pokemon: int = None) -> dict:

    if name_pokemon is None:
        pokemon_url = f'{base_url}/pokemon/{id_pokemon}/'
        response = try_catch(pokemon_url, {})
    else:
        pokemon_url = f'{base_url}/pokemon/{name_pokemon}/'
        response = try_catch(pokemon_url, {})

    if 'error' in response:
        return {'error': response['error']}
    else:
        return response

def get_pokemon_type_list(offset: int, limit: int, id_type: int) -> list:
    pokemon_type_endpoint = f'{base_url}/type/{id_type}'

    response = try_catch(pokemon_type_endpoint, {})

    pokemon_list = []
    filtered_list = []
    if len(response['pokemon']) > 0:
        for pokemon in response['pokemon']:
            pokemon_list.append(pokemon['pokemon'])

        for i in range(offset, limit):
            filtered_list.append(pokemon_list[i])

    if 'error' in response:
        return {'error': response['error']}
    else:
        return filtered_list