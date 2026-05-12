# Protótipo do Sistema — Kanban Web

**Sistema:** Kanban Web  
**Disciplina:** Engenharia de Software — UnB  
**Versão:** 1.0  
**Data:** 2026-05-11

---

## 1. Visão Geral do Protótipo

O protótipo do Kanban Web é um **protótipo de alta fidelidade funcional**, implementado como sistema real executável. Diferente de um protótipo de papel ou mockup de ferramenta de design, o protótipo **é o próprio sistema operacional**, composto por:

- Backend FastAPI rodando em `http://127.0.0.1:8000`
- Frontend SPA em `static/index.html` com Alpine.js
- Banco de dados SQLite (`kanban.db`) com dados persistentes

---

## 2. Como Executar o Protótipo

### 2.1 Pré-requisitos

| Requisito      | Versão Mínima | Como verificar            |
|----------------|---------------|---------------------------|
| Python         | 3.10+         | `python --version`        |
| pip            | Atualizado    | `pip --version`           |
| Navegador      | Chrome 110+ / Firefox 110+ | —           |

### 2.2 Passo a Passo

```bash
# 1. Acesse a pasta do projeto web
cd kanban_web

# 2. Crie e ative o ambiente virtual
python -m venv venv

# Linux / macOS / WSL:
source venv/bin/activate

# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o servidor
uvicorn main:app --reload
```

### 2.3 URLs de Acesso

| URL                             | Descrição                                   |
|---------------------------------|---------------------------------------------|
| `http://127.0.0.1:8000/`        | Interface web do protótipo (frontend)       |
| `http://127.0.0.1:8000/docs`    | Swagger UI — documentação interativa da API |
| `http://127.0.0.1:8000/redoc`   | ReDoc — documentação alternativa da API     |

---

## 3. Roteiro de Teste do Sistema (System Test Script)

O roteiro abaixo descreve os passos para um **teste de sistema completo** do protótipo, cobrindo todos os fluxos funcionais principais.

---

### FASE 1 — Autenticação e Cadastro

#### Teste ST-01: Cadastrar nova conta

**Pré-condição:** Sistema rodando; nenhuma conta cadastrada  
**Dados de teste:**
- Nome: `Pedro Alves`
- Email: `pedro@unb.br`
- Senha: `Ab1.x`

**Passos:**
1. Acessar `http://127.0.0.1:8000/`
2. Clicar na aba **Cadastro**
3. Preencher os campos com os dados de teste
4. Clicar em **Criar Conta**

**Resultado esperado:**
- Toast verde: "Conta criada com sucesso! Faça login."
- Sistema permanece na tela de login

---

#### Teste ST-02: Cadastrar conta com dados inválidos

**Passos:**
1. Na aba Cadastro, preencher:
   - Nome: `Ana` (menos de 5 chars)
   - Email: `ana@unb.br`
   - Senha: `Ab1.x`
2. Clicar em **Criar Conta**

**Resultado esperado:**
- Toast vermelho exibindo a mensagem de validação do campo `nome`
- Conta **não** criada

---

#### Teste ST-03: Login com credenciais corretas

**Dados de teste:** Email: `pedro@unb.br`, Senha: `Ab1.x`

**Passos:**
1. Na aba Login, preencher e-mail e senha
2. Clicar em **Entrar**

**Resultado esperado:**
- Tela de login some; painel de projetos exibido
- Nome "Pedro Alves" visível na navbar

---

#### Teste ST-04: Login com senha errada

**Passos:**
1. Login com e-mail correto e senha `Zz9!a` (incorreta)

**Resultado esperado:**
- Toast vermelho: "Email ou senha inválidos"
- Tela de login permanece

---

### FASE 2 — Gestão de Projetos (Quadros)

#### Teste ST-05: Criar quadro

**Pré-condição:** Usuário autenticado  
**Dados:**
- Código: `AB12`
- Nome: `Projeto Alpha`
- Descrição: `Sistema de teste`
- WIP Limit: 10

**Passos:**
1. Clicar em **+ Novo Projeto**
2. Preencher o formulário e confirmar

