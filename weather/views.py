import requests
from django.shortcuts import render

def index (request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=37c7a38b3f7634ee184f6bc7aa41d329'
	city = 'London'

	r = requests.get(url.format(city)).json()
	

	city_weather = {

		'city' : city,
		'lat': r['coord']['lat'],
		'lon': r['coord']['lon'],
		'temperature' : r['main']['temp'],
		'pressures' : r['main']['pressure'],
		'humidity' : r['main']['humidity'],
		'temperature_min' : r['main']['temp_min'],
		'temperature_max' : r['main']['temp_max'],
		'description' : r['weather'][0]['description'] ,
		'icon' : r['weather'][0]['icon'] ,
	}

	print (city_weather)
	context = {'city_weather' : city_weather}

	return render(request, 'weather/weather.html', context)