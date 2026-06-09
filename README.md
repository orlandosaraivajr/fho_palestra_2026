# Consumo de API — Palestra Congresso FHO 2026

Material de apoio da palestra **"Consumo de API: o que você precisa saber antes de usar"**, apresentada no Congresso FHO 2026.

O repositório reúne exemplos práticos de consumo de APIs públicas em Python e Java, além de um exemplo de integração com modelos de linguagem (LLMs) via [OpenRouter](https://openrouter.ai), usando LangChain.

---

## Estrutura do repositório

```
fho_palestra_2026/
│
├── ConsumoAPI.pdf              # Slides da palestra
│
├── exemplos/                   # APIs públicas — sem autenticação
│   ├── ApiExample.java         # REST Countries com Java HttpClient
│   ├── openmeteo.py            # Previsão do tempo com Open-Meteo
│   ├── rick_and_morty.py       # Rick and Morty API (GET, filtros, paginação)
│   └── viacep.py               # Consulta de CEP brasileiro
│
└── openrouter/                 # Integração com LLMs via OpenRouter
    ├── openrouter.py           # Exemplo básico com LangChain
    ├── openrouter2.py          # Versão com boas práticas (logging, retry, validação)
    ├── requirements.txt        # Dependências Python
    └── env.example             # Modelo do arquivo .env
```

---

## Pré-requisitos

- Python 3.12+
- Java 11+ (apenas para o exemplo Java)
- Conta no [OpenRouter](https://openrouter.ai) com uma API Key (para os exemplos da pasta `openrouter/`)

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/orlandosaraivajr/fho_palestra_2026.git
cd fho_palestra_2026
```

### 2. Crie e ative um ambiente virtual Python

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r openrouter/requirements.txt
```

> Os exemplos da pasta `exemplos/` usam apenas `requests`, que já está incluído no `requirements.txt`.

---

## Configuração do OpenRouter

### 1. Copie o arquivo de exemplo

```bash
cp openrouter/env.example openrouter/.env
```

### 2. Edite o `.env` com sua chave

```env
OPENROUTER_API_KEY=sk-or-v1-SUA_CHAVE_AQUI
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

> Sua API Key pode ser gerada em [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys). O arquivo `.env` nunca deve ser commitado — ele já está protegido pelo `.gitignore`.

---

## Exemplos

### APIs públicas (sem autenticação)

Todos os exemplos abaixo rodam diretamente, sem nenhuma configuração adicional.

#### Open-Meteo — Previsão do tempo para São Paulo

```bash
python exemplos/openmeteo.py
```

```
Temperatura atual: 18.2°C
Velocidade do vento: 12.4 km/h
```

#### ViaCEP — Consulta de endereço por CEP

```bash
python exemplos/viacep.py
```

```
Logradouro: Avenida Paulista
Bairro: Bela Vista
Cidade: São Paulo - SP
```

#### Rick and Morty API — Personagens e episódios

```bash
python exemplos/rick_and_morty.py
```

Demonstra quatro técnicas de consumo de API:

| Técnica | Descrição |
|---|---|
| GET por ID | `GET /character/1` |
| GET com filtros | `GET /character?name=Rick&status=alive` |
| GET múltiplos recursos | `GET /character/1,2,3` |
| Paginação automática | Percorre todas as páginas de `/episode` com `Session` |

#### REST Countries — Java HttpClient

```bash
cd exemplos
javac ApiExample.java
java ApiExample
```

```
Status: 200
Body: [{"name":{"common":"Brazil"}...}]
```

---

### OpenRouter + LangChain

#### Exemplo básico

```bash
cd openrouter
python openrouter.py
```

#### Exemplo com boas práticas

```bash
cd openrouter
python openrouter2.py
```

O `openrouter2.py` inclui:

- Validação de variáveis de ambiente com falha rápida
- Logging com timestamp e nível
- Retry automático com backoff exponencial em caso de rate limit (429)
- Tratamento granular de erros (`RateLimitError`, `APIConnectionError`, `APIStatusError`)
- Dicionário de modelos — troca de modelo alterando apenas uma constante

#### Modelos disponíveis no `openrouter2.py`

| Chave | Modelo | Tier |
|---|---|---|
| `haiku` | `anthropic/claude-haiku-4-5` | Pago |
| `gemini` | `google/gemini-3.5-flash` | Pago |
| `llama` | `meta-llama/llama-3.3-70b-instruct:free` | Gratuito |
| `deepseek` | `deepseek/deepseek-chat` | Pago |

Para trocar de modelo, edite a constante `DEFAULT_MODEL` em `openrouter2.py`:

```python
DEFAULT_MODEL = "gemini"  # ou "haiku", "llama", "deepseek"
```

---

## Conceitos abordados na palestra

- O que é uma API e por que os `#include` do C/C++ também são APIs
- Modelo OSI e as 7 camadas de rede
- TCP/IP — three-way handshake e diferença entre TCP e UDP
- HTTP na camada de aplicação — métodos, status codes e headers
- RFCs essenciais: 9110, 9111, 6749, 7519, 9457
- Consumo de APIs em Java e Python (`requests`)
- Integração com LLMs via OpenRouter e LangChain

---

## Tecnologias utilizadas

- [Python](https://www.python.org/) 3.12+
- [requests](https://docs.python-requests.org/) — cliente HTTP Python
- [LangChain](https://python.langchain.com/) — framework para aplicações com LLMs
- [langchain-openai](https://python.langchain.com/docs/integrations/chat/openai/) — integração OpenAI-compatível
- [OpenRouter](https://openrouter.ai/) — gateway unificado para múltiplos LLMs
- [python-dotenv](https://pypi.org/project/python-dotenv/) — gerenciamento de variáveis de ambiente
- Java 11+ [HttpClient](https://docs.oracle.com/en/java/javase/11/docs/api/java.net.http/java/net/http/HttpClient.html) — cliente HTTP nativo

---

## APIs públicas utilizadas

| API | Documentação | Autenticação |
|---|---|---|
| Rick and Morty | [rickandmortyapi.com/documentation](https://rickandmortyapi.com/documentation) | Não |
| ViaCEP | [viacep.com.br](https://viacep.com.br) | Não |
| Open-Meteo | [open-meteo.com/en/docs](https://open-meteo.com/en/docs) | Não |
| REST Countries | [restcountries.com](https://restcountries.com) | Não |
| OpenRouter | [openrouter.ai/docs](https://openrouter.ai/docs) | API Key |

---

