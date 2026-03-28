from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from .models import WeatherRecord


class FetchWeatherEndpointTest(TestCase):
    """Tests para POST /api/fetch-weather/"""

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/fetch-weather/"

    @patch("weather.views.fetch_weather_data")
    def test_fetch_weather_success(self, mock_fetch):
        """Debe guardar el registro y responder 201."""
        mock_fetch.return_value = {"temperature": 22.5, "humidity": 60.0}

        response = self.client.post(self.url, {"city": "Bogota"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["city"], "Bogota")
        self.assertEqual(response.data["temperature"], 22.5)
        self.assertEqual(WeatherRecord.objects.count(), 1)

    @patch("weather.views.fetch_weather_data")
    def test_fetch_weather_city_not_found(self, mock_fetch):
        """Si la ciudad no existe, debe responder 404."""
        mock_fetch.side_effect = ValueError("Ciudad 'CiudadFalsa' no encontrada.")

        response = self.client.post(self.url, {"city": "CiudadFalsa"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    @patch("weather.views.fetch_weather_data")
    def test_fetch_weather_invalid_api_key(self, mock_fetch):
        """Si la API key es inválida, debe responder 401."""
        mock_fetch.side_effect = PermissionError("API key inválida o no autorizada.")

        response = self.client.post(self.url, {"city": "Lima"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetch_weather_missing_city(self):
        """Si no se manda 'city', debe responder 400."""
        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ListWeatherEndpointTest(TestCase):
    """Tests para GET /api/weather/"""

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/weather/"

        WeatherRecord.objects.create(city="Bogota", temperature=18.0, humidity=80.0)
        WeatherRecord.objects.create(city="Lima", temperature=22.0, humidity=70.0)
        WeatherRecord.objects.create(city="Bogota", temperature=19.5, humidity=75.0)

    def test_list_all_records(self):
        """Debe retornar todos los registros."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_city(self):
        """Debe filtrar correctamente por ciudad."""
        response = self.client.get(self.url, {"city": "Bogota"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for record in response.data:
            self.assertIn("Bogota", record["city"])

    def test_filter_by_city_case_insensitive(self):
        """El filtro de ciudad no debe ser sensible a mayúsculas."""
        response = self.client.get(self.url, {"city": "bogota"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_no_results(self):
        """Si la ciudad no existe, debe retornar lista vacía."""
        response = self.client.get(self.url, {"city": "Tokyo"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
