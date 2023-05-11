from django.shortcuts import render
import requests
from .models import City

def index(request):
    if (request.method == 'POST'):
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=8e625a607d16ebabe7e9ebe493366fb7"
        
        city = request.POST['city']

        res = requests.get(url.format(city)).json()

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


def prognoz(request):
    if (request.method == 'POST'):
        url = "http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=8e625a607d16ebabe7e9ebe493366fb7"
        
        city = request.POST['city']
        date_get = request.POST['date']

        res = requests.get(url.format(city)).json()

        all_info = []

        if len(res) == 2:
            city = "Такого города не существует"
        else:
            city = res['city']['name']

            all_info = City_Info(date_get, res['list'], all_info)

            if len(all_info) == 0:
                city = "Введена некорректная дата"

        context = {'all_info': all_info, 'city': city}

    else:  
        all_info = []
        city = "Введите город и дату"

        context = {'all_info': all_info, 'city': city}
    
    return render(request, 'weather/prognoz.html', context)


def DT(elem):
    dt = elem['dt_txt'].split()
    time = dt[1].split(":")
    time = time[0] + ":" + time[1]
    date = dt[0].split("-")
    date = date[2] + "." + date[1]
    return date, time


def City_Info(date_get, res, all_info):
    for elem in res:

        dt = DT(elem)

        if date_get == dt[0] or date_get == "-":
            city_info = {
            'dt': dt[0] + " " + dt[1],
            'temp': elem['main']['temp'],
            'icon': elem['weather'][0]["icon"]
            }
            all_info.append(city_info)
    return all_info