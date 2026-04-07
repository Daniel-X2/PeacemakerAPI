# 🎬 API Pacificador
[![entrega continua](https://github.com/Daniel-X2/PeacemakerAPI/actions/workflows/desenvolvimento.yml/badge.svg)](https://github.com/Daniel-X2/PeacemakerAPI/actions/workflows/desenvolvimento.yml)

API REST inspirada na série **Pacificador (Peacemaker)**, desenvolvida com **FastAPI** e **SQLAlchemy**. Permite consultar informações sobre o elenco, personagens, realizar votações, visualizar rankings e estatísticas, além de buscas avançadas com filtros personalizados.

🌐 **API em produção:** https://api-pacificador.onrender.com/docs

---

## 🚀 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e de alta performance
- **SQLAlchemy** - ORM para manipulação do banco de dados
- **Pydantic** - Validação de dados e serialização
- **PostgreSQL** - Banco de dados relacional (produção)
- **Pytest** - Framework de testes
- **Locust** - Testes de carga
- **Render** - Plataforma de hospedagem
- **SlowAPI** - Rate limiting por IP na rota de votação
- **GitHub Actions** - CI/CD automatizado
---

## 🌐 Acesso Rápido

- **Documentação Interativa (Swagger):** https://api-pacificador.onrender.com/docs
- **API Base URL:** `https://api-pacificador.onrender.com`

---

## ⚡ Testes de Carga (Locust)

A API foi submetida a testes de carga utilizando o **Locust**, simulando múltiplos usuários concorrentes realizando requisições.

📊 **Cenário de teste:**
- Simulação de múltiplos usuários acessando endpoints principais
- Execução contra ambiente em produção
- Testes focados em estabilidade e tempo de resposta

📁 Arquivo de resultado disponível no projeto:
- `dados/Locust.csv`

📌 **O que foi validado:**
- Tempo médio de resposta
- Taxa de requisições por segundo (RPS)
- Estabilidade sob carga
- Baixa taxa de falhas

Esses testes demonstram que a API suporta múltiplas requisições simultâneas mantendo consistência e desempenho.

---

## 📁 Estrutura do Projeto
```
.
├───main.py
├───src/
│   ├── service/
│   ├── repository/
│   ├── dto/
│   ├── modelos/
│   └── Erros_personalizado/
├───dados/
│   ├── banco.py
│   ├── banco.db
│   └── dados.json
└───test_service.py
```

---

## 🛠️ Como Rodar o Projeto Localmente

```bash
git clone https://github.com/Daniel-X2/api-pacificador
cd api-pacificador
python -m venv .venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

Acesse: `http://localhost:8000/docs`

---

## 🧪 Testes

```bash
pytest test_service.py -v
```

---

## 🎯 Arquitetura

O projeto segue arquitetura em camadas:

- **Controller** - Entrada HTTP
- **Service** - Regras de negócio
- **Repository** - Acesso a dados
- **Models** - Estrutura do banco
- **DTO** - Serialização

---

## 🚧 Melhorias Futuras

- [ ] Autenticação JWT
- [ ] Paginação
- [ ] CI/CD
- [ ] Rate limiting
- [ ] Logs estruturados

---

## 📞 Contato

Projeto desenvolvido para fins de portfólio demonstrando boas práticas com FastAPI, testes e arquitetura limpa.

- 🌐 https://api-pacificador.onrender.com/docs
- 💻 https://github.com/Daniel-X2/api-pacificador

---

**Nota:** API voltada para fins educacionais.

