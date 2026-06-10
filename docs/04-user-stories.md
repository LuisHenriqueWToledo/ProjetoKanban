# Especificação de Requisitos Funcionais — Histórias de Usuário

**Sistema:** Kanban Web  
**Disciplina:** Engenharia de Software — UnB  
**Versão:** 1.0  
**Data:** 2026-05-11

---

## 1. Personas

### Persona 1 — Carlos (Dono de Projeto)
> Carlos é estudante de Engenharia de Software, no 5º semestre. Ele coordena projetos de disciplinas práticas e precisa ter visibilidade clara do que cada colega está fazendo, identificar gargalos rapidamente e garantir que as tarefas sejam concluídas dentro dos prazos.

### Persona 2 — Marina (Membro de Equipe)
> Marina é estudante de Ciência da Computação. Participa de múltiplos projetos simultaneamente e precisa de uma forma simples de saber quais tarefas são suas, qual é a prioridade de cada uma e comunicar seu progresso sem reuniões frequentes.

### Persona 3 — Rafael (Observador / Membro)
> Rafael é monitor de uma disciplina de Engenharia de Software. Ele precisa visualizar o progresso das equipes nos projetos, mas não cria nem edita cartões — apenas acompanha o andamento geral.

---

## 2. Épicos

| Épico | Descrição                                              |
|-------|--------------------------------------------------------|
| EP-01 | Gestão de Identidade (autenticação e conta)            |
| EP-02 | Gestão de Projetos (quadros Kanban)                    |
| EP-03 | Gestão de Tarefas (cartões Kanban)                     |
| EP-04 | Gestão de Raias (swimlanes por responsável)            |
| EP-05 | Colaboração (membros e permissões)                     |
| EP-06 | Métricas e Análise de Desempenho                       |

---

## 3. Histórias de Usuário

---

### EP-01: Gestão de Identidade

---

#### US-01 — Criar Conta

**Como** novo usuário,  
**Quero** me cadastrar no sistema com meu nome, e-mail e senha,  
**Para que** eu possa acessar os meus projetos de qualquer dispositivo.

**Critérios de Aceitação:**

- [ ] O formulário de cadastro contém campos para nome, e-mail e senha
- [ ] O sistema valida que o e-mail possui exatamente um `@`, parte local com 2–10 chars e domínio com 2–20 chars
- [ ] O sistema valida que o nome tem 5–30 chars, começa com maiúscula e não contém caracteres especiais (exceto espaço e hífen)
- [ ] O sistema valida que a senha tem exatamente 5 caracteres únicos, contendo ao menos uma maiúscula, uma minúscula, um dígito e um sinal de pontuação (`.,;!?`)
- [ ] Se o e-mail já estiver cadastrado, o sistema exibe mensagem de conflito e não duplica a conta
- [ ] Após cadastro bem-sucedido, a conta aparece como recurso acessível

**Endpoint:** `POST /auth/cadastrar`  
**Status HTTP:** `201 Created` | `409 Conflict` | `422 Unprocessable Entity`

**Notas Técnicas:**
- Validação pelo schema `ContaCreate` (Pydantic)
- E-mail é chave primária — unicidade garantida pelo banco

---

#### US-02 — Fazer Login

**Como** usuário cadastrado,  
**Quero** fazer login com meu e-mail e senha,  
**Para que** eu possa acessar meus projetos e tarefas.

**Critérios de Aceitação:**

- [ ] O formulário de login contém campos para e-mail e senha
- [ ] Credenciais corretas resultam em login bem-sucedido e exibição do painel principal
- [ ] Credenciais incorretas resultam em mensagem de erro clara sem revelar qual campo está errado
- [ ] A sessão é mantida localmente (localStorage) até o usuário fazer logout
- [ ] Campo de senha tem toggle para mostrar/ocultar o texto

**Endpoint:** `POST /auth/login`  
**Status HTTP:** `200 OK` | `401 Unauthorized`

