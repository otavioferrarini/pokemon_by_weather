from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import WeatherForm
import requests
import random
import os

def home(request):
	wform = WeatherForm()
	return render(request, 'pokeweather/home.html', {
		'wform': wform,
		})

def byweather(request):
	wform = WeatherForm()
	#tenta pegar a cidade no GET do link e acessar a OpenWeatherAPI com a cidade, se falhar, a pagina é redirecionada para o /pokeweather/
	try:
		city = request.GET.get('cidade')
		wdados = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&appid=' + os.environ['APP_ID']).json()
		clima = wdados['weather'][0]['main']
	except KeyError:
		return HttpResponseRedirect('/pokeweather/') 

	temp = wdados['main']['temp']
	tipo = ''

	#checa a temperatura e o clima fornecido pela API e decide o tipo adequado para o pokémon
	if clima == 'Rain':
		tipo = 'electric'
		clima = ''
	elif temp < 5:
		tipo = 'ice'
	elif temp >= 5 and temp < 10:
		tipo = 'water'
	elif temp >= 12 and temp < 15:
		tipo = 'grass'
	elif temp >= 15 and temp < 21:
		tipo = 'ground'
	elif temp >= 23 and temp < 27:
		tipo = 'bug'
	elif temp >= 27 and temp <= 33:
		tipo = 'rock'
	elif temp > 33:
		tipo = 'fire'
	else: tipo = 'normal'

	pdados = requests.get('https://pokeapi.co/api/v2/type/' + tipo).json()
	maxsize = len(pdados['pokemon']) - 1
	rndm = random.randint(0, maxsize)

	#checa se o valor aleatório do pokémon é igual ao do último, definido pelo cookie
	try:
		while request.session.get('consec') == rndm:
		 	rndm = random.randint(0, maxsize)
	except KeyError:
		pass
		
	#coloca um cookie para impedir que o pokémon seja repetido
	request.session.__setitem__('consec', rndm)
		
	pkmndados = requests.get(pdados['pokemon'][rndm]['pokemon']['url']).json()
		
	#tenta colocar o tipo secundário so pokémon, se existir
	try:
		tipo2 = pkmndados['types'][1]['type']['name']
	except IndexError:
		tipo2 = ''
		
	context = {
		'wform': wform,
		'city': city,
		'clima': clima,
		'temp': temp,
		'img': pkmndados['sprites']['other']['official-artwork']['front_default'],
		'tipo': tipo,
		'tipo2': tipo2,
		'pokemon': pdados['pokemon'][rndm]['pokemon']['name'],
	}

	return render(request, 'pokeweather/byweather.html', context)
