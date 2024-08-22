from django.shortcuts import render
import random
from django.http import JsonResponse
import requests

# Define a dictionary for genres based on weather types
weather_genres = {
    "sunny": ["Adventure", "Action", "Comedy"],
    "rain": ["Drama", "Romance", "Mystery"],
    "snow": ["Slice of Life", "Fantasy", "Supernatural"],
    "cloudy": ["Sci-Fi", "Thriller", "Horror"],
    "fog": ["Mystery", "Supernatural", "Drama"],
    "storm": ["Action", "Thriller", "Adventure"],
    "windy": ["Adventure", "Action", "Sci-Fi"],
    "hot": ["Romance", "Comedy", "Adventure"],
    "cold": ["Fantasy", "Slice of Life", "Drama"],
    "hail": ["Action", "Sci-Fi", "Thriller"],
    "overcast": ["Sci-Fi", "Drama", "Mystery"],
    "partly cloudy": ["Adventure", "Romance", "Comedy"],
    "showers": ["Drama", "Romance", "Slice of Life"],
    "thunderstorm": ["Action", "Thriller", "Supernatural"],
    "drizzle": ["Drama", "Mystery", "Romance"],
    "clear": ["Comedy", "Adventure", "Romance"],
    "dull": ["Slice of Life", "Drama", "Fantasy"],
    "humid": ["Romance", "Comedy", "Adventure"],
    "freezing": ["Fantasy", "Slice of Life", "Mystery"],
}

def recommend_anime_genre(weather_description):
    weather_description = weather_description.lower()
    for key in weather_genres.keys():
        if key in weather_description:
            genres = weather_genres[key]
            return random.choice(genres)
    
    # Return a default genre if no match is found
    return "Fantasy"

def get_weather(request, city):
    # Fetch weather data
    url = f"https://goweather.herokuapp.com/weather/{city}"
    response = requests.get(url)
    weather_data = response.json()
    
    celsius_temp = float(weather_data.get('temperature', '0 °C').replace('°C', '').strip())
    fahrenheit_temp = (celsius_temp * 9/5) + 32
    weather_data['temperature'] = f"{fahrenheit_temp:.1f} °F"

    # Determine recommended anime genre
    genre = recommend_anime_genre(weather_data.get("description", ""))
    
    # Fetch anime recommendations from Jikan API
    genre_mapping = {
        "Adventure": 1,
        "Action": 2,
        "Comedy": 4,
        "Drama": 8,
        "Romance": 10,
        "Mystery": 17,
        "Slice of Life": 36,
        "Fantasy": 7,
        "Supernatural": 37,
        "Sci-Fi": 10,
        "Thriller": 28,
        "Horror": 14
    }

    genre_id = genre_mapping.get(genre, 1)  # Default to 1 if genre is not found

    anime_url = f"https://api.jikan.moe/v4/anime?genres={genre_id}"
    anime_response = requests.get(anime_url)
    anime_data = anime_response.json()
    
    # Extract relevant data including thumbnails
    for anime in anime_data.get("data", []):
        anime['thumbnail_url'] = anime['images']['jpg']['image_url']
    
    # Include the recommended anime list, the recommended genre, and city in the response
    weather_data["recommended_anime"] = anime_data.get("data", [])
    weather_data["recommended_genre"] = genre
    weather_data["city"] = city
    
    return JsonResponse(weather_data)
