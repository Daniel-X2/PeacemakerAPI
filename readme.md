# 🎬 API Pacificador

API REST inspirada na série **Pacificador (Peacemaker)**, desenvolvida com **FastAPI** e **SQLAlchemy**. Permite consultar informações sobre o elenco, personagens, realizar votações, visualizar rankings e estatísticas, além de buscas avançadas com filtros personalizados.

---

## 🚀 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e de alta performance
- **SQLAlchemy** - ORM para manipulação do banco de dados
- **Pydantic** - Validação de dados e serialização
- **SQLite** - Banco de dados relacional
- **Pytest** - Framework de testes

---

## 📁 Estrutura do Projeto
```
.
├───main.py                      # Endpoints da API
├───src/
│   ├── service/
│   │   └── main_service.py          # Lógica de negócio
│   ├── repository/
│   │   └── repo.py                  # Camada de acesso aos dados
│   ├── dto/
│   │   └── dto.py                   # Data Transfer Objects e serialização
│   ├── modelos/
│   │   └── models.py                # Modelos SQLAlchemy
│   └── Erros_personalizado/         
│       └── erros.py                  # Exceções customizadas
├───dados/
│   ├── banco.py                 # Configuração do banco
│   ├── banco.db                 # Banco SQLite
│   └── dados.json               # Dados iniciais
│                 
└───test_service.py              # Testes automatizados
```

---

## 🛠️ Como Rodar o Projeto

### 1. Clone o repositório
```bash
git clone https://github.com/Daniel-X2/api-pacificador
cd api-pacificador
```

### 2. Crie um ambiente virtual
```bash
python -m venv .venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install fastapi sqlalchemy pydantic pytest uvicorn
```

### 4. Execute a API
```bash
uvicorn main:app --reload
```

A API estará disponível em: `http://localhost:8000`

### 5. Acesse a documentação interativa
-    `http://localhost:8000/docs`


---

## 📌 Endpoints

### **1. GET /** 
Endpoint de teste
```
Retorno: "ola mano"
```

### **2. GET /elenco**
Retorna todo o elenco cadastrado no banco de dados.

**Resposta de sucesso (200):**
```json
[
  {
    "nome": "Christopher Smith / Pacificador",
    "ator": "John Cena",
    "vivo": true,
    "habilidades": ["Matador", "Especialista em armas"],
    "upvote": 5
  }
]
```

### **3. GET /elenco/{ator}**
Retorna informações completas de um ator específico.

**Exemplo:** `/elenco/John`

**Parâmetros:**
- `ator` (string, mínimo 3 caracteres) - Nome do ator a buscar

**Códigos de resposta:**
- `200` - Ator encontrado
- `400` - Validação falhou (menos de 3 caracteres)
- `404` - Ator não encontrado

### **4. GET /personagem/{personagem}**
Retorna dados completos de um personagem específico.

**Exemplo:** `/personagem/Adrian`

**Parâmetros:**
- `personagem` (string, mínimo 3 caracteres) - Nome do personagem

**Códigos de resposta:**
- `200` - Personagem encontrado
- `400` - Validação falhou
- `404` - Personagem não encontrado

### **5. POST /votar/{personagem}**
Adiciona um voto ao personagem informado.

**Exemplo:** `/votar/Pacificador`

**Resposta de sucesso:**
```json
"sucesso"
```

**Códigos de resposta:**
- `200` - Voto computado com sucesso
- `400` - Nome muito curto (mínimo 3 caracteres)
- `404` - Personagem não encontrado

### **6. GET /ranking/**
Retorna o ranking dos personagens mais votados.

**Parâmetros opcionais:**
- `top` (int, padrão: 3) - Quantidade de personagens no ranking

**Exemplo:** `/ranking/?top=5`

**Resposta de sucesso (200):**
```json
{
  "1° lugar": {
    "nome": "Christopher Smith / Pacificador",
    "ator": "John Cena",
    "vivo": true,
    "habilidades": ["Matador", "Especialista em armas"],
    "upvote": 10
  },
  "2° lugar": { ... },
  "3° lugar": { ... }
}
```

**Códigos de resposta:**
- `200` - Ranking retornado
- `404` - Valor zero, negativo ou banco vazio

### **7. GET /stats**
Retorna estatísticas gerais da API.

**Resposta de sucesso (200):**
```json
{
  "total de personagens": 8,
  "total de personagens vivos": 6,
  "total de personagens mortos": 2,
  "personagem com maior quantidade de votos": "Christopher Smith / Pacificador 10 votos"
}
```

### **8. GET /busca/**
Realiza busca avançada com filtros personalizados.

**Parâmetros opcionais:**
- `vivo` (bool, padrão: true) - Filtra por status (vivo/morto)
- `habilidade` (string, mínimo 3 caracteres) - Filtra por habilidade específica
- `mais_votado` (bool, padrão: false) - Retorna apenas o mais votado do filtro

**Exemplos de uso:**

Buscar personagens vivos:
```
/busca/?vivo=true
```

Buscar personagens com habilidade "matador":
```
/busca/?habilidade=matador
```

Buscar o personagem vivo, com habilidade "matador" e mais votado:
```
/busca/?vivo=true&habilidade=matador&mais_votado=true
```

**Códigos de resposta:**
- `200` - Resultados encontrados
- `400` - Parâmetros inválidos ou habilidade muito curta
- `404` - Nenhum personagem encontrado com os filtros

---

## 🧪 Testes

Execute os testes automatizados:
```bash
pytest test_service.py -v
```

**Cobertura de testes:**
- ✅ Busca com filtro por status (vivo/morto)
- ✅ Busca com filtro por habilidade
- ✅ Busca combinada (status + habilidade + mais votado)
- ✅ Busca no elenco por ator/personagem
- ✅ Retorno completo do elenco
- ✅ Estatísticas
- ✅ Ranking

---

## 🗂️ Estrutura de Dados

**Modelo Elenco:**
```python
{
  "nome": str,           # Nome do personagem
  "ator": str,           # Nome do ator
  "vivo": bool,          # Status do personagem
  "habilidades": list,   # Lista de habilidades
  "upvote": int          # Quantidade de votos
}
```

---

## 🎯 Arquitetura

O projeto segue o padrão de **arquitetura em camadas**:

- **Controller (main.py)** - Recebe requisições HTTP e trata exceções
- **Service (service.py)** - Contém a lógica de negócio
- **Repository (repo.py)** - Acessa e manipula dados no banco
- **Models (models.py)** - Define estrutura das tabelas
- **DTO (dto.py)** - Serializa dados para resposta da API

---

## 🚧 Melhorias Futuras

- [ ] Adicionar autenticação JWT
- [ ] Implementar paginação nos endpoints
- [ ] Dockerizar a aplicação
- [ ] Adicionar CI/CD
- [ ] Expandir cobertura de testes
- [ ] Implementar rate limiting
- [ ] Adicionar logs estruturados

---

## 📞 Contato

Desenvolvido para demonstração de boas práticas em desenvolvimento de APIs REST com FastAPI, arquitetura limpa e testes automatizados.

---

**Nota:** Esta API foi criada para fins educativos e de portfolio.
