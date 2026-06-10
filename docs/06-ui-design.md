# Projeto de Interface com o Usuário (UI Design)

**Sistema:** Kanban Web  
**Disciplina:** Engenharia de Software — UnB  
**Versão:** 1.0  
**Data:** 2026-05-11

---

## 1. Princípios de Design

O design da interface do Kanban Web segue os seguintes princípios:

| Princípio           | Aplicação no Sistema                                                         |
|---------------------|------------------------------------------------------------------------------|
| **Minimalismo**     | Apenas controles necessários expostos; design limpo sem sobrecarga visual    |
| **Feedback imediato**| Toast notifications para toda ação; destaque visual no drag-and-drop        |
| **Consistência**    | Mesma paleta, tipografia e componentes em toda a aplicação                   |
| **Prevenção de erros**| Hints de validação abaixo de cada campo; disable de botão WIP atingido    |
| **Acessibilidade**  | Contraste de cor adequado; labels semânticos; suporte a foco de teclado     |

---

## 2. Sistema de Design

### 2.1 Paleta de Cores

| Token                  | Cor Hex   | Uso                                           |
|------------------------|-----------|-----------------------------------------------|
| `indigo-700`           | `#4338CA` | Navbar, botões primários, destaques           |
| `indigo-600`           | `#4F46E5` | Hover de botões primários                     |
| `indigo-200`           | `#C7D2FE` | Avatar de membro, badges de DONO              |
| `gray-100`             | `#F3F4F6` | Fundo da aplicação, tabs inativas             |
| `gray-700`             | `#374151` | Texto principal                               |
| `green-600`            | `#16A34A` | Toast de sucesso, coluna "FEITO"              |
| `red-600`              | `#DC2626` | Toast de erro, botão confirmar exclusão       |
| `yellow-100`           | `#FEF9C3` | Coluna "EM TESTE" (Kanban de cartões)         |
| `blue-100`             | `#DBEAFE` | Coluna "FAZENDO" (Kanban de cartões)          |
| `white`                | `#FFFFFF` | Superfícies de cards e modais                 |

**Prioridade de Cartão (Badge):**

| Prioridade | Cor de fundo  | Cor de texto  |
|------------|---------------|---------------|
| ALTA       | `red-100`     | `red-700`     |
| MEDIA      | `yellow-100`  | `yellow-700`  |
| BAIXA      | `green-100`   | `green-700`   |

### 2.2 Tipografia

| Uso                    | Tailwind          | Especificação                  |
|------------------------|-------------------|--------------------------------|
| Título principal       | `text-2xl font-bold` | 24px, weight 700            |
| Título de seção        | `text-xl font-bold`  | 20px, weight 700            |
| Texto de corpo         | `text-sm`            | 14px, weight 400            |
| Label de campo         | `text-xs font-semibold uppercase tracking-wide` | 12px, caps |
| Hint de validação      | `text-xs text-gray-400` | 12px, cor suave           |
| Código de item         | `font-mono text-xs`  | Monoespaçada, 12px           |

### 2.3 Componentes Base

#### Botão Primário
```html
<button class="bg-indigo-600 hover:bg-indigo-700 text-white
               px-4 py-2 rounded-lg text-sm font-medium">
  Ação Principal
</button>
```

#### Botão Secundário (Cancelar)
```html
<button class="px-4 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 text-sm">
  Cancelar
</button>
```

#### Botão Destrutivo (Excluir)
```html
<button class="bg-red-600 hover:bg-red-700 text-white
               px-4 py-2 rounded-lg text-sm">
  Confirmar Exclusão
</button>
```

#### Campo de Texto
```html
<input class="w-full border rounded-lg px-3 py-2 text-sm
              focus:outline-none focus:ring-2 focus:ring-indigo-400" />
```

#### Badge de Status / Papel
```html
<span class="text-xs px-2 py-0.5 rounded-full font-medium
             bg-indigo-100 text-indigo-700">DONO</span>
```

