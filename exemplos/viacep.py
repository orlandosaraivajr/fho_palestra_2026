import requests
 
def consultar_cep(cep):
    cep_limpo = cep.replace('-', '').replace(' ', '')
    url = f'https://viacep.com.br/ws/{cep_limpo}/json/'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        if 'erro' in dados:
            return None  # CEP não encontrado
        return dados
    return None
 
endereco = consultar_cep('01310-100')
if endereco:
    print(f"Logradouro: {endereco['logradouro']}")
    print(f"Bairro: {endereco['bairro']}")
    print(f"Cidade: {endereco['localidade']} - {endereco['uf']}")
