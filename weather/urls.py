from django.urls import path
from .views import WeatherViewSet

fetch_view = WeatherViewSet.as_view({"post": "fetch_weather"})
list_view = WeatherViewSet.as_view({"get": "list_weather"})

urlpatterns = [
    path("fetch-weather/", fetch_view, name="fetch-weather"),
    path("weather/", list_view, name="weather-list"),
]