---

## 3. Wireframes das Telas

### 3.1 Tela de Login / Cadastro

```
┌─────────────────────────────────────────────┐
│                                             │
│                                             │
│         ┌───────────────────────┐           │
│         │       Kanban          │           │
│         │  ┌────────┬────────┐  │           │
│         │  │ Login  │Cadastro│  │           │  ← Tabs
│         │  └────────┴────────┘  │           │
│         │                       │           │
│         │  [Email          ]    │           │
│         │                       │           │
│         │  [Senha (5 chars)]👁  │           │  ← Toggle ver senha
│         │                       │           │
│         │  [    Entrar     ]     │           │  ← Botão primário
│         └───────────────────────┘           │
│                                             │
└─────────────────────────────────────────────┘
```

**Comportamento:**
- Tab ativa tem fundo branco com sombra; inativa tem fundo cinza
- Erro de credenciais exibe toast vermelho na parte inferior direita
- Campos submetidos com Enter (`@submit.prevent`)

---

### 3.2 Tela de Cadastro

```
┌─────────────────────────────────────────────┐
│         ┌───────────────────────┐           │
│         │       Kanban          │           │
│         │  [  Login  ][Cadastro]│           │
│         │  ─────────────────── │           │
│         │  [Nome            ]  │           │
│         │   5–30 chars...      │           │  ← Hints abaixo
│         │                      │           │
│         │  [Email           ]  │           │
│         │   Apenas letras...   │           │
│         │                      │           │
│         │  [Senha      ] 👁    │           │
│         │   5 chars únicos...  │           │
│         │                      │           │
│         │  [ Criar Conta ]     │           │
│         └───────────────────────┘           │
└─────────────────────────────────────────────┘
```

---

### 3.3 Navbar (Barra de Navegação)

```
┌──────────────────────────────────────────────────────────────────┐
│ Kanban / Nome do Quadro  │  Nome.do.user  [👥 Membros 3] [← Projetos] [Sair] │
└──────────────────────────────────────────────────────────────────┘
```

| Elemento              | Visibilidade           | Ação                           |
|-----------------------|------------------------|--------------------------------|
| Logo "Kanban"         | Sempre                 | —                              |
| "/ Nome do Quadro"    | Dentro de um quadro    | —                              |
| Nome do usuário       | Autenticado            | Abre modal de perfil           |
| Botão 👥 Membros      | Dentro de um quadro    | Abre painel de membros         |
| Botão ← Projetos      | Dentro de um quadro    | Retorna ao painel de projetos  |
| Botão Sair            | Autenticado            | Logout                         |

---

### 3.4 Tela Principal — Kanban de Projetos

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Kanban                                                    Pedro  [Sair]  │
├──────────────────────────────────────────────────────────────────────────┤
│  Meus Projetos                              [+ Novo Projeto]             │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │   A FAZER    │  │ EM ANDAMENTO │  │  EM TESTES   │  │  CONCLUIDO  │ │
│  │──────────────│  │──────────────│  │──────────────│  │─────────────│ │
│  │ ┌──────────┐ │  │ ┌──────────┐ │  │              │  │             │ │
│  │ │ AB12     │ │  │ │ CD34     │ │  │              │  │             │ │
│  │ │ Projeto  │ │  │ │ Projeto  │ │  │    Vazio     │  │   Vazio     │ │
│  │ │ Alpha    │ │  │ │ Beta     │ │  │              │  │             │ │
│  │ │ WIP: 10  │ │  │ │ WIP: 5   │ │  │              │  │             │ │
│  │ │ [🗑 Del] │ │  │ │ [🗑 Del] │ │  │              │  │             │ │
│  │ └──────────┘ │  │ └──────────┘ │  │              │  │             │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └─────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
```

**Comportamento:**
- Clique no card do quadro → abre o Kanban de Cartões daquele quadro
- Botão 🗑 Deletar → abre modal de confirmação (apenas para o dono)
- Arrastar card entre colunas → atualiza status via `PATCH /quadros/{codigo}/status`
- Coluna de destino destaca com borda pontilhada ao arrastar sobre ela

---

### 3.5 Tela de Kanban de Cartões

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ Kanban / Projeto Alpha                Pedro 👥 Membros 3  [← Projetos] [Sair]     │
├────────────────────────────────────────────────────────────────────────────────────┤
│                     COLUNAS                                                     │
│             A FAZER     FAZENDO     EM TESTE      FEITO                         │
│┌──────────┬───────────────────────────────────────────────────────────────────────┐│
││ Raia     │                                                                       ││
│├──────────┼───────────────────────────────────────────────────────────────────────┤│
││ Pedro    │ [CD34][EF56]  [ ]         [ ]           [ ]                          ││
││ (2 itens)│                                                                       ││
│├──────────┼───────────────────────────────────────────────────────────────────────┤│
││ Ana      │ [ ]          [GH78]      [ ]           [ ]                           ││
││ (1 item) │                                                                       ││
│├──────────┼───────────────────────────────────────────────────────────────────────┤│
││ João     │ [ ]          [ ]         [IJ90]        [KL12]                        ││
││ (2 itens)│                                                                       ││
│└──────────┴───────────────────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────────────────────────┘
```