---

#### US-03 — Fazer Logout

**Como** usuário autenticado,  
**Quero** encerrar minha sessão no sistema,  
**Para que** minha conta fique protegida ao deixar o dispositivo.

**Critérios de Aceitação:**

- [ ] Botão "Sair" visível na barra de navegação quando autenticado
- [ ] Ao clicar em "Sair", a sessão é removida do localStorage
- [ ] Após logout, a tela de login é exibida novamente
- [ ] Dados do usuário não ficam acessíveis após logout

**Implementação:** Client-side — limpeza de `localStorage` e reset do estado Alpine.js

---

#### US-04 — Editar Perfil

**Como** usuário autenticado,  
**Quero** alterar meu nome e/ou senha,  
**Para que** eu possa manter meus dados atualizados.

**Critérios de Aceitação:**

- [ ] O painel de perfil é acessível clicando no nome do usuário na navbar
- [ ] O e-mail é exibido como somente leitura (não pode ser alterado)
- [ ] O usuário pode alterar apenas o nome, apenas a senha, ou ambos simultaneamente
- [ ] As mesmas regras de validação do cadastro se aplicam à atualização
- [ ] Campos deixados em branco não são atualizados

**Endpoint:** `PUT /contas/{email}`  
**Status HTTP:** `200 OK` | `404 Not Found` | `422 Unprocessable Entity`

---

#### US-05 — Excluir Conta

**Como** usuário autenticado,  
**Quero** excluir permanentemente minha conta,  
**Para que** meus dados sejam removidos do sistema.

**Critérios de Aceitação:**

- [ ] A exclusão de conta remove todos os quadros criados pelo usuário (cascade)
- [ ] A exclusão remove também todas as participações como membro em outros quadros
- [ ] O sistema confirma a ação antes de executar (modal de confirmação)
- [ ] Após exclusão, o usuário é redirecionado para a tela de login

**Endpoint:** `DELETE /contas/{email}`  
**Status HTTP:** `204 No Content` | `404 Not Found`

---

### EP-02: Gestão de Projetos (Quadros)

---

#### US-06 — Criar Quadro

**Como** Carlos (dono de projeto),  
**Quero** criar um novo quadro Kanban com código, nome, descrição e limite WIP,  
**Para que** eu possa organizar as tarefas do meu projeto.

**Critérios de Aceitação:**

- [ ] O formulário de criação contém campos para código, nome, descrição e seleção de limite WIP
- [ ] O código deve ter o formato `LLDD` (2 letras maiúsculas + 2 dígitos, ex: `AB12`)
- [ ] Nome e descrição seguem as regras de validação de texto (5–30 chars, inicial maiúscula)
- [ ] O limite WIP pode ser 5, 10, 15 ou 20
- [ ] Se o código já existir, o sistema retorna erro 409
- [ ] O quadro criado aparece na coluna "A FAZER" do painel de projetos
- [ ] O criador é automaticamente registrado como DONO do quadro

**Endpoint:** `POST /quadros/?email_dono={email}`  
**Status HTTP:** `201 Created` | `409 Conflict` | `422 Unprocessable Entity`

---

#### US-07 — Visualizar Lista de Projetos

**Como** Marina (membro de equipe),  
**Quero** ver todos os projetos dos quais faço parte,  
**Para que** eu possa acessar rapidamente o quadro correto.

**Critérios de Aceitação:**

- [ ] O painel inicial exibe todos os quadros onde o usuário é DONO ou MEMBRO
- [ ] Os quadros são organizados visualmente em colunas por status (`A FAZER`, `EM ANDAMENTO`, `EM TESTES`, `CONCLUIDO`)
- [ ] Cada quadro exibe seu código, nome, descrição e limite WIP
- [ ] Quadros podem ser arrastados entre as colunas de status

