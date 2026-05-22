# Especificação de Requisitos Não Funcionais (System-Wide Requirements)

**Sistema:** Kanban Web  
**Disciplina:** Engenharia de Software — UnB  
**Versão:** 1.0  
**Data:** 2026-05-11

---

## 1. Introdução

Este documento especifica os requisitos não funcionais (RNF) do sistema Kanban Web. Os requisitos não funcionais descrevem as **qualidades** que o sistema deve possuir, não o que ele deve fazer, mas **como deve se comportar**. Eles são organizados por categorias de qualidade conforme o modelo ISO/IEC 25010 (SQuaRE).

---

## 2. Desempenho (Performance Efficiency)

### RNF-PERF-01 — Tempo de Resposta da API

| Atributo         | Valor                                                                       |
|------------------|-----------------------------------------------------------------------------|
| **Identificador**| RNF-PERF-01                                                                 |
| **Categoria**    | Desempenho                                                                  |
| **Descrição**    | Todas as requisições à API REST devem retornar resposta em tempo adequado   |
| **Critério**     | 95% das requisições respondidas em ≤ 500 ms; nenhuma ultrapassar 2 000 ms   |
| **Justificativa**| Garantir fluidez na experiência do usuário durante operações de CRUD        |
| **Métrica**      | Tempo medido do recebimento da requisição até o envio da resposta HTTP      |
| **Prioridade**   | Alta                                                                        |

### RNF-PERF-02 — Tempo de Carregamento do Frontend

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-PERF-02                                                                  |
| **Categoria**    | Desempenho                                                                   |
| **Descrição**    | A interface web deve carregar completamente em tempo aceitável               |
| **Critério**     | First Contentful Paint (FCP) ≤ 2 s em conexão de 10 Mbps                    |
| **Justificativa**| Primeira impressão do usuário determina a adoção da ferramenta               |
| **Prioridade**   | Média                                                                        |

### RNF-PERF-03 — Capacidade de Usuários Simultâneos

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-PERF-03                                                                  |
| **Categoria**    | Desempenho / Escalabilidade                                                  |
| **Descrição**    | O sistema deve suportar múltiplos usuários acessando simultaneamente         |
| **Critério**     | Suportar até 50 usuários concorrentes sem degradação perceptível             |
| **Justificativa**| Contexto acadêmico com turmas de até ~50 alunos                             |
| **Prioridade**   | Média                                                                        |

---

## 3. Confiabilidade (Reliability)

### RNF-REL-01 — Integridade Transacional

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-REL-01                                                                   |
| **Categoria**    | Confiabilidade                                                               |
| **Descrição**    | Operações de escrita devem ser atômicas — concluídas por completo ou revertidas |
| **Critério**     | Nenhuma operação deve deixar o banco em estado inconsistente em caso de falha|
| **Implementação**| Uso de transações SQLAlchemy com `db.commit()` / `db.rollback()`            |
| **Prioridade**   | Alta                                                                         |

### RNF-REL-02 — Disponibilidade

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-REL-02                                                                   |
| **Categoria**    | Confiabilidade                                                               |
| **Descrição**    | O sistema deve estar disponível durante os períodos de uso ativo             |
| **Critério**     | Disponibilidade ≥ 99% durante horário comercial (08h–22h, dias úteis)       |
| **Justificativa**| Uso acadêmico com prazos de entrega                                          |
| **Prioridade**   | Média                                                                        |

### RNF-REL-03 — Tratamento de Erros

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-REL-03                                                                   |
| **Categoria**    | Confiabilidade                                                               |
| **Descrição**    | O sistema deve retornar mensagens de erro claras e não expor stack traces    |
| **Critério**     | Respostas de erro sempre contêm campo `detail` com mensagem descritiva em português; código HTTP correto |
| **Implementação**| `HTTPException` do FastAPI com mensagens padronizadas                       |
| **Prioridade**   | Alta                                                                         |

---

## 4. Segurança (Security)

### RNF-SEC-01 — Validação de Entrada no Backend

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-SEC-01                                                                   |
| **Categoria**    | Segurança                                                                    |
| **Descrição**    | Toda entrada de dados deve ser validada e sanitizada no backend, independentemente do frontend |
| **Critério**     | Schemas Pydantic com validadores aplicados em todos os endpoints de escrita  |
| **Justificativa**| Prevenção contra injeção de dados maliciosos (OWASP A03:2021 — Injection)   |
| **Prioridade**   | Alta                                                                         |

### RNF-SEC-02 — Controle de Autorização por Recurso

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-SEC-02                                                                   |
| **Categoria**    | Segurança                                                                    |
| **Descrição**    | Operações destrutivas em quadros só podem ser realizadas pelo dono           |
| **Critério**     | Endpoints de exclusão de quadro e gerenciamento de membros verificam `email_dono` e retornam `403` para outros usuários |
| **Justificativa**| OWASP A01:2021 — Broken Access Control                                      |
| **Prioridade**   | Alta                                                                         |

