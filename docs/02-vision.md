# Documento de Visão e Escopo — Kanban Web

**Disciplina:** Engenharia de Software — UnB  
**Versão:** 1.0  
**Data:** 2026-05-11  
**Autores:** Equipe de Desenvolvimento — Projeto TP01

---

## 1. Introdução

### 1.1 Finalidade do Documento

Este documento descreve a visão do produto **Kanban Web**, definindo o problema que o sistema resolve, os objetivos de negócio, o público-alvo, as principais funcionalidades, as restrições e o escopo do projeto. Serve como referência central para decisões de design, desenvolvimento e validação do sistema.

### 1.2 Definições e Acrônimos

| Termo         | Definição                                                                 |
|---------------|---------------------------------------------------------------------------|
| **Kanban**    | Método visual de gestão de fluxo de trabalho originado na Toyota (1940s)  |
| **WIP**       | Work-In-Progress — número máximo de tarefas simultâneas em uma coluna     |
| **Quadro**    | Instância de um projeto no sistema, contendo colunas e cartões            |
| **Cartão**    | Unidade de trabalho (tarefa) representada visualmente no quadro           |
| **Dono**      | Usuário que criou o quadro e possui permissões administrativas sobre ele  |
| **Membro**    | Usuário convidado para colaborar em um quadro                             |
| **API REST**  | Interface de programação baseada em HTTP com recursos nomeados por URLs   |
| **ORM**       | Object-Relational Mapping — mapeamento entre classes Python e tabelas SQL |

---

## 2. Posicionamento

### 2.1 Declaração do Problema

| Campo              | Descrição                                                                                                  |
|--------------------|-------------------------------------------------------------------------------------------------------------|
| **O problema de**  | Falta de visibilidade e controle sobre o andamento de tarefas em projetos acadêmicos e pequenas equipes     |
| **Afeta**          | Estudantes, pequenas equipes de desenvolvimento e projetos acadêmicos                                       |
| **Cujo impacto é** | Perda de prazo, duplicação de esforço, ausência de métricas de produtividade e dificuldade de colaboração   |
| **Uma boa solução**| Um sistema web leve de gestão Kanban com controle WIP, colaboração em tempo real e métricas de ciclo de vida |

### 2.2 Declaração do Produto

| Campo              | Descrição                                                                                                  |
|--------------------|-------------------------------------------------------------------------------------------------------------|
| **Para**           | Estudantes e pequenas equipes de desenvolvimento de software                                                |
| **Que**            | Precisam organizar e acompanhar tarefas de forma colaborativa e visual                                      |
| **O Kanban Web é** | Um sistema de gestão de projetos baseado no método Kanban acessível via navegador web                       |
| **Que**            | Oferece quadros compartilhados, controle de WIP, drag-and-drop de cartões e métricas de ciclo de vida       |
| **Diferente de**   | Ferramentas como Trello ou Jira, que exigem conta em serviço externo, têm curva de aprendizado maior e custo |
| **Nosso produto**  | É simples, autocontido, de fácil instalação local e desenvolvido com fins acadêmicos                        |

---

## 3. Partes Interessadas (Stakeholders)

| Parte Interessada         | Papel                         | Interesse Principal                                          |
|---------------------------|-------------------------------|--------------------------------------------------------------|
| Equipe de desenvolvimento | Desenvolvedores / Mantenedores| Implementar e manter o sistema com qualidade de código       |
| Professor da disciplina   | Avaliador                     | Verificar a aplicação de conceitos de Engenharia de Software |
| Estudantes (usuários)     | Usuários finais               | Gerenciar tarefas de projetos de forma eficiente             |
| Orientadores de IC/TCC    | Usuários potenciais           | Acompanhar progresso de alunos em pesquisas                  |

---

## 4. Visão Geral do Produto

### 4.1 Perspectiva do Produto

O Kanban Web é uma aplicação web independente, composta por:

- **Backend:** API REST em FastAPI (Python), responsável pela lógica de negócio e persistência
- **Frontend:** Interface de página única (SPA) servida pelo próprio backend, desenvolvida com Alpine.js e Tailwind CSS
- **Banco de Dados:** SQLite, embutido no servidor, sem necessidade de serviço externo

O sistema não depende de serviços de terceiros durante sua operação normal.

### 4.2 Diagrama de Contexto

```
                         ┌──────────────────────────────────┐
                         │          Kanban Web               │
  ┌─────────────┐        │  ┌─────────────────────────────┐ │
  │   Usuário   │──HTTP──│  │   FastAPI (Backend REST)    │ │
  │ (Navegador) │        │  │   Alpine.js (Frontend SPA)  │ │
  └─────────────┘        │  └────────────┬────────────────┘ │
                         │               │ SQLAlchemy ORM    │
                         │        ┌──────▼──────┐            │
                         │        │  kanban.db  │            │
                         │        │  (SQLite)   │            │
                         │        └─────────────┘            │
                         └──────────────────────────────────┘
```

### 4.3 Capacidades do Produto

