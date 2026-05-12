# Descrição do Processo de Gerenciamento — Kanban Web

**Disciplina:** Engenharia de Software — UnB  
**Versão:** 1.0  
**Data:** 2026-05-11

---

## 1. Visão Geral do Processo

O sistema Kanban Web implementa um processo de gerenciamento visual de tarefas baseado no método Kanban. O método organiza o trabalho em um quadro dividido em colunas que representam estágios do fluxo produtivo. Cada unidade de trabalho é representada por um **cartão**, que percorre as colunas da esquerda para a direita até ser concluído.

O processo é colaborativo: um **dono** cria o quadro e convida **membros**. Todos os membros podem criar, mover e visualizar cartões dentro de qualquer quadro ao qual pertencem.

---

## 2. Estrutura do Quadro

### 2.1 Identificação

| Atributo       | Formato          | Descrição                                           |
|----------------|------------------|-----------------------------------------------------|
| `codigo`       | 2 letras + 2 dígitos (ex: `AB12`) | Identificador único global do quadro |
| `nome`         | 5–30 chars, inicial maiúscula | Nome descritivo do projeto             |
| `descricao`    | 5–30 chars, inicial maiúscula | Resumo do objetivo do quadro           |
| `limite_wip`   | 5, 10, 15 ou 20  | Número máximo de cartões por coluna (Work-In-Progress) |
| `email_dono`   | e-mail válido    | Responsável pelo quadro                             |
| `status`       | enum (ver §2.3)  | Estado atual calculado automaticamente              |

### 2.2 Colunas do Quadro

O quadro possui quatro colunas fixas, representando o ciclo de vida de cada tarefa:

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│   A FAZER   │──▶│   FAZENDO   │──▶│  EM TESTE   │──▶│    FEITO    │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
```

| Coluna     | Significado                                              | Cor de referência |
|------------|----------------------------------------------------------|-------------------|
| `A FAZER`  | Tarefas planejadas, ainda não iniciadas                  | Cinza / Branco    |
| `FAZENDO`  | Tarefas em execução ativa                                | Azul / Índigo     |
| `EM TESTE` | Tarefas concluídas em desenvolvimento, aguardando revisão| Amarelo / Âmbar   |
| `FEITO`    | Tarefas completamente revisadas e aceitas                | Verde             |

### 2.3 Status Derivado do Quadro

O status do quadro é **calculado automaticamente** pelo sistema sempre que um cartão é movido ou removido, com base nas colunas dos seus cartões:

| Condição                                              | Status do Quadro   |
|-------------------------------------------------------|--------------------|
| Todos os cartões em `A FAZER`                         | `A FAZER`          |
| Cartões distribuídos em colunas distintas             | `EM ANDAMENTO`     |
| Todos os cartões em `EM TESTE` ou `FEITO`             | `EM TESTES`        |
| Todos os cartões em `FEITO`                           | `CONCLUIDO`        |
| Quadro sem cartões                                    | não alterado       |

### 2.4 Controle WIP (Work-In-Progress)

O limite WIP impõe uma restrição ao número máximo de cartões simultâneos em qualquer coluna. Ao tentar mover um cartão para uma coluna que já atingiu o limite, o sistema retorna erro `409 Conflict`. Isso força a equipe a finalizar tarefas antes de iniciar novas, reduzindo o desperdício por multitarefa excessiva.

Valores permitidos de WIP: **5**, **10**, **15**, **20**.

---

## 3. Estrutura do Cartão

### 3.1 Atributos

| Atributo       | Tipo / Formato                     | Obrigatório | Descrição                                         |
|----------------|------------------------------------|-------------|---------------------------------------------------|
| `codigo`       | 2 letras + 2 dígitos (ex: `CD34`)  | Sim         | Identificador do cartão (único dentro do quadro)  |
| `codigo_quadro`| String(4), FK → `quadros.codigo`   | Sim         | Quadro ao qual o cartão pertence                  |
| `nome`         | 5–30 chars, inicial maiúscula      | Sim         | Título da tarefa                                  |
| `descricao`    | 5–30 chars, inicial maiúscula      | Sim         | Detalhamento da tarefa                            |
| `responsavel`  | Nome de um membro do quadro        | Sim         | Pessoa responsável pela execução                  |
| `prioridade`   | `BAIXA`, `MEDIA`, `ALTA`           | Sim         | Nível de urgência do cartão                       |
| `data_limite`  | Date (YYYY-MM-DD)                  | Não         | Prazo máximo para conclusão                       |
| `coluna`       | `A FAZER`, `FAZENDO`, `EM TESTE`, `FEITO` | Sim  | Estágio atual no fluxo                            |
| `criado_em`    | DateTime UTC                       | Auto        | Momento em que o cartão foi criado                |
| `iniciado_em`  | DateTime UTC                       | Auto        | Momento em que o cartão foi movido para `FAZENDO` |
| `concluido_em` | DateTime UTC                       | Auto        | Momento em que o cartão foi movido para `FEITO`   |

### 3.2 Ciclo de Vida do Cartão

```
[Criação]
    │
    ▼