**Endpoint:** `GET /quadros/?email_dono={email}`  
**Status HTTP:** `200 OK`

---

#### US-08 — Mover Status do Quadro

**Como** Carlos,  
**Quero** mover o status do quadro manualmente no painel de projetos,  
**Para que** eu possa ajustar o status quando necessário além da atualização automática.

**Critérios de Aceitação:**

- [ ] O quadro pode ser arrastado entre as colunas de status no painel de projetos
- [ ] O status é atualizado na base de dados via `PATCH /quadros/{codigo}/status`
- [ ] A coluna de destino é destacada visualmente durante o arraste

**Endpoint:** `PATCH /quadros/{codigo}/status`  
**Status HTTP:** `200 OK` | `404 Not Found`

---

#### US-09 — Excluir Quadro

**Como** Carlos,  
**Quero** excluir um quadro que não é mais necessário,  
**Para que** minha lista de projetos fique organizada.

**Critérios de Aceitação:**

- [ ] Apenas o DONO do quadro pode excluí-lo
- [ ] Um modal de confirmação é exibido antes da exclusão
- [ ] Todos os cartões e vínculos de membro são excluídos junto com o quadro (cascade)
- [ ] Tentativas de exclusão por não-donos retornam `403 Forbidden`

**Endpoint:** `DELETE /quadros/{codigo}?email_dono={email}`  
**Status HTTP:** `204 No Content` | `403 Forbidden` | `404 Not Found`

---

### EP-03: Gestão de Tarefas (Cartões)

---

#### US-10 — Criar Cartão

**Como** Marina,  
**Quero** criar um cartão de tarefa em um quadro,  
**Para que** o trabalho a ser feito fique registrado e visível para a equipe.

**Critérios de Aceitação:**

- [ ] O formulário de cartão contém: código, nome, descrição, responsável, prioridade e data limite
- [ ] O código do cartão segue o formato `LLDD` e é único dentro do quadro
- [ ] O responsável deve ser selecionado a partir da lista de membros do quadro
- [ ] A prioridade pode ser BAIXA, MEDIA ou ALTA
- [ ] A data limite é opcional; quando fornecida, deve ser igual ou posterior à data atual
- [ ] O cartão é criado na coluna `A FAZER` por padrão
- [ ] `criado_em` é registrado automaticamente com o timestamp UTC atual

**Endpoint:** `POST /cartoes/`  
**Status HTTP:** `201 Created` | `409 Conflict` | `422 Unprocessable Entity`

---

#### US-11 — Visualizar Cartões do Quadro

**Como** Rafael (observador),  
**Quero** ver todos os cartões de um quadro organizados por coluna e raia,  
**Para que** eu possa acompanhar o progresso das tarefas.

**Critérios de Aceitação:**

- [ ] Os cartões são listados em suas respectivas colunas (`A FAZER`, `FAZENDO`, `EM TESTE`, `FEITO`) e raias
- [ ] Cada raia representa um responsável do quadro
- [ ] Cada cartão exibe: código, nome, responsável, prioridade e data limite (se houver)
- [ ] A prioridade é destacada visualmente (ex: cor de badge diferente por nível)
- [ ] O número de cartões em cada coluna é exibido junto com o limite WIP

**Endpoint:** `GET /cartoes/quadro/{codigo_quadro}`  
**Status HTTP:** `200 OK`

---

#### US-12 — Mover Cartão Entre Colunas

**Como** Marina,  
**Quero** mover um cartão de uma coluna para outra arrastando-o,  
**Para que** o estado atual da tarefa seja refletido no quadro.

**Critérios de Aceitação:**