| ID   | Capacidade                                | Benefício ao Usuário                                        |
|------|-------------------------------------------|-------------------------------------------------------------|
| C-01 | Cadastro e autenticação de usuários       | Acesso seguro e personalizado ao sistema                    |
| C-02 | Criação e gerenciamento de quadros Kanban | Organização visual de projetos com status automático        |
| C-03 | Criação e movimentação de cartões         | Acompanhamento do fluxo de tarefas em tempo real            |
| C-04 | Controle de limite WIP por coluna         | Prevenção de sobrecarga e gargalos no processo              |
| C-05 | Colaboração por convite de membros        | Trabalho em equipe com controle de permissões               |
| C-06 | Métricas de ciclo de vida (Lead/Cycle Time)| Análise de desempenho e identificação de melhorias         |
| C-07 | Drag-and-drop de cartões e quadros        | Interação intuitiva e ágil para movimentação de itens       |
| C-08 | Documentação interativa da API (Swagger)  | Facilidade de integração e teste por desenvolvedores        |

---

## 5. Escopo do Produto

### 5.1 Dentro do Escopo (In Scope)

- Autenticação por e-mail e senha (sem tokens JWT nesta versão)
- CRUD completo de contas, quadros e cartões
- Sistema de papéis Dono/Membro por quadro
- Convite e remoção de membros
- Controle WIP configurável (5, 10, 15 ou 20 por coluna)
- Status automático do quadro baseado nos cartões
- Registro de timestamps de ciclo (`criado_em`, `iniciado_em`, `concluido_em`)
- Endpoint de métricas por quadro
- Interface web responsiva (desktop e mobile)
- Documentação da API via Swagger UI e ReDoc
- Validação de domínio nos dados de entrada (backend e frontend)

### 5.2 Fora do Escopo (Out of Scope — versão atual)

- Notificações por e-mail
- Upload de anexos nos cartões
- Comentários e histórico de atividades
- Integração com ferramentas externas (GitHub, Jira, Slack)
- Autenticação OAuth (Google, GitHub, etc.)
- Aplicativo mobile nativo
- Multi-tenancy com isolamento completo de dados por organização
- Exportação de relatórios em PDF/CSV
- Visualizações de gráfico (Burndown, CFD)

---

## 6. Requisitos de Alto Nível

### 6.1 Requisitos Funcionais (Resumo)

| ID   | Requisito                                                                 |
|------|---------------------------------------------------------------------------|
| RF-01| O sistema deve permitir criar conta com e-mail, nome e senha              |
| RF-02| O sistema deve autenticar usuários por e-mail e senha                     |
| RF-03| O usuário autenticado deve poder criar, visualizar e excluir quadros       |
| RF-04| O sistema deve organizar quadros em colunas de status                     |
| RF-05| O usuário deve poder criar, editar, mover e excluir cartões em quadros    |
| RF-06| O sistema deve impor o limite WIP ao mover cartões                        |
| RF-07| O dono do quadro deve poder convidar e remover membros                    |
| RF-08| O sistema deve calcular e atualizar o status do quadro automaticamente    |
| RF-09| O sistema deve registrar timestamps ao mover cartões para `FAZENDO`/`FEITO`|
| RF-10| O sistema deve expor métricas de lead time e cycle time por quadro        |

### 6.2 Requisitos Não Funcionais (Resumo)

| ID    | Requisito                                                                  |
|-------|----------------------------------------------------------------------------|
| RNF-01| Tempo de resposta da API inferior a 500 ms para 95% das requisições        |
| RNF-02| Interface responsiva compatível com Chrome, Firefox, Edge e Safari modernos|
| RNF-03| Toda entrada de dados deve ser validada no backend independentemente       |
| RNF-04| Código-fonte estruturado com separação clara de camadas (MVC)              |
| RNF-05| O sistema deve funcionar sem conexão de rede externa (exceto CDN do Tailwind)|

---

## 7. Restrições do Projeto

| Tipo                | Restrição                                                                   |
|---------------------|-----------------------------------------------------------------------------|
| **Tecnológica**     | Python 3.10+; FastAPI; SQLite; Alpine.js; Tailwind CSS                      |
| **Acadêmica**       | Projeto de disciplina — prazo semestral, equipe de alunos                   |
| **Infraestrutura**  | Executado localmente ou em ambiente de baixo custo (single server)          |
| **Segurança**       | Senhas armazenadas em texto plano (limitação acadêmica — sem bcrypt nesta versão)|
| **Escala**          | Projetado para dezenas de usuários simultâneos, não para produção em larga escala|

---

## 8. Precedência e Prioridade de Funcionalidades

| Prioridade | Funcionalidade                          | Justificativa                                      |
|:----------:|-----------------------------------------|----------------------------------------------------|
| Alta       | Autenticação e cadastro                 | Pré-requisito para todas as outras funcionalidades |
| Alta       | CRUD de quadros                         | Funcionalidade central do produto                  |
| Alta       | CRUD de cartões e movimentação          | Entrega de valor principal ao usuário              |
| Alta       | Controle WIP                            | Diferencial essencial do método Kanban             |
| Média      | Colaboração com membros                 | Habilita uso em equipe                             |
| Média      | Métricas de ciclo de vida               | Agrega valor analítico ao produto                  |
| Baixa      | Documentação interativa da API          | Suporte ao desenvolvedor / avaliação acadêmica     |

---

## 9. Critérios de Aceitação do Produto

O produto será considerado aceito quando:

1. Todos os endpoints da API retornarem respostas corretas conforme documentado no Swagger
2. A interface web permitir realizar o fluxo completo (cadastro → login → criar quadro → criar cartão → mover cartão → logout) sem erros
3. O controle WIP impedir a movimentação quando o limite é atingido
4. O status do quadro for atualizado automaticamente ao mover cartões
5. Os timestamps `iniciado_em` e `concluido_em` forem registrados corretamente
6. A aplicação funcionar corretamente nos navegadores Chrome, Firefox e Edge em suas versões recentes