**Comportamento:**
- `(2/10)` indica cartões atuais / limite WIP da coluna
- Quando coluna está cheia, o número fica vermelho
- Botão `[+ Novo Cartão]` permite escolher coluna inicial e raia inicial
- Drag-and-drop horizontal muda coluna; drag-and-drop vertical muda raia
- Cada interseção coluna x raia é uma drop zone independente
- Cabeçalho da raia mostra responsável e quantidade total de cartões na raia
- ✏ abre modal de edição; 🗑 abre modal de confirmação de exclusão

### 3.5.1 Gestão de Raias no Layout

- Botão `+ Nova Raia` visível no topo da grade para criar raia
- Menu de contexto da raia com ações `Editar` e `Excluir`
- Excluir raia com cartões vinculados exibe erro orientando realocação prévia

---

### 3.6 Modal de Criação / Edição de Cartão

```
┌─────────────────────────────────────────────┐
│  Novo Cartão                                │
│  ─────────────────────────────────────────  │
│  [Código (ex: CD34)              ]          │
│   2 letras maiúsculas + 2 dígitos           │
│                                             │
│  [Nome da tarefa                 ]          │
│   5–30 chars, iniciar com maiúscula         │
│                                             │
│  [Descrição da tarefa            ]          │
│   5–30 chars, iniciar com maiúscula         │
│                                             │
│  [▼ Selecione o Responsável      ]          │
│                                             │
│  [▼ Prioridade: Média            ]          │
│                                             │
│  [Data Limite: dd/mm/aaaa   📅  ]           │
│                                             │
│  ⚠ Mensagem de erro (se houver)            │
│                                             │
│                  [Cancelar] [Criar Cartão]  │
└─────────────────────────────────────────────┘
```

**Comportamento:**
- Campo "Código" oculto no modo edição (código imutável)
- Dropdown "Responsável" populado com os membros do quadro via `GET /quadros/{codigo}/membros`
- Erros de validação do backend exibidos no campo `⚠` dentro do modal
- Botão confirmar desativado enquanto a requisição está em andamento

---

### 3.7 Modal de Membros

```
┌─────────────────────────────────────────────┐
│  Membros do Projeto                         │
│  ─────────────────────────────────────────  │
│  Convidar por email  (visível apenas ao dono│
│  [email@dominio.com          ] [Convidar]   │
│                                             │
│  Membros do projeto                         │
│  ┌─────────────────────────────────────┐   │
│  │  P  Pedro Alves        DONO         │   │
│  │     pedro@unb.br                    │   │
│  ├─────────────────────────────────────┤   │
│  │  A  Ana Costa          MEMBRO  [✕]  │   │
│  │     ana@unb.br                      │   │
│  ├─────────────────────────────────────┤   │
│  │  J  João Silva         MEMBRO  [✕]  │   │
│  │     joao@unb.br                     │   │
│  └─────────────────────────────────────┘   │
│                              [Fechar]       │
└─────────────────────────────────────────────┘
```

