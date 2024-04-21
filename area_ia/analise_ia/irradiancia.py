import requests
from chave_api_nrel import API_KEY

# URL base da API do NREL Solar
base_url = 'https://developer.nrel.gov/api/solar/solar_resource/v1.json?'

# Parâmetros da solicitação (latitude, longitude e intervalo de datas)
latitude = '-23.555037954867913'
longitude = '-46.63829435599854'
start_date = '2020-01-01'
end_date = '2020-01-07'


# Construa a URL da solicitação com os parâmetros
url = f'{base_url}api_key={API_KEY}&lat={latitude}&lon={longitude}&start_date={start_date}&end_date={end_date}'

# Faça a solicitação GET para a API do NREL
response = requests.get(url)

# Verifique se a solicitação foi bem-sucedida (código de status 200)
if response.status_code == 200:
    # Converta a resposta para JSON
    data = response.json()
    # Extraia os dados de irradiação solar (por exemplo, a irradiação solar diária média)
    print(data)
    solar_radiation = data['outputs']['avg_dni']['annual']
    print(f'Irradiação solar média anual: {solar_radiation} kWh/m^2')
else:
    print('Erro ao fazer solicitação à API do NREL')
