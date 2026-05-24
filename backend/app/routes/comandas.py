import streamlit as st
import requests

API_URL = "https://sistemas-comandas-aps.onrender.com"

st.title("🍽️ Comandas")

# ==========================
# LISTAR COMANDAS
# ==========================

r = requests.get(
    f"{API_URL}/comandas"
)

comandas = []

if r.status_code == 200:
    comandas = r.json()

if len(comandas) == 0:

    st.info(
        "Nenhuma comanda cadastrada"
    )

else:

    for c in comandas:

        st.container()

        st.write(
            f"""
            Mesa: {c["mesa"]}

            Status: {c["status"]}

            Total: R$ {c["total"]}
            """
        )

st.divider()

# ==========================
# NOVA COMANDA
# ==========================

st.subheader(
    "Nova comanda"
)

mesa = st.number_input(
    "Mesa",
    min_value=1
)

if st.button(
    "Criar"
):

    requests.post(
        f"{API_URL}/comandas",
        json={
            "mesa": mesa
        }
    )

    st.rerun()


st.divider()

# ==========================
# ADICIONAR ITEM
# ==========================

st.subheader(
    "Adicionar item"
)

# busca produtos
r_prod = requests.get(
    f"{API_URL}/produtos"
)

produtos = []

if r_prod.status_code == 200:
    produtos = r_prod.json()

if len(comandas) > 0 and len(produtos) > 0:

    lista_comandas = {
        f"Mesa {c['mesa']}": c["id"]
        for c in comandas
    }

    lista_produtos = {
        p["nome"]: p["id"]
        for p in produtos
    }

    comanda_escolhida = st.selectbox(
        "Comanda",
        list(lista_comandas.keys())
    )

    produto = st.selectbox(
        "Produto",
        list(lista_produtos.keys())
    )

    quantidade = st.number_input(
        "Quantidade",
        min_value=1,
        value=1
    )

    if st.button(
        "Adicionar produto"
    ):

        requests.post(
            f"{API_URL}/itens",
            json={
                "comanda_id":
                lista_comandas[
                    comanda_escolhida
                ],

                "produto_id":
                lista_produtos[
                    produto
                ],

                "quantidade":
                quantidade
            }
        )

        st.success(
            "Produto adicionado"
        )

        st.rerun()

else:

    st.warning(
        "Cadastre produtos e comandas primeiro"
    )