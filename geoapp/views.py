import requests
import os
import random
from dotenv import load_dotenv
from django.shortcuts import render
from .forms import CountryForm
from pymongo import MongoClient

load_dotenv()
api_key = os.getenv('OPENWEATHERMAP_API_KEY')

client = MongoClient("mongodb://<MONGO_PRIVATE_IP>:27017/")
db = client['assignment10']
history_collection = db['history']

def search_country(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            continent = form.cleaned_data['continent']
            country_input = form.cleaned_data['country'].strip().lower()

            response = requests.get(f"https://restcountries.com/v3.1/region/{continent}")
            countries = response.json()

            results = []

            if country_input:
                # Search for a specific country
                for country in countries:
                    if country_input == country['name']['common'].lower():
                        results.append(country)
                        break
                if not results:
                    return render(request, 'search_results.html', {
                        'error': f"'{country_input}' not found in {continent}."
                    })
            else:
                # Pick 5 random countries
                if len(countries) >= 5:
                    results = random.sample(countries, 5)
                else:
                    results = countries  

            output = []
            for match in results:
                name = match['name']['common']
                capital = match.get('capital', ['Unknown'])[0]
                population = match.get('population', 'N/A')
                latlng = match.get('latlng', [])

                # Get weather
                weather = {}
                if capital != 'Unknown':
                    weather_data = requests.get(
                        f"https://api.openweathermap.org/data/2.5/weather?q={capital}&appid={api_key}&units=metric"
                    ).json()
                    weather['temp'] = weather_data.get('main', {}).get('temp', 'N/A')
                    weather['desc'] = weather_data.get('weather', [{}])[0].get('description', 'N/A')

                record = {
                    "country": name,
                    "capital": capital,
                    "population": population,
                    "latlng": latlng,
                    "weather": weather
                }

                output.append(record)
                history_collection.insert_one(record)

            return render(request, 'search_results.html', {'results': output})

    else:
        form = CountryForm()

    return render(request, 'continent_form.html', {'form': form})

def view_history(request):
    history = list(history_collection.find())
    return render(request, 'history.html', {'history': history})