- [ ] Cartões podem ser movidos por drag-and-drop entre as colunas
- [ ] Cartões podem ser movidos entre células da matriz (coluna de destino + raia atual)
- [ ] Ao tentar mover para uma coluna que atingiu o limite WIP, o movimento é bloqueado e uma mensagem de erro é exibida
- [ ] Quando um cartão é movido para `FAZENDO` pela primeira vez, `iniciado_em` é registrado
- [ ] Quando um cartão é movido para `FEITO` pela primeira vez, `concluido_em` é registrado
- [ ] O status do quadro é recalculado automaticamente após o movimento
- [ ] O cartão na coluna de destino é destacado visualmente durante o arraste

**Endpoint:** `PATCH /cartoes/{codigo}/mover?codigo_quadro={codigo_quadro}`  
**Status HTTP:** `200 OK` | `409 Conflict (WIP)` | `404 Not Found`

---

#### US-13 — Editar Cartão

**Como** Marina,  
**Quero** editar os atributos de um cartão existente,  
**Para que** eu possa corrigir informações ou atualizar o responsável.

**Critérios de Aceitação:**

- [ ] Um botão de edição é acessível em cada cartão (ex: ícone de lápis)
- [ ] É possível editar: nome, descrição, responsável, prioridade e data limite
- [ ] O código do cartão não pode ser alterado após a criação
- [ ] As mesmas regras de validação da criação se aplicam à edição
- [ ] As alterações são refletidas imediatamente na interface

**Endpoint:** `PUT /cartoes/{codigo}?codigo_quadro={codigo_quadro}`  
**Status HTTP:** `200 OK` | `404 Not Found` | `422 Unprocessable Entity`

---

#### US-14 — Excluir Cartão

**Como** Carlos,  
**Quero** excluir um cartão que foi criado por engano,  
**Para que** o quadro não tenha tarefas desnecessárias.

**Critérios de Aceitação:**

- [ ] Um botão de exclusão é acessível em cada cartão
- [ ] Um modal de confirmação é exibido antes da exclusão
- [ ] Após exclusão, o status do quadro é recalculado
- [ ] O cartão removido deixa de aparecer imediatamente na interface

**Endpoint:** `DELETE /cartoes/{codigo}?codigo_quadro={codigo_quadro}`  
**Status HTTP:** `204 No Content` | `404 Not Found`

---

### EP-04: Gestão de Raias

---

#### US-19 — Criar Raia

**Como** Carlos,  
**Quero** criar uma nova raia em um quadro,  
**Para que** eu possa estruturar visualmente o trabalho por responsável.

**Critérios de Aceitação:**

- [ ] Apenas membros do quadro podem criar raias
- [ ] O nome da raia segue regras de texto (5–30 chars, inicial maiúscula)
- [ ] A raia é criada com uma ordem de exibição (`ordem_exibicao`)
- [ ] Não é permitido nome de raia duplicado no mesmo quadro

**Endpoint:** `POST /quadros/{codigo_quadro}/raias`  
**Status HTTP:** `201 Created` | `409 Conflict` | `422 Unprocessable Entity`

---

#### US-20 — Visualizar Raias do Quadro

**Como** Marina,  
**Quero** visualizar as raias de um quadro,  
**Para que** eu possa entender a estrutura horizontal de trabalho.

**Critérios de Aceitação:**

- [ ] O endpoint retorna as raias ordenadas por `ordem_exibicao`
- [ ] Cada raia exibe: identificador, nome e responsável associado
- [ ] As raias retornadas pertencem somente ao quadro informado

**Endpoint:** `GET /quadros/{codigo_quadro}/raias`  
**Status HTTP:** `200 OK` | `404 Not Found`

---

#### US-21 — Editar Raia

**Como** Carlos,  
**Quero** editar os dados de uma raia,  
**Para que** eu possa ajustar nome e organização das raias ao longo do projeto.

**Critérios de Aceitação:**

- [ ] É possível alterar o nome da raia
- [ ] É possível alterar a ordem de exibição da raia
- [ ] Não é permitido gerar conflito de nome no mesmo quadro

**Endpoint:** `PUT /raias/{id_raia}`  
**Status HTTP:** `200 OK` | `404 Not Found` | `409 Conflict` | `422 Unprocessable Entity`

