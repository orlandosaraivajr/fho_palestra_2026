"""
Exemplo de uso do LangChain com OpenRouter.
Boas práticas: validação de env vars, tratamento de erros,
retry automático, logging e separação de responsabilidades.
"""

import logging
import os
import sys

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from openai import APIConnectionError, APIStatusError, RateLimitError

# ─────────────────────────────────────────────
# Configuração de logging
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# Modelos disponíveis (comente/descomente)
# ─────────────────────────────────────────────
MODELS = {
    "haiku":   "anthropic/claude-haiku-4-5",
    "gemini":  "google/gemini-3.5-flash",
    "llama":   "meta-llama/llama-3.3-70b-instruct:free",
    "deepseek":"deepseek/deepseek-chat",
}

DEFAULT_MODEL = "haiku"


# ─────────────────────────────────────────────
# Carregamento e validação das variáveis de ambiente
# ─────────────────────────────────────────────
def carregar_configuracao() -> dict:
    load_dotenv()

    api_key  = os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("OPENROUTER_BASE_URL")

    if not api_key:
        logger.error("Variável OPENROUTER_API_KEY não encontrada no .env")
        sys.exit(1)

    if not base_url:
        logger.warning("OPENROUTER_BASE_URL não definida — usando padrão.")
        base_url = "https://openrouter.ai/api/v1"

    return {"api_key": api_key, "base_url": base_url}


# ─────────────────────────────────────────────
# Criação do modelo LLM
# ─────────────────────────────────────────────
def criar_llm(config: dict, model_key: str = DEFAULT_MODEL) -> ChatOpenAI:
    model_id = MODELS.get(model_key)

    if not model_id:
        modelos_validos = ", ".join(MODELS.keys())
        raise ValueError(f"Modelo '{model_key}' inválido. Opções: {modelos_validos}")

    logger.info("Modelo selecionado: %s", model_id)

    llm = ChatOpenAI(
        model=model_id,
        temperature=0,
        api_key=config["api_key"],
        base_url=config["base_url"],
    )

    # Retry automático: 3 tentativas com backoff exponencial
    return llm.with_retry(
        retry_if_exception_type=(RateLimitError, APIConnectionError),
        stop_after_attempt=3,
        wait_exponential_jitter=True,
    )


# ─────────────────────────────────────────────
# Criação da chain
# ─────────────────────────────────────────────
def criar_chain(llm: ChatOpenAI):
    prompt = PromptTemplate.from_template("Conte-me um pouco sobre {tema}")
    parser = StrOutputParser()
    return prompt | llm | parser


# ─────────────────────────────────────────────
# Execução da chain com tratamento de erros
# ─────────────────────────────────────────────
def executar(chain, tema: str) -> str | None:
    if not tema or not tema.strip():
        raise ValueError("O tema não pode ser vazio.")

    logger.info("Enviando requisição para o tema: '%s'", tema)

    try:
        resultado = chain.invoke({"tema": tema})
        logger.info("Resposta recebida com sucesso.")
        return resultado

    except RateLimitError:
        logger.error("Rate limit atingido. Aguarde e tente novamente.")

    except APIConnectionError:
        logger.error("Falha de conexão. Verifique sua internet ou o base_url.")

    except APIStatusError as e:
        logger.error("Erro HTTP %s retornado pela API: %s", e.status_code, e.message)

    except Exception as e:
        logger.error("Erro inesperado: %s", e)

    return None


# ─────────────────────────────────────────────
# Ponto de entrada
# ─────────────────────────────────────────────
def main():
    config = carregar_configuracao()
    llm    = criar_llm(config, model_key=DEFAULT_MODEL)
    chain  = criar_chain(llm)

    tema = "programação orientada a objetos"
    resultado = executar(chain, tema)

    if resultado:
        print("\n" + "=" * 60)
        print(resultado)
        print("=" * 60)
    else:
        logger.warning("Nenhuma resposta obtida.")
        sys.exit(1)


if __name__ == "__main__":
    main()