### RNF-SEC-03 — Unicidade de Recursos

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-SEC-03                                                                   |
| **Categoria**    | Segurança / Integridade                                                      |
| **Descrição**    | O sistema deve garantir unicidade de e-mail de conta e código de quadro      |
| **Critério**     | Tentativas de duplicação retornam `409 Conflict` com mensagem explicativa    |
| **Implementação**| Chaves primárias e constraints `UniqueConstraint` no banco de dados          |
| **Prioridade**   | Alta                                                                         |

### RNF-SEC-04 — CORS Configurado

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-SEC-04                                                                   |
| **Categoria**    | Segurança                                                                    |
| **Descrição**    | O middleware CORS deve estar configurado no backend                          |
| **Critério**     | CORS habilitado via `CORSMiddleware` no FastAPI                              |
| **Observação**   | Em produção, `allow_origins` deve ser restrito ao domínio do frontend        |
| **Prioridade**   | Média                                                                        |

### RNF-SEC-05 — Validação de Regras de Senha

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-SEC-05                                                                   |
| **Categoria**    | Segurança                                                                    |
| **Descrição**    | Senhas devem obedecer a regras de complexidade mínima                        |
| **Critério**     | Exatamente 5 caracteres únicos contendo: ≥1 maiúscula, ≥1 minúscula, ≥1 dígito, ≥1 pontuação |
| **Justificativa**| Aumentar entropia mesmo dentro da restrição acadêmica de comprimento         |
| **Prioridade**   | Alta                                                                         |

---

## 5. Manutenibilidade (Maintainability)

### RNF-MANT-01 — Separação de Responsabilidades (Camadas)

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-MANT-01                                                                  |
| **Categoria**    | Manutenibilidade                                                             |
| **Descrição**    | O código deve ser organizado em camadas com responsabilidades bem definidas  |
| **Critério**     | Separação em: `models.py` (entidades ORM), `schemas.py` (validação), `routers/` (endpoints), `database.py` (persistência) |
| **Prioridade**   | Alta                                                                         |

### RNF-MANT-02 — Nomenclatura em Português

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-MANT-02                                                                  |
| **Categoria**    | Manutenibilidade                                                             |
| **Descrição**    | Nomes de variáveis, funções e endpoints devem estar em português             |
| **Critério**     | Consistência com o domínio do projeto acadêmico e com o módulo C++           |
| **Prioridade**   | Média                                                                        |

### RNF-MANT-03 — Routers Modulares

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-MANT-03                                                                  |
| **Categoria**    | Manutenibilidade                                                             |
| **Descrição**    | Cada domínio de negócio deve ter seu próprio router FastAPI                  |
| **Critério**     | Routers separados: `auth`, `contas`, `quadros`, `cartoes`, `membros`        |
| **Prioridade**   | Alta                                                                         |

### RNF-MANT-04 — Schemas Reutilizáveis

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-MANT-04                                                                  |
| **Categoria**    | Manutenibilidade                                                             |
| **Descrição**    | Funções de validação de domínio devem ser centralizadas e reutilizáveis      |
| **Critério**     | Funções `validar_codigo`, `validar_email`, `validar_senha`, etc. definidas em `schemas.py` e compartilhadas entre schemas |
| **Prioridade**   | Alta                                                                         |

---

## 6. Usabilidade (Usability)

### RNF-USA-01 — Interface Responsiva

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-USA-01                                                                   |
| **Categoria**    | Usabilidade                                                                  |
| **Descrição**    | A interface deve se adaptar a diferentes tamanhos de tela                    |
| **Critério**     | Funcional em resoluções de 375 px (mobile) a 1920 px (desktop)              |
| **Implementação**| Tailwind CSS com grid responsivo e componentes adaptáveis                    |
| **Prioridade**   | Média                                                                        |

### RNF-USA-02 — Feedback Visual Imediato

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-USA-02                                                                   |
| **Categoria**    | Usabilidade                                                                  |
| **Descrição**    | O sistema deve fornecer feedback visual para todas as ações do usuário       |
| **Critério**     | Notificações toast para sucesso (verde) e erro (vermelho) após cada operação |
| **Prioridade**   | Alta                                                                         |

### RNF-USA-03 — Drag-and-Drop Intuitivo

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-USA-03                                                                   |
| **Categoria**    | Usabilidade                                                                  |
| **Descrição**    | Cartões e quadros devem poder ser movidos por arraste                        |
| **Critério**     | Drag-and-drop funcional para mover cartões entre colunas; cursor muda ao arrastar; destino destacado |
| **Implementação**| API HTML5 Drag and Drop Events (`dragstart`, `dragover`, `drop`)            |
| **Prioridade**   | Alta                                                                         |

### RNF-USA-04 — Validação com Mensagens de Erro Descritivas

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-USA-04                                                                   |
| **Categoria**    | Usabilidade                                                                  |
| **Descrição**    | Erros de validação devem ser apresentados ao usuário em linguagem clara      |
| **Critério**     | Mensagens de erro exibidas dentro do modal ou como toast; nunca exibir detalhes internos de stack trace |
| **Prioridade**   | Alta                                                                         |