---

#### US-22 — Excluir Raia

**Como** Carlos,  
**Quero** excluir uma raia que não será mais usada,  
**Para que** o quadro permaneça organizado.

**Critérios de Aceitação:**

- [ ] A raia só pode ser excluída se não houver cartões vinculados a ela
- [ ] Em caso de cartões vinculados, o sistema retorna erro orientando a realocação prévia
- [ ] A exclusão remove apenas a raia selecionada

**Endpoint:** `DELETE /raias/{id_raia}`  
**Status HTTP:** `204 No Content` | `404 Not Found` | `409 Conflict`

---

#### US-23 — Mover Cartão Entre Raias

**Como** Marina,  
**Quero** mover um cartão para outra raia,  
**Para que** eu possa reatribuir trabalho entre responsáveis mantendo o histórico do cartão.

**Critérios de Aceitação:**

- [ ] O movimento entre raias ocorre por drag-and-drop vertical
- [ ] O movimento entre raias não altera automaticamente a coluna do cartão
- [ ] O cartão passa a refletir a nova raia e o novo responsável associado
- [ ] O sistema valida que a raia de destino pertence ao mesmo quadro do cartão

**Endpoint:** `PATCH /cartoes/{codigo}/mover-raia?codigo_quadro={codigo_quadro}`  
**Status HTTP:** `200 OK` | `404 Not Found` | `422 Unprocessable Entity`

---

### EP-05: Colaboração

---

#### US-15 — Convidar Membro para Quadro

**Como** Carlos,  
**Quero** convidar outros usuários cadastrados para o meu quadro,  
**Para que** eles possam colaborar nas tarefas do projeto.

**Critérios de Aceitação:**

- [ ] Apenas o DONO do quadro pode convidar membros
- [ ] O convite é feito pelo e-mail do usuário a ser convidado
- [ ] O usuário convidado deve estar cadastrado no sistema
- [ ] O dono não pode ser convidado (já pertence ao quadro)
- [ ] Um usuário já membro não pode ser convidado novamente (retorna `409`)
- [ ] Após o convite, o usuário aparece na lista de membros com papel `MEMBRO`

**Endpoint:** `POST /quadros/{codigo}/membros?email_dono={email}`  
**Status HTTP:** `201 Created` | `400 Bad Request` | `404 Not Found` | `409 Conflict`

---

#### US-16 — Visualizar Membros do Quadro

**Como** Marina,  
**Quero** ver quem são os membros de um quadro,  
**Para que** eu saiba quem está colaborando no projeto.

**Critérios de Aceitação:**

- [ ] O painel de membros exibe nome, e-mail e papel de cada participante
- [ ] O DONO aparece sempre em primeiro lugar com badge distintivo
- [ ] O painel é acessível pelo ícone 👥 na barra de navegação quando dentro de um quadro

**Endpoint:** `GET /quadros/{codigo}/membros`  
**Status HTTP:** `200 OK` | `404 Not Found`

---

#### US-17 — Remover Membro do Quadro

**Como** Carlos,  
**Quero** remover um membro do quadro,  
**Para que** eu possa controlar quem tem acesso ao projeto.

**Critérios de Aceitação:**

- [ ] Apenas o DONO pode remover membros
- [ ] O DONO não pode remover a si mesmo
- [ ] Um botão de remoção (✕) aparece ao lado de cada MEMBRO no painel (não ao lado do DONO)
- [ ] A remoção é imediata após confirmação

**Endpoint:** `DELETE /quadros/{codigo}/membros/{email_usuario}?email_dono={email}`  
**Status HTTP:** `204 No Content` | `403 Forbidden` | `404 Not Found`

---

### EP-06: Métricas e Análise

---

#### US-18 — Visualizar Métricas de Fluxo