A FAZER ──── mover ──▶ FAZENDO ──── mover ──▶ EM TESTE ──── mover ──▶ FEITO
    │              (registra           │                        │
    │           iniciado_em)           │                  (registra
    │                                  │                 concluido_em)
    └──── excluir a qualquer momento ──┘
```

- `iniciado_em` é registrado **na primeira vez** que o cartão entra na coluna `FAZENDO`.
- `concluido_em` é registrado **na primeira vez** que o cartão entra na coluna `FEITO`.
- Ambos os carimbos de tempo são imutáveis após definidos.

### 3.3 Prioridades

| Prioridade | Uso recomendado                                       |
|------------|-------------------------------------------------------|
| `ALTA`     | Bloqueio de outros trabalhos; prazo iminente          |
| `MEDIA`    | Tarefa importante mas com folga de tempo              |
| `BAIXA`    | Melhoria ou tarefa de backlog sem urgência            |

---

## 4. Papéis e Permissões

| Ação                            | DONO | MEMBRO |
|---------------------------------|:----:|:------:|
| Criar quadro                    |  ✓   |   —    |
| Excluir quadro                  |  ✓   |   —    |
| Convidar membros                |  ✓   |   —    |
| Remover membros                 |  ✓   |   —    |
| Criar cartões                   |  ✓   |   ✓    |
| Mover cartões                   |  ✓   |   ✓    |
| Editar cartões                  |  ✓   |   ✓    |
| Excluir cartões                 |  ✓   |   ✓    |
| Visualizar quadro e cartões     |  ✓   |   ✓    |

---

## 5. Fluxo de Trabalho Detalhado

### 5.1 Criação de Conta e Autenticação

1. O usuário acessa `http://127.0.0.1:8000/`.
2. Seleciona a aba **Cadastro** e preenche nome, e-mail e senha.
3. O sistema valida as regras de domínio (ver §6) e cria a conta.
4. O usuário realiza login com e-mail e senha.
5. A sessão é armazenada em `localStorage` no navegador.

### 5.2 Gestão de Projetos (Quadros)

1. Após login, o usuário vê o **Kanban de Projetos**: quatro colunas correspondentes aos status possíveis de quadro.
2. O usuário clica em **+ Novo Projeto** para criar um quadro.
3. Preenche código, nome, descrição e limite WIP.
4. O quadro aparece na coluna `A FAZER` do Kanban de Projetos.
5. Ao avançar os cartões internos, o status do quadro muda automaticamente.
6. O dono pode excluir o quadro; todos os cartões são cascadeados.

### 5.3 Gestão de Tarefas (Cartões)