### RNF-USA-05 — Compatibilidade com Navegadores

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-USA-05                                                                   |
| **Categoria**    | Usabilidade / Portabilidade                                                  |
| **Descrição**    | A interface deve funcionar nos principais navegadores modernos               |
| **Critério**     | Compatível com Chrome 110+, Firefox 110+, Edge 110+, Safari 16+             |
| **Prioridade**   | Média                                                                        |

---

## 7. Portabilidade (Portability)

### RNF-PORT-01 — Independência de Sistema Operacional

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-PORT-01                                                                  |
| **Categoria**    | Portabilidade                                                                |
| **Descrição**    | O backend deve ser executável em Windows, Linux e macOS                      |
| **Critério**     | Instalação documentada para Windows (PowerShell), Linux/macOS e WSL          |
| **Implementação**| Python + SQLite portáveis; sem dependências de sistema operacional específico|
| **Prioridade**   | Alta                                                                         |

### RNF-PORT-02 — Banco de Dados Autocontido

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-PORT-02                                                                  |
| **Categoria**    | Portabilidade                                                                |
| **Descrição**    | O banco de dados deve ser criado automaticamente sem configuração externa     |
| **Critério**     | `kanban.db` criado automaticamente na primeira execução via `create_all()`   |
| **Prioridade**   | Alta                                                                         |

---

## 8. Compatibilidade (Compatibility)

### RNF-COMP-01 — API REST Padrão HTTP

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-COMP-01                                                                  |
| **Categoria**    | Compatibilidade                                                              |
| **Descrição**    | A API deve seguir os princípios REST com uso correto dos verbos HTTP         |
| **Critério**     | `GET` para leitura; `POST` para criação; `PUT/PATCH` para atualização; `DELETE` para remoção; códigos HTTP semanticamente corretos |
| **Prioridade**   | Alta                                                                         |

### RNF-COMP-02 — Documentação OpenAPI

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-COMP-02                                                                  |
| **Categoria**    | Compatibilidade                                                              |
| **Descrição**    | A API deve ser documentada automaticamente via OpenAPI 3.0                   |
| **Critério**     | Swagger UI acessível em `/docs`; ReDoc acessível em `/redoc`                 |
| **Implementação**| Gerado automaticamente pelo FastAPI                                          |
| **Prioridade**   | Média                                                                        |

---

## 9. Restrições de Implementação

### RNF-IMPL-01 — Stack Tecnológica Obrigatória

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-IMPL-01                                                                  |
| **Categoria**    | Restrição                                                                    |
| **Descrição**    | O sistema deve usar as tecnologias definidas no escopo do projeto            |
| **Critério**     | Backend: Python 3.10+ com FastAPI e SQLAlchemy; Frontend: Alpine.js e Tailwind CSS; Banco: SQLite |
| **Prioridade**   | Alta (restrição acadêmica)                                                   |

### RNF-IMPL-02 — Sem Dependências de Serviços Externos em Runtime

| Atributo         | Valor                                                                        |
|------------------|------------------------------------------------------------------------------|
| **Identificador**| RNF-IMPL-02                                                                  |
| **Categoria**    | Restrição                                                                    |
| **Descrição**    | O sistema não deve depender de serviços externos para funcionar              |
| **Critério**     | Todas as dependências declaradas em `requirements.txt`; Alpine.js servido localmente |
| **Observação**   | Tailwind CSS pode ser carregado via CDN para desenvolvimento; em produção, recomenda-se build local |
| **Prioridade**   | Média                                                                        |

---

## 10. Rastreabilidade

| RNF           | Componente de Implementação                              |
|---------------|----------------------------------------------------------|
| RNF-PERF-01   | `uvicorn` async + SQLAlchemy connection pooling          |
| RNF-REL-01    | `db.commit()` / `db.rollback()` em todos os routers      |
| RNF-REL-03    | `HTTPException` com mensagens em pt-BR                   |
| RNF-SEC-01    | `schemas.py` com `@field_validator` em todos os schemas  |
| RNF-SEC-02    | Verificação de `email_dono` em `routers/membros.py` e `routers/quadros.py` |
| RNF-SEC-03    | `primary_key` e `UniqueConstraint` em `models.py`        |
| RNF-USA-02    | Sistema de toast em `static/index.html` (Alpine.js)      |
| RNF-USA-03    | HTML5 Drag Events em `static/index.html`                 |
| RNF-PORT-01   | `requirements.txt` com dependências portáveis            |
| RNF-PORT-02   | `models.Base.metadata.create_all(bind=engine)` em `main.py` |
| RNF-COMP-02   | FastAPI gera automaticamente `/docs` e `/redoc`          |

## Link
https://docs.google.com/document/d/13nzqcIo8rn389AA8-JqbjToc2vKD3AoLgqHwMx2gg78/edit?usp=sharing