**Como** Carlos,  
**Quero** ver métricas de fluxo do quadro com recorte temporal,  
**Para que** eu possa identificar gargalos e melhorar o processo da equipe.

**Critérios de Aceitação:**

- [ ] O endpoint de métricas retorna: lead time, cycle time, throughput e WIP atual
- [ ] Lead time = `concluido_em − criado_em`
- [ ] Cycle time = `concluido_em − iniciado_em`
- [ ] Throughput 7d = quantidade de cartões com `concluido_em` nos últimos 7 dias (janela móvel)
- [ ] Throughput diário médio = `Throughput 7d / 7`
- [ ] WIP atual = quantidade de cartões na coluna `FAZENDO`
- [ ] Apenas cartões que já passaram por `FAZENDO` possuem cycle time definido
- [ ] Cartões ainda não concluídos não entram no cálculo de lead time, cycle time e throughput

**Endpoint:** `GET /cartoes/quadro/{codigo_quadro}/metricas`  
**Status HTTP:** `200 OK`

---

## 4. Mapeamento Épicos × Histórias × Endpoints

| História | Épico | Endpoint Principal                                        | Método   |
|----------|-------|----------------------------------------------------------|----------|
| US-01    | EP-01 | `/auth/cadastrar`                                        | POST     |
| US-02    | EP-01 | `/auth/login`                                            | POST     |
| US-03    | EP-01 | (client-side)                                            | —        |
| US-04    | EP-01 | `/contas/{email}`                                        | PUT      |
| US-05    | EP-01 | `/contas/{email}`                                        | DELETE   |
| US-06    | EP-02 | `/quadros/`                                              | POST     |
| US-07    | EP-02 | `/quadros/`                                              | GET      |
| US-08    | EP-02 | `/quadros/{codigo}/status`                               | PATCH    |
| US-09    | EP-02 | `/quadros/{codigo}`                                      | DELETE   |
| US-10    | EP-03 | `/cartoes/`                                              | POST     |
| US-11    | EP-03 | `/cartoes/quadro/{codigo_quadro}`                        | GET      |
| US-12    | EP-03 | `/cartoes/{codigo}/mover`                                | PATCH    |
| US-13    | EP-03 | `/cartoes/{codigo}`                                      | PUT      |
| US-14    | EP-03 | `/cartoes/{codigo}`                                      | DELETE   |
| US-15    | EP-05 | `/quadros/{codigo}/membros`                              | POST     |
| US-16    | EP-05 | `/quadros/{codigo}/membros`                              | GET      |
| US-17    | EP-05 | `/quadros/{codigo}/membros/{email_usuario}`              | DELETE   |
| US-18    | EP-06 | `/cartoes/quadro/{codigo_quadro}/metricas`               | GET      |
| US-19    | EP-04 | `/quadros/{codigo_quadro}/raias`                         | POST     |
| US-20    | EP-04 | `/quadros/{codigo_quadro}/raias`                         | GET      |
| US-21    | EP-04 | `/raias/{id_raia}`                                       | PUT      |
| US-22    | EP-04 | `/raias/{id_raia}`                                       | DELETE   |
| US-23    | EP-04 | `/cartoes/{codigo}/mover-raia`                           | PATCH    |

---

## 5. Backlog Priorizado (MoSCoW)

| Prioridade | Histórias                                        |
|:----------:|--------------------------------------------------|
| **Must Have** | US-01, US-02, US-06, US-10, US-11, US-12     |
| **Should Have** | US-03, US-04, US-07, US-08, US-13, US-14, US-15, US-16, US-19, US-20, US-23 |
| **Could Have** | US-05, US-17, US-18, US-21, US-22           |
| **Won't Have (v1)** | Notificações, exportação, comentários   |


## Link
https://docs.google.com/document/d/145Gvsj7Ux2V33LvDlRKBWVVg8JULmQ5JnkGJ2ia4RiQ/edit?usp=sharing