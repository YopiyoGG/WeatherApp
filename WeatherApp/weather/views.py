from django.shortcuts import render
import requests
from .models import City

def index(request):
    if (request.method == 'POST'):
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=8e625a607d16ebabe7e9ebe493366fb7"
        
        city = request.POST['city']

        res = requests.get(url.format(city)).json()
        print(res)
        all_cities = []

        if (len(res) == 2):
            city_info = {
            'city': "Такого города нет",
            }
            all_cities.append(city_info)
            
        else:
            if (request.POST.get("action") == "Добавить в избранное"):
                City.objects.create(name = res['name'])
            elif (request.POST.get("action") == "Удалить из избранного"):
                for favorite in City.objects.all():
                    if (favorite.name == res['name']):
                        deleteCity = City.objects.get(name = res['name'])
                        deleteCity.delete()
            else:
                city_info = {
                    'city': res['name'],
                    'temp': res["main"]["temp"],
                    'icon': res["weather"][0]["icon"]
                }
                all_cities.append(city_info)
            

        for favorite in City.objects.all():
            res = requests.get(url.format(favorite.name)).json()
            city_info = {
                'city': favorite.name,
                'temp': res["main"]["temp"],
                'icon': res["weather"][0]["icon"]
            }
            all_cities.append(city_info)

        context = {'all_info': all_cities}

    else:
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=8e625a607d16ebabe7e9ebe493366fb7"
        
        all_cities = []

        for favorite in City.objects.all():
            res = requests.get(url.format(favorite.name)).json()
            city_info = {
                'city': favorite.name,
                'temp': res["main"]["temp"],
                'icon': res["weather"][0]["icon"]
            }
            all_cities.append(city_info)

        context = {'all_info': all_cities}
    
    return render(request, 'weather/index.html', context)