**Comportamento:**
- Avatares circulares com inicial do nome em indigo
- Botão ✕ visível apenas ao dono e não aparece ao lado do próprio dono
- Scroll vertical quando há muitos membros (max-height definido)

---

### 3.8 Sistema de Toast (Notificações)

```
                                    ┌──────────────────────────┐
                                    │ ✓ Cartão criado com      │
                                    │   sucesso                │ ← Verde (sucesso)
                                    └──────────────────────────┘

                                    ┌──────────────────────────┐
                                    │ ✕ Limite WIP atingido    │
                                    │   na coluna 'FAZENDO'    │ ← Vermelho (erro)
                                    └──────────────────────────┘
```

**Especificação:**
- Posição: canto inferior direito (`fixed bottom-6 right-6`)
- Duração: 3 segundos
- Animação: fade in (slide-up 300ms) / fade out (200ms)
- Máximo de 1 toast visível por vez (o último sobrescreve)

---

## 4. Fluxo de Navegação

```
                    ┌──────────────────┐
                    │  Tela de Login   │
                    │   / Cadastro     │
                    └────────┬─────────┘
                             │ Login bem-sucedido
                             ▼
                    ┌──────────────────┐
                    │ Painel de        │◀──── ← Projetos
                    │ Projetos (Quadros│
                    └────────┬─────────┘
                             │ Click no quadro
                             ▼
                    ┌──────────────────┐
                    │ Kanban de Cartões│
                    │  (dentro quadro) │
                    │  ┌───────────┐   │
                    │  │👥 Membros │   │ → Painel Membros (modal)
                    │  └───────────┘   │
                    │  ┌───────────┐   │
                    │  │ Nome user │   │ → Modal Perfil
                    │  └───────────┘   │
                    └──────────────────┘
```

---

## 5. Estados de Interface

### 5.1 Estado Vazio
- Células coluna x raia sem cartões exibem área clicável com texto "+  Adicionar cartão"
- Painel de projetos sem quadros exibe mensagem "Nenhum projeto ainda. Clique em + Novo Projeto."

### 5.2 Estado de Carregamento
- Requisições à API desabilitam o botão de confirmação
- Não há spinner explícito (a resposta é rápida com SQLite local)

### 5.3 Estado de Erro
- Erros de validação aparecem dentro do modal no campo vermelho destacado
- Erros de rede ou servidor aparecem como toast vermelho
- Erro 403 (sem permissão): toast "Você não tem permissão para esta ação"
- Erro 409 (WIP): toast "Limite WIP atingido na coluna '...'"

### 5.4 Estado de Arrastar (Drag-and-Drop)
- Cursor muda para `grab` ao passar sobre um cartão
- Cursor muda para `grabbing` ao clicar e arrastar
- Opacidade do cartão em arraste cai para 70%
- Célula de destino (coluna x raia) recebe `outline: 2px dashed #6366f1` e fundo azul claro

---

## 6. Responsividade

| Breakpoint | Layout                                               |
|------------|------------------------------------------------------|
| < 640px (mobile) | Raias em acordeão; colunas por raia em scroll horizontal |
| 640–1024px (tablet) | Matriz reduzida com cabeçalhos fixos de coluna e raia |
| > 1024px (desktop) | Matriz completa coluna x raia (layout padrão) |

Tailwind CSS gerencia os breakpoints via classes utilitárias responsivas (`sm:`, `md:`, `lg:`).

## Link
https://docs.google.com/document/d/1FWlPFiwcXTkyFTqmgb4l1-WuBL-sM40wgCSYkXd64l4/edit?usp=sharing