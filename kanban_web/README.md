# 📊 Kanban Web — Backend & Frontend

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?style=flat-square&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3-lightblue?style=flat-square&logo=sqlite)
![Alpine.js](https://img.shields.io/badge/Alpine.js-Lightweight%20JS-orange?style=flat-square&logo=javascript)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

**Sistema de gestão Kanban** desenvolvido para a disciplina de **Engenharia de Software (UnB)**

[📖 Documentação](#-documentação-do-projeto) • [🚀 Quick Start](#-como-rodar) • [🏗️ Arquitetura](#-arquitetura-do-projeto) • [📡 API](#-endpoints-principais)

</div>

---

## 🎯 Visão Geral

Um **sistema de gestão Kanban** completo e moderno, com:

- ✅ **Backend robusto** com FastAPI (Python)
- ✅ **Banco de dados** seguro com SQLAlchemy + SQLite
- ✅ **Frontend responsivo** com Alpine.js
- ✅ **Autenticação** de usuários integrada
- ✅ **Gerenciamento de quadros** com suporte a membros e cartões
- ✅ **API REST** totalmente documentada (Swagger UI + ReDoc)

---

## 📁 Estrutura do projeto

```
kanban_web/
├── main.py           # Ponto de entrada da aplicação FastAPI
├── database.py       # Configuração do SQLAlchemy e SQLite
├── models.py         # Modelos ORM (tabelas do banco)
├── schemas.py        # Schemas Pydantic (validação de entrada/saída)
├── requirements.txt  # Dependências Python
├── routers/
│   ├── auth.py       # Login e cadastro
│   ├── contas.py     # CRUD de contas de usuário
│   ├── quadros.py    # CRUD de quadros Kanban
│   ├── cartoes.py    # CRUD de cartões
│   └── membros.py    # Gerenciamento de membros de quadros
└── static/
    └── index.html    # Frontend (servido pelo próprio FastAPI)
```

O banco de dados `kanban.db` (SQLite) é criado automaticamente na primeira execução dentro da pasta `kanban_web/`.

---

## ⚙️ Tecnologias Utilizadas

| Camada | Tecnologia | Descrição |
|--------|-----------|-----------|
| **Backend** | FastAPI | Framework REST de alta performance |
| **ORM** | SQLAlchemy | Mapeamento objeto-relacional |
| **Banco de Dados** | SQLite | Banco de dados leve e portável |
| **Validação** | Pydantic | Validação de dados com type hints |
| **Frontend** | Alpine.js | Framework JavaScript minimalista |
| **Autenticação** | JWT | Tokens para autenticação segura |

---

## 🚀 Como rodar

### 📋 Pré-requisitos

- Python **3.10+**
- `pip` atualizado
- Terminal (Windows PowerShell, Bash, WSL, etc)

### ⚡ Instalação rápida (4 passos)

#### 1️⃣ Clone ou acesse a pasta do projeto

```bash
cd kanban_web
```

#### 2️⃣ Crie e ative o ambiente virtual

**🐧 Linux / macOS / WSL:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**🪟 Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> 💡 **Dica:** Após ativar, o terminal exibirá `(venv)` no início da linha.

#### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4️⃣ Inicie o servidor

```bash
uvicorn main:app --reload
```

🎉 O servidor estará disponível em: **http://127.0.0.1:8000**

---

## 🌐 Acessando a aplicação

| 🔗 URL | 📝 Descrição |
|--------|-----------|
| [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/) | 🎨 Frontend (Interface Kanban) |
| [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs) | 📚 Documentação Swagger UI |
| [`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc) | 📖 Documentação ReDoc |

---

## 🏗️ Arquitetura do projeto

### Autenticação
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/auth/cadastrar` | 📝 Cadastrar nova conta |
| `POST` | `/auth/login` | 🔐 Login de usuário |

### Contas
| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/contas/{email}` | 👤 Buscar conta por e-mail |
| `DELETE` | `/contas/{email}` | 🗑️ Remover conta |

### Quadros
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/quadros/` | ➕ Criar quadro |
| `GET` | `/quadros/{codigo}` | 🔍 Buscar quadro por código |
| `PUT` | `/quadros/{codigo}` | ✏️ Atualizar quadro |
| `DELETE` | `/quadros/{codigo}` | ❌ Remover quadro |

### Cartões
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/cartoes/` | ➕ Criar cartão |
| `GET` | `/cartoes/{codigo}` | 🔍 Buscar cartão |
| `PUT` | `/cartoes/{codigo}` | ✏️ Atualizar cartão |
| `DELETE` | `/cartoes/{codigo}` | ❌ Remover cartão |

### Membros
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/membros/` | 👥 Adicionar membro a um quadro |
| `DELETE` | `/membros/{quadro}/{email}` | 🚫 Remover membro de um quadro |

---

## ✅ Regras de validação

> 🔗 **Nota:** As regras abaixo espelham os domínios definidos na arquitetura do projeto (baseados em especificação C++)

| Campo | Regra | Exemplo |
|-------|-------|---------|
| **Código** | 4 caracteres: `LLDD` (2 letras + 2 dígitos) | `AB12` ✓ |
| **Nome/Texto** | 5-30 caracteres, começa com maiúscula, sem espaços duplos | `Meu Projeto` ✓ |
| **E-mail** | Parte local: 2-10 chars, domínio: 2-20 chars, apenas letras e pontos | `user.name@example.com` ✓ |
| **Senha** | 5-8 caracteres, letras + dígitos, sem espaços | `Pass123` ✓ |
| **Limite WIP** | Inteiro entre 1 e 10 | `5` ✓ |
| **Coluna** | `A FAZER` \| `FAZENDO` \| `FEITO` | `FAZENDO` ✓ |
| **Prioridade** | `BAIXA` \| `MEDIA` \| `ALTA` | `ALTA` ✓ |
| **Status do Quadro** | `A FAZER` \| `EM ANDAMENTO` \| `EM TESTES` \| `CONCLUIDO` | `EM ANDAMENTO` ✓ |

---

## 📚 Documentação do projeto

A documentação completa do projeto está disponível na pasta `../docs/`:

| 📄 Documento | 🎯 Propósito |
|-------------|-----------|
| **PDF 2** - Documento de Visão e Escopo | Define objetivos, escopo e justificativas |
| **PDF 4** - Especificação de Requisitos Funcionais | Lista as histórias de usuário (user stories) |
| **PDF 5** - Documento de Arquitetura | Descreve a arquitetura técnica do sistema |
| **PDF 6** - Projeto de Interface com o Usuário | Design e mockups da interface |
| **PDF 7** - Projeto Físico de Banco de Dados | Esquema e estrutura do banco de dados |

---

## 🛠️ Estrutura dos arquivos Python

| 📄 Arquivo | 🎯 Função |
|-----------|---------|
| `main.py` | Ponto de entrada e configuração da aplicação FastAPI |
| `database.py` | Configuração do SQLAlchemy e conexão SQLite |
| `models.py` | Modelos ORM (mapeamento das tabelas do banco) |
| `schemas.py` | Schemas Pydantic (validação de entrada/saída) |
| `routers/*.py` | Endpoints organizados por domínio |

### Routers (Endpoints organizados)
- `auth.py` — Autenticação (cadastro, login)
- `contas.py` — Gerenciamento de contas de usuário
- `quadros.py` — CRUD de quadros Kanban
- `cartoes.py` — CRUD de cartões
- `membros.py` — Gerenciamento de membros de quadros
- `raias.py` — Gerenciamento de raias/colunas

---

## ⚡ Comandos úteis

```bash
# Ativar ambiente virtual (Windows)
.\venv\Scripts\Activate.ps1

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar servidor em modo desenvolvimento (com auto-reload)
uvicorn main:app --reload

# Rodar servidor em outra porta
uvicorn main:app --reload --port 8080

# Desativar ambiente virtual
deactivate
```

---

## 💡 Observações importantes

- 📦 O arquivo `kanban.db` (banco SQLite) é **gerado automaticamente** — não precisa criar manualmente
- 🔄 O servidor `--reload` reinicia automaticamente ao salvar arquivos `.py` — perfeito para desenvolvimento
- 📁 A pasta `venv/` deve ser ignorada pelo Git (já configurada no `.gitignore`)
- 🔐 Nunca commitê credenciais ou `.env` files — use variáveis de ambiente
- ✅ Antes de fazer commit, teste os endpoints no Swagger UI (`/docs`)

---

## 📞 Suporte & Dúvidas

**Dúvidas sobre o projeto?** Consulte:

- 📖 **Documentação API:** [Swagger UI](http://127.0.0.1:8000/docs) — disponível localmente
- 📚 **Documentos PDF:** Veja a pasta `../docs/` para arquitetura, requisitos e design
- 🐛 **Relatar bugs:** Abra uma issue ou contate a equipe de desenvolvimento

---

## 👥 Desenvolvido para

**Engenharia de Software** — Universidade de Brasília (UnB)

---

<div align="center">

**Made by the:**

**Caetano Korilo Fleury de Amorim - 212006737**

**Luis Henrique Wiltgen de Toledo - 221003968**

**Pedro Rafael Faria Ferreira - 190094591**

**Vinicius Chaves - 211060764**

</div>
