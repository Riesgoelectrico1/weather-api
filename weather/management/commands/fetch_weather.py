from django.core.management.base import BaseCommand, CommandError
from weather.models import WeatherRecord
from weather.services import fetch_weather_data


class Command(BaseCommand):
    help = "Consulta el clima de una ciudad y guarda el registro en la base de datos."

    def add_arguments(self, parser):
        parser.add_argument("city", type=str, help="Nombre de la ciudad a consultar")

    def handle(self, *args, **options):
        city = options["city"]

        self.stdout.write(f"Consultando clima para: {city} ...")

        try:
            weather_data = fetch_weather_data(city)
        except ValueError as e:
            raise CommandError(str(e))
        except PermissionError as e:
            raise CommandError(str(e))
        except Exception as e:
            raise CommandError(f"Error inesperado: {e}")

        record = WeatherRecord.objects.create(
            city=city,
            temperature=weather_data["temperature"],
            humidity=weather_data["humidity"],
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Guardado: {record.city} | Temp: {record.temperature}°C | "
                f"Humedad: {record.humidity}% | {record.timestamp}"
            )
        )
