import requests
from django.shortcuts import render
from .models import City

def home(request):
    return render(request, 'home.html')

def index(request):
    api_key = "3e474146a4143b81bec68f9b7e55c8ed"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={{}}&appid={api_key}&units=metric"

    if request.method == 'POST':
        city = request.POST.get('city')
        City.objects.create(name=city)

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()

        if r.get('cod') != 200:
            continue

        data = {
            'city': city.name,
            'temp': r['main']['temp'],
            'desc': r['weather'][0]['description'],
        }
        weather_data.append(data)

    return render(request, 'weather/index.html', {'weather_data': weather_data})