**Resultado esperado:**
- Toast verde: "Quadro criado com sucesso!"
- Card `AB12 — Projeto Alpha` aparece na coluna "A FAZER" do Kanban de Projetos

---

#### Teste ST-06: Criar quadro com código duplicado

**Passos:**
1. Tentar criar outro quadro com código `AB12`

**Resultado esperado:**
- Toast vermelho: "Código de quadro já existe"
- Segundo quadro não criado

---

#### Teste ST-07: Arrastar quadro para coluna diferente de status

**Passos:**
1. Arrastar o card `AB12` para a coluna "EM ANDAMENTO"

**Resultado esperado:**
- Card aparece na coluna "EM ANDAMENTO"
- Status do quadro atualizado no banco

---

### FASE 3 — Gestão de Tarefas (Cartões)

#### Teste ST-08: Abrir quadro e criar cartão

**Pré-condição:** Quadro `AB12` criado  
**Dados:**
- Código: `CD34`
- Nome: `Impl. backend`
- Descrição: `Endpoints REST`
- Responsável: Pedro Alves
- Prioridade: ALTA
- Data limite: (data futura)

**Passos:**
1. Clicar no card do quadro `AB12`
2. Clicar em **+ Novo Cartão** na coluna "A FAZER"
3. Preencher e confirmar

**Resultado esperado:**
- Toast verde: "Cartão criado com sucesso!"
- Card aparece na coluna "A FAZER" com badge vermelho (ALTA)
- Contador da coluna mostra `(1/10)`

---

#### Teste ST-09: Mover cartão para FAZENDO

**Passos:**
1. Arrastar o cartão `CD34` para a coluna "FAZENDO"

**Resultado esperado:**
- Cartão aparece em "FAZENDO"
- `iniciado_em` registrado automaticamente (verificável via `/docs`)
- Status do quadro recalculado para "EM ANDAMENTO"

---

#### Teste ST-10: Testar limite WIP

**Pré-condição:** Criar um quadro com `limite_wip = 5`; criar 5 cartões e movê-los para "FAZENDO"

**Passos:**
1. Criar o 6º cartão e tentar arrastá-lo para "FAZENDO"

**Resultado esperado:**
- Toast vermelho: "Limite WIP atingido na coluna 'FAZENDO'"
- Cartão permanece na coluna de origem

---

#### Teste ST-11: Mover cartão para FEITO

**Passos:**
1. Mover o cartão `CD34` de "FAZENDO" → "EM TESTE" → "FEITO"

**Resultado esperado:**
- `concluido_em` registrado automaticamente
- Status do quadro recalculado para "CONCLUIDO" (se for o único cartão)

---

#### Teste ST-12: Editar cartão

**Passos:**
1. Clicar no ícone ✏ do cartão `CD34`
2. Alterar a prioridade para BAIXA e confirmar

**Resultado esperado:**
- Badge do cartão muda para verde (BAIXA)
- Toast verde confirmando edição

---

#### Teste ST-13: Excluir cartão

**Passos:**
1. Clicar no ícone 🗑 do cartão `CD34`
2. Confirmar no modal

**Resultado esperado:**
- Cartão removido da coluna
- Toast verde: "Cartão excluído"

---

### FASE 4 — Colaboração com Membros

#### Teste ST-14: Cadastrar segundo usuário

**Passos:**
1. Fazer logout
2. Cadastrar conta:
   - Nome: `Ana Costa`
   - Email: `ana@unb.br`
   - Senha: `Bc2;y`

---

#### Teste ST-15: Convidar membro

**Pré-condição:** Dois usuários cadastrados; autenticado como `pedro@unb.br`

**Passos:**
1. Dentro do quadro `AB12`, clicar em **👥 Membros**
2. Digitar `ana@unb.br` e clicar em **Convidar**

**Resultado esperado:**
- `Ana Costa` aparece na lista de membros com papel "MEMBRO"
- Badge com contador de membros atualizado

---

#### Teste ST-16: Verificar acesso do membro convidado

**Passos:**
1. Fazer logout
2. Login como `ana@unb.br`

**Resultado esperado:**
- Quadro `AB12 — Projeto Alpha` aparece na lista de projetos de Ana

---

#### Teste ST-17: Tentar excluir quadro como membro (deve falhar)

