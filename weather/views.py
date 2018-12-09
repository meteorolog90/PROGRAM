import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index (request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=37c7a38b3f7634ee184f6bc7aa41d329'
	

	if request.method == 'POST':
		form = CityForm(request.POST)
		form.save()

	form = CityForm()

	cities = City.objects.all()

	weather_data = []

	for city in cities:


		r = requests.get(url.format(city)).json()
		
		city_weather = {

			'city' : city.name,
			'lat': r['coord']['lat'],
			'lon': r['coord']['lon'],
			'temperature' : r['main']['temp'],
			'pressures' : r['main']['pressure'],
			'humidity' : r['main']['humidity'],
			# 'temperature_min' : r['main']['temp_min'],
			# 'temperature_max' : r['main']['temp_max'],
			'description' : r['weather'][0]['description'] ,
			'icon' : r['weather'][0]['icon'] ,
		}

		weather_data.append(city_weather)

	
	context = {'weather_data' : weather_data, 'form': form}

	return render(request, 'weather/weather.html', context)