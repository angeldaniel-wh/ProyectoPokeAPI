from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
import requests
from django.utils.autoreload import ensure_echo_on

from .requestsPokemon import *

# Vista index
def index(request : HttpRequest) -> HttpResponse:
    limit = request.GET.get('limit', 6)
    offset = request.GET.get('offset', 0)

    context = get_pokemon_list_with_images(limit= limit, offset= offset)

    pokemones = context['pokemon_list']
    if context['url_next']:
        url_next = context['url_next'].split('/')[-1]
    else:
        url_next = None

    if context['url_previous']:
        url_previous = context['url_previous'].split('/')[-1]
    else:
        url_previous = None

    return render(request, 'index.html', {'pokemones': pokemones, 'url_next': url_next, 'url_previous': url_previous})

def pokemon_info_name(request : HttpRequest) -> HttpResponse:
    name_pokemon = request.GET.get('pokemon', '').strip()

    if not name_pokemon:
        return render(request, 'index.html', {'error': 'NO hay pokemones'})

    pokemon = get_pokemon_info(name_pokemon= name_pokemon)
    print(pokemon)
    pokemon_context = {}

    if 'name' in pokemon:
        pokemon_context.update({
            'name': pokemon['name'],
            'id': pokemon['id'],
            'imagen': pokemon['sprites']['front_default'],
            'peso': pokemon['weight'],
            'altura': pokemon['height'],
            'types': pokemon['types'],
            'habilidades': pokemon['abilities'],
            'movimientos': pokemon['moves']
            }
        )
        for i in range(len(pokemon['types'])):
            pokemon['types'][i]['type']['id_type'] = pokemon['types'][i]['type']['url'].split('/')[-2]
    else:
        pokemon_context.update({})

    return render(request, 'poke_info.html', {'pokemon': pokemon_context})

def pokemon_info(request : HttpRequest, id_pokemon : int) -> HttpResponse:
    pokemon = get_pokemon_info(id_pokemon)

    pokemon_context = {}

    pokemon_context.update({
        'name': pokemon['name'],
        'id': pokemon['id'],
        'imagen': pokemon['sprites']['front_default'],
        'peso': pokemon['weight'],
        'altura': pokemon['height'],
        'types': pokemon['types'],
        'habilidades': pokemon['abilities'],
        'movimientos': pokemon['moves']
        }
    )

    for i in range(len(pokemon['types'])):
        pokemon['types'][i]['type']['id_type'] = pokemon['types'][i]['type']['url'].split('/')[-2]

    return render(request, 'poke_info.html', {'pokemon': pokemon_context})

def pokemon_types(request : HttpRequest, id_type : int) -> HttpResponse:
    end = int(request.GET.get('end', 6))
    start = int(request.GET.get('start', 0))
    url_next = f'?start={end}&end={end + 6}'
    url_previous = f'?start={start - 6}&end={start}'

    pokemones = get_pokemon_list_with_images(limit=end, offset=start, id_type=id_type)
    return render(request, 'index.html', {'pokemones': pokemones, 'url_next': url_next, 'url_previous': url_previous})