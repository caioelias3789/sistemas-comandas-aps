# sistemas-comandas-aps
Sistema de comandas para restaurantes com FastAPI e Streamlit, incluindo login por perfil, gestão de produtos, comandas, relatórios e controle de pedidos.

sistemas-comandas-aps/
│
├── .devcontainer/
│   └── devcontainer.json
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth_routes.py
│   │   │   ├── comandas.py
│   │   │   ├── itens.py
│   │   │   ├── produtos.py
│   │   │   ├── relatorios.py
│   │   │   └── users.py
│   │   │
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── permissoes.py
│   │   └── schemas.py
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_comandas.py
│   │   ├── test_itens.py
│   │   └── test_produtos.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── telas/
│   │   ├── comandas.py
│   │   ├── dashboard.py
│   │   ├── produtos.py
│   │   └── relatorios.py
│   │
│   ├── app.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
