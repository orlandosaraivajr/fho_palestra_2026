"""
Consumo da API Rick and Morty
https://rickandmortyapi.com/documentation

Demonstra: GET simples, parâmetros de query, paginação,
           tratamento de erros e uso de Session.
"""

import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError


BASE_URL = "https://rickandmortyapi.com/api"


# ─────────────────────────────────────────────
# 1. Buscar um personagem pelo ID
# ─────────────────────────────────────────────
def buscar_personagem(id: int) -> dict | None:
    try:
        response = requests.get(f"{BASE_URL}/character/{id}", timeout=5)
        response.raise_for_status()  # lança HTTPError para status 4xx/5xx
        return response.json()

    except HTTPError as e:
        status = e.response.status_code
        if status == 404:
            print(f"  [404] Personagem {id} não encontrado.")
        else:
            print(f"  [HTTP {status}] Erro ao buscar personagem {id}: {e}")
        return None

    except ConnectionError:
        print("  [ERRO] Sem conexão com a internet ou API indisponível.")
        return None

    except Timeout:
        print("  [ERRO] A requisição demorou demais (timeout).")
        return None


# ─────────────────────────────────────────────
# 2. Listar personagens com filtro e paginação
# ─────────────────────────────────────────────
def listar_personagens(nome: str = "", status: str = "", pagina: int = 1) -> dict | None:
    """
    Parâmetros de filtro suportados pela API:
      name   → parte do nome
      status → 'alive', 'dead' ou 'unknown'
      page   → número da página (cada página tem 20 itens)
    """
    params = {"page": pagina}
    if nome:
        params["name"] = nome
    if status:
        params["status"] = status

    try:
        response = requests.get(f"{BASE_URL}/character", params=params, timeout=5)
        response.raise_for_status()
        return response.json()

    except HTTPError as e:
        if e.response.status_code == 404:
            print(f"  [404] Nenhum personagem encontrado com os filtros informados.")
        else:
            print(f"  [HTTP {e.response.status_code}] {e}")
        return None

    except (ConnectionError, Timeout) as e:
        print(f"  [ERRO de rede] {e}")
        return None


# ─────────────────────────────────────────────
# 3. Buscar múltiplos personagens de uma vez
# ─────────────────────────────────────────────
def buscar_varios_personagens(ids: list[int]) -> list[dict]:
    """
    A API aceita uma lista de IDs em um único request:
    /character/1,2,3
    """
    ids_str = ",".join(str(i) for i in ids)

    try:
        response = requests.get(f"{BASE_URL}/character/{ids_str}", timeout=5)
        response.raise_for_status()
        data = response.json()
        # Se for um único ID, a API retorna um dict; vários IDs retornam lista
        return data if isinstance(data, list) else [data]

    except HTTPError as e:
        print(f"  [HTTP {e.response.status_code}] Erro ao buscar personagens: {e}")
        return []

    except (ConnectionError, Timeout) as e:
        print(f"  [ERRO de rede] {e}")
        return []


# ─────────────────────────────────────────────
# 4. Buscar todos os episódios usando Session
#    (Session reutiliza a conexão TCP — mais
#    eficiente para múltiplas chamadas seguidas)
# ─────────────────────────────────────────────
def listar_todos_episodios() -> list[dict]:
    episodios = []

    with requests.Session() as session:
        url = f"{BASE_URL}/episode"

        while url:
            try:
                response = session.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()

                episodios.extend(data["results"])

                # A API devolve a URL da próxima página em data["info"]["next"]
                # Quando não há mais páginas, o valor é None
                url = data["info"]["next"]

            except HTTPError as e:
                print(f"  [HTTP {e.response.status_code}] Erro ao buscar episódios.")
                break

            except (ConnectionError, Timeout) as e:
                print(f"  [ERRO de rede] {e}")
                break

    return episodios


# ─────────────────────────────────────────────
# MAIN — demonstração de tudo acima
# ─────────────────────────────────────────────
if __name__ == "__main__":

    # ── 1. Personagem por ID ──────────────────
    print("=" * 50)
    print("1. Buscando o personagem de ID 1")
    print("=" * 50)
    personagem = buscar_personagem(1)
    if personagem:
        print(f"  Nome:    {personagem['name']}")
        print(f"  Status:  {personagem['status']}")
        print(f"  Espécie: {personagem['species']}")
        print(f"  Origem:  {personagem['origin']['name']}")

    # ── 1b. ID que não existe ─────────────────
    print("\nBuscando personagem com ID inválido (99999):")
    buscar_personagem(99999)

    # ── 2. Listagem com filtro ────────────────
    print("\n" + "=" * 50)
    print("2. Personagens vivos chamados 'Rick'")
    print("=" * 50)
    resultado = listar_personagens(nome="Rick", status="alive")
    if resultado:
        info = resultado["info"]
        print(f"  Total encontrado: {info['count']} personagens "
              f"em {info['pages']} página(s)")
        for p in resultado["results"][:5]:  # mostra até 5
            print(f"  • {p['name']:30} | {p['status']:7} | {p['species']}")

    # ── 3. Vários personagens de uma vez ──────
    print("\n" + "=" * 50)
    print("3. Buscando personagens 2, 3 e 5 de uma vez")
    print("=" * 50)
    varios = buscar_varios_personagens([2, 3, 5])
    for p in varios:
        print(f"  [{p['id']:>3}] {p['name']:30} — {p['status']}")

    # ── 4. Todos os episódios ─────────────────
    print("\n" + "=" * 50)
    print("4. Buscando todos os episódios (com paginação automática)")
    print("=" * 50)
    episodios = listar_todos_episodios()
    print(f"  Total de episódios: {len(episodios)}")
    print("  Primeiros 5 episódios:")
    for ep in episodios[:5]:
        qtd_personagens = len(ep["characters"])
        print(f"  • {ep['episode']} — {ep['name']:35} | {qtd_personagens} personagens")

    print("\nFim.")
