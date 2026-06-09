import requests
 
# Coordenadas de São Paulo
params = {
    'latitude': -23.5505,
    'longitude': -46.6333,
    'current': 'temperature_2m,wind_speed_10m',
    'hourly': 'temperature_2m,precipitation_probability',
    'timezone': 'America/Sao_Paulo',
    'forecast_days': 1
}
 
response = requests.get('https://api.open-meteo.com/v1/forecast', params=params)
dados = response.json()
 
temp_atual = dados['current']['temperature_2m']
vento = dados['current']['wind_speed_10m']
print(f'Temperatura atual: {temp_atual}°C')
print(f'Velocidade do vento: {vento} km/h')