**Pré-condição:** Autenticado como `ana@unb.br`

**Passos:**
1. Tentar excluir o quadro `AB12`

**Resultado esperado:**
- Toast vermelho: "Sem permissão para excluir este quadro"
- Quadro permanece

---

### FASE 5 — Edição de Perfil

#### Teste ST-18: Alterar nome do usuário

**Pré-condição:** Autenticado como `pedro@unb.br`

**Passos:**
1. Clicar no nome "Pedro Alves" na navbar
2. Alterar para `Pedro Silva`
3. Clicar em **Salvar Alterações**

**Resultado esperado:**
- Nome atualizado na navbar
- Toast verde: "Perfil atualizado com sucesso!"

---

## 4. Demonstração em Vídeo — Roteiro Sugerido

> **Nota:** O vídeo deve ter duração de **5–10 minutos** e cobrir os testes principais do sistema.

### Sugestão de Estrutura do Vídeo

| Tempo    | Cena                                                                 |
|----------|----------------------------------------------------------------------|
| 00:00    | Apresentação: sistema, disciplina, integrantes                       |
| 00:30    | Iniciar servidor (`uvicorn main:app --reload`)                       |
| 01:00    | Cadastro de dois usuários (Pedro e Ana)                              |
| 01:45    | Login como Pedro                                                     |
| 02:00    | Criar quadro `AB12 — Projeto Alpha` com WIP = 5                      |
| 02:30    | Criar 3 cartões com prioridades diferentes                           |
| 03:15    | Demonstrar drag-and-drop dos cartões entre colunas                   |
| 04:00    | Tentar ultrapassar o limite WIP → mostrar bloqueio                   |
| 04:30    | Convidar Ana como membro                                             |
| 05:00    | Login como Ana → verificar acesso ao quadro                          |
| 05:30    | Tentar excluir quadro como Ana → mostrar erro 403                    |
| 06:00    | Mostrar `/docs` (Swagger UI) com os endpoints disponíveis            |
| 06:30    | Executar `GET /cartoes/quadro/AB12/metricas` no Swagger              |
| 07:00    | Encerramento                                                         |

---

## 5. Cobertura de Requisitos pelo Protótipo

| Requisito Funcional | Testado em         | Status    |
|---------------------|--------------------|-----------|
| RF-01 (Criar conta) | ST-01, ST-02       | ✓ Coberto |
| RF-02 (Autenticação)| ST-03, ST-04       | ✓ Coberto |
| RF-03 (CRUD quadros)| ST-05, ST-06, ST-09| ✓ Coberto |
| RF-04 (Status quadro automático) | ST-09, ST-11 | ✓ Coberto |
| RF-05 (CRUD cartões)| ST-08, ST-12, ST-13| ✓ Coberto |
| RF-06 (WIP)         | ST-10              | ✓ Coberto |
| RF-07 (Membros)     | ST-15, ST-16, ST-17| ✓ Coberto |
| RF-08 (Status auto) | ST-09, ST-11       | ✓ Coberto |
| RF-09 (Timestamps)  | ST-09, ST-11       | ✓ Coberto |
| RF-10 (Métricas)    | Swagger UI         | ✓ Coberto |

---

## 6. Limitações Conhecidas do Protótipo

| Limitação                              | Impacto                                      | Melhoria Futura                             |
|----------------------------------------|----------------------------------------------|---------------------------------------------|
| Senhas em texto plano                  | Risco de segurança se exposto                | Usar bcrypt/argon2 + HTTPS                  |
| Sem expiração de sessão (localStorage) | Sessão permanece até logout manual           | Implementar JWT com expiração               |
| SQLite sem WAL mode                    | Possível lock em escritas concorrentes       | Habilitar WAL ou migrar para PostgreSQL     |
| Tailwind via CDN                       | Dependência de rede externa para dev         | Build local com PostCSS + PurgeCSS          |
| Sem paginação na listagem              | Pode degradar com muitos cartões             | Implementar paginação nos endpoints GET     |
| Sem autenticação nos endpoints GET     | Qualquer pessoa com a URL pode ler dados     | Exigir header de autenticação em todos endpoints |
