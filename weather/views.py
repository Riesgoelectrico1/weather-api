from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import WeatherRecord
from .serializers import WeatherRecordSerializer
from .services import fetch_weather_data


class WeatherViewSet(viewsets.ViewSet):
    """
    ViewSet con dos endpoints:
      POST /api/fetch-weather/  -> consulta la API externa y guarda el registro
      GET  /api/weather/        -> lista registros con filtros opcionales
    """

    @action(detail=False, methods=["post"], url_path="fetch-weather")
    def fetch_weather(self, request):
        city = request.data.get("city", "").strip()

        if not city:
            return Response(
                {"error": "El campo 'city' es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            weather_data = fetch_weather_data(city)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(
                {"error": f"Error al consultar la API externa: {e}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        record = WeatherRecord.objects.create(
            city=city,
            temperature=weather_data["temperature"],
            humidity=weather_data["humidity"],
        )

        serializer = WeatherRecordSerializer(record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="weather")
    def list_weather(self, request):
        queryset = WeatherRecord.objects.all().order_by("-timestamp")

        # Filtro por ciudad (case-insensitive)
        city = request.query_params.get("city", "")
        if city:
            queryset = queryset.filter(city__icontains=city)

        # Filtro por fecha (solo fecha, sin hora)
        date = request.query_params.get("date", "")
        if date:
            queryset = queryset.filter(timestamp__date=date)

        serializer = WeatherRecordSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