1. O usuário clica em um quadro para abrí-lo.
2. Visualiza o **Kanban de Cartões** com as quatro colunas de tarefa.
3. Clica em **+ Novo Cartão** para adicionar uma tarefa.
4. Preenche código, nome, descrição, responsável, prioridade e data limite.
5. Move o cartão arrastando-o (drag-and-drop) entre as colunas.
6. O sistema verifica o limite WIP antes de aceitar o movimento.
7. O cartão pode ser editado ou excluído em qualquer momento.

### 5.4 Colaboração

1. O dono abre o painel **Membros** (ícone 👥 na barra de navegação).
2. Digita o e-mail de um usuário cadastrado e clica em **Convidar**.
3. O membro passa a ter acesso ao quadro em sua própria lista de projetos.
4. O dono pode remover membros a qualquer momento.

---

## 6. Regras de Domínio e Validação

Todas as regras são validadas pelo backend (Pydantic + SQLAlchemy) independentemente do frontend.

| Campo       | Regra                                                                 |
|-------------|-----------------------------------------------------------------------|
| `codigo`    | Exatamente 4 chars: `[A-Z]{2}[0-9]{2}` (ex: `AB12`)                 |
| `nome`      | 5–30 chars; começa com maiúscula; sem espaços duplos                  |
| `descricao` | 5–30 chars; começa com maiúscula; sem espaços duplos                  |
| `email`     | Exatamente 1 `@`; parte local 2–10 chars; domínio 2–20 chars         |
| `senha`     | Exatamente 5 chars únicos; ≥1 maiúscula, ≥1 minúscula, ≥1 dígito, ≥1 pontuação (`.,;!?`) |
| `limite_wip`| Valor em {5, 10, 15, 20}                                             |
| `prioridade`| Valor em {`BAIXA`, `MEDIA`, `ALTA`}                                  |
| `coluna`    | Valor em {`A FAZER`, `FAZENDO`, `EM TESTE`, `FEITO`}                 |

---

## 7. Métricas de Fluxo (Cycle Time)

O sistema registra automaticamente três marcos temporais para cada cartão, permitindo o cálculo de métricas de desempenho do processo:

| Métrica            | Cálculo                                  | Significado                                       |
|--------------------|------------------------------------------|---------------------------------------------------|
| **Lead Time**      | `concluido_em − criado_em`               | Tempo total desde criação até conclusão           |
| **Cycle Time**     | `concluido_em − iniciado_em`             | Tempo efetivo de execução (sem espera inicial)    |
| **Tempo em espera**| `iniciado_em − criado_em`                | Quanto tempo o cartão ficou aguardando início     |

Esses dados são expostos pelo endpoint `GET /cartoes/quadro/{codigo_quadro}/metricas`.

---

## 8. Diagrama de Processo (BPMN simplificado)

```
Usuário                Sistema              Banco de Dados
   │                      │                       │
   │── Cadastrar ─────────▶                       │
   │                      │── Validar Domínios    │
   │                      │── INSERT contas ──────▶
   │◀── Conta criada ──────│                       │
   │                      │                       │
   │── Login ─────────────▶                       │
   │                      │── SELECT conta ───────▶
   │◀── Sessão iniciada ───│                       │
   │                      │                       │
   │── Criar Quadro ───────▶                      │
   │                      │── INSERT quadro ──────▶
   │◀── Quadro criado ─────│                       │
   │                      │                       │
   │── Criar Cartão ───────▶                      │
   │                      │── INSERT cartao ──────▶
   │◀── Cartão criado ─────│                       │
   │                      │                       │
   │── Mover Cartão ───────▶                      │
   │                      │── Verificar WIP ──────▶
   │                      │── UPDATE coluna ──────▶
   │                      │── UPDATE status_quadro▶
   │◀── Cartão movido ─────│                       │
```

## Link
https://docs.google.com/document/d/1LkhOIwT9gKa-4z2mxxDhM8Oml6Gz9Hjxyq-n_PsO-EE/edit?usp=sharing