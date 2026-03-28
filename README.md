# weather_api

Proyecto Django + DRF para consultar y almacenar datos de clima usando OpenWeatherMap.

---

## Requisitos

- Python 3.10+
- Cuenta en [OpenWeatherMap](https://openweathermap.org/api) (API key gratuita)

---

## Instalación

```bash
git clone <repo-url>
cd weather_api

pip install -r requirements.txt
```

Crear el archivo `.env` en la raíz del proyecto:

```
OPENWEATHER_API_KEY=tu_api_key_aqui
```

Aplicar migraciones:

```bash
python manage.py migrate
```

---

## Uso

### Comando de gestión

Consulta el clima de una ciudad y guarda el resultado en la base de datos:

```bash
python manage.py fetch_weather "Bogota"
python manage.py fetch_weather "Lima"
```

### Levantar servidor

```bash
python manage.py runserver
```

---

## Endpoints

### POST `/api/fetch-weather/`

Recibe una ciudad, consulta la API externa y guarda el registro.

**Request:**
```json
{ "city": "Bogota" }
```

**Response 201:**
```json
{
  "id": 1,
  "city": "Bogota",
  "temperature": 14.5,
  "humidity": 82.0,
  "timestamp": "2024-03-27T10:00:00Z"
}
```

**Errores:**
- `400` - Falta el campo `city`
- `401` - API key inválida
- `404` - Ciudad no encontrada

---

### GET `/api/weather/`

Lista todos los registros guardados. Acepta filtros opcionales.

**Filtros:**
```
/api/weather/?city=bogota
/api/weather/?date=2024-03-27
/api/weather/?city=bogota&date=2024-03-27
```

**Response 200:**
```json
[
  {
    "id": 1,
    "city": "Bogota",
    "temperature": 14.5,
    "humidity": 82.0,
    "timestamp": "2024-03-27T10:00:00Z"
  }
]
```

---

## Tests

```bash
python manage.py test weather --verbosity=2
```

Cubre:
- POST exitoso con mock de la API externa
- POST con ciudad no encontrada (404)
- POST con API key inválida (401)
- POST sin campo `city` (400)
- GET lista completa
- GET filtro por ciudad
- GET filtro case-insensitive
- GET sin resultados

---

## Estructura del proyecto

```
weather_api/
├── .env                        # Variables de entorno (no subir a git)
├── requirements.txt
├── manage.py
├── weather_api/
│   ├── settings.py
│   └── urls.py
└── weather/
    ├── models.py               # WeatherRecord
    ├── serializers.py
    ├── services.py             # Lógica de llamada a OpenWeatherMap
    ├── views.py                # ViewSet con fetch_weather y list_weather
    ├── urls.py
    ├── tests.py
    └── management/
        └── commands/
            └── fetch_weather.py
```

---

## .gitignore recomendado

```
.env
db.sqlite3
__pycache__/
*.pyc
```
