# Descrição da Infraestrutura de Implantação

**Sistema:** Kanban Web  
**Disciplina:** Engenharia de Software — UnB  
**Versão:** 1.0  
**Data:** 2026-05-11

---

## 1. Visão Geral

Este documento descreve a infraestrutura necessária para implantar o Kanban Web em dois ambientes: **desenvolvimento local** (utilizado durante a disciplina) e **produção de baixo custo** (para disponibilização pública do sistema acadêmico).

---

## 2. Ambiente de Desenvolvimento Local

### 2.1 Hardware (Máquina do Desenvolvedor)

| Componente        | Requisito Mínimo             | Recomendado                     |
|-------------------|------------------------------|---------------------------------|
| **Processador**   | x86-64 dual-core 1.6 GHz     | Quad-core 2.4 GHz+              |
| **Memória RAM**   | 4 GB                         | 8 GB                            |
| **Armazenamento** | 500 MB livres                | SSD com 5 GB livres             |
| **SO**            | Windows 10+, Ubuntu 20.04+, macOS 12+ | Qualquer versão suportada |
| **Rede**          | Loopback (127.0.0.1)         | —                               |

### 2.2 Software (Desenvolvimento Local)

| Componente         | Versão Mínima | Função                                              | Instalação                         |
|--------------------|---------------|-----------------------------------------------------|------------------------------------|
| **Python**         | 3.10          | Interpretador e runtime do backend                  | `python.org` ou gerenciador de SO  |
| **pip**            | 22+           | Gerenciador de pacotes Python                       | Incluído com Python                |
| **venv**           | (built-in)    | Isolamento de dependências                          | Incluído com Python                |
| **FastAPI**        | 0.110+        | Framework web do backend                            | `pip install fastapi`              |
| **Uvicorn**        | 0.29+         | Servidor ASGI (desenvolvimento com `--reload`)      | `pip install uvicorn[standard]`    |
| **SQLAlchemy**     | 2.0+          | ORM para acesso ao banco de dados                   | `pip install sqlalchemy`           |
| **Pydantic**       | 2.0+          | Validação e serialização de dados                   | `pip install pydantic`             |
| **SQLite**         | 3.x           | Banco de dados embutido                             | Incluído com Python (`sqlite3`)    |
| **Navegador**      | Chrome 110+ / Firefox 110+ | Acesso ao frontend        | —                                  |
| **Alpine.js**      | 3.x           | Framework reativo do frontend (servido localmente)  | Arquivo `static/alpinejs.min.js`   |
| **Tailwind CSS**   | 3.x           | Framework CSS utilitário (via CDN em dev)           | CDN: `https://cdn.tailwindcss.com` |

**Diagrama do Ambiente de Desenvolvimento:**

```
┌──────────────────────────────────────────────────────────────┐
│                  Máquina do Desenvolvedor                     │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │               Ambiente Virtual Python (venv)            │ │
│  │                                                         │ │
│  │   FastAPI 0.110  +  Uvicorn 0.29  +  SQLAlchemy 2.0    │ │
│  │                        │                               │ │
│  │            localhost:8000                               │ │
│  └──────────────────────┬──────────────────────────────────┘ │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────────┐ │
│  │              kanban_web/kanban.db (SQLite)               │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │               Navegador (Chrome/Firefox)                 │ │
│  │         http://127.0.0.1:8000/  →  index.html           │ │
│  │         Alpine.js (local)  +  Tailwind (CDN)            │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Ambiente de Produção (Single Server — Baixo Custo)

### 3.1 Hardware (Servidor de Produção)

| Componente        | Mínimo para Produção Acadêmica | Justificativa                              |
|-------------------|--------------------------------|--------------------------------------------|
| **vCPUs**         | 1 vCPU                         | Uvicorn single-worker suficiente para ~50 usuários |
| **Memória RAM**   | 512 MB                         | Python + SQLite + Uvicorn: ~100 MB em uso  |
| **Armazenamento** | 10 GB SSD                      | OS + Python + banco de dados com anos de dados |
| **Rede**          | 1 Gbps (compartilhada)         | Tráfego baixo (texto/JSON)                 |
| **IP**            | IP público fixo ou domínio     | Acesso externo                             |

**Provedores recomendados (custo zero / baixo):**

| Provedor           | Plano            | Custo Aproximado | Observações                              |
|--------------------|------------------|------------------|------------------------------------------|
| **Render.com**     | Free tier        | Gratuito         | Sleep após inatividade; 512 MB RAM       |
| **Railway.app**    | Starter          | ~US$ 5/mês       | Sempre ativo; 512 MB RAM                 |
| **Fly.io**         | Free tier        | Gratuito (limites) | 256 MB RAM; sem sleep                  |
| **Oracle Cloud**   | Always Free      | Gratuito         | 1 vCPU ARM, 1 GB RAM; mais robusto       |
| **Heroku**         | Eco dyno         | ~US$ 5/mês       | Histórico; boa documentação              |

### 3.2 Software (Servidor de Produção)

| Camada             | Componente        | Versão    | Função                                              |
|--------------------|-------------------|-----------|-----------------------------------------------------|
| **SO**             | Ubuntu Server     | 22.04 LTS | Sistema operacional do servidor                     |
| **Gerenciador**    | systemd           | —         | Gerenciar ciclo de vida do processo Uvicorn         |
| **Proxy reverso**  | Nginx             | 1.24+     | Servir arquivos estáticos, SSL termination, cache   |
| **Certificado SSL**| Let's Encrypt (Certbot) | —   | HTTPS gratuito; renovação automática a cada 90 dias |
| **Runtime**        | Python            | 3.11      | Interpretador do backend                            |
| **Servidor ASGI**  | Uvicorn           | 0.29+     | Servir a aplicação FastAPI                          |
| **Workers**        | Gunicorn + Uvicorn workers | — | Múltiplos workers em produção (4 recomendado)   |
| **ORM**            | SQLAlchemy        | 2.0+      | Acesso ao banco                                     |
| **Banco**          | SQLite → PostgreSQL | —       | Migrar para PostgreSQL em produção real             |

**Diagrama do Ambiente de Produção:**

```
  Internet
     │
     ▼ HTTPS :443
┌────────────────────────────────────────────────────────────┐
│                        Nginx (Proxy Reverso)               │
│   - SSL/TLS termination (Let's Encrypt)                    │
│   - Servir arquivos estáticos (/static/)                   │
│   - Proxy pass → 127.0.0.1:8000                            │
└──────────────────────────┬─────────────────────────────────┘
                           │ HTTP :8000
┌──────────────────────────▼─────────────────────────────────┐
│              Gunicorn + Uvicorn Workers                     │
│   gunicorn -k uvicorn.workers.UvicornWorker main:app        │
│   --workers 4 --bind 127.0.0.1:8000                        │
│                                                            │
│   ┌──────────────────────────────────────────────────────┐ │
│   │                   FastAPI Application                │ │
│   │   routers/ + models/ + schemas/ + database/          │ │
│   └──────────────────────┬───────────────────────────────┘ │
│                          │                                  │
│   ┌──────────────────────▼───────────────────────────────┐ │
│   │           kanban.db (SQLite) ou PostgreSQL            │ │
│   └──────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

---

## 4. Serviços Externos

| Serviço              | Uso                            | Obrigatório | URL / Nota                              |
|----------------------|--------------------------------|-------------|------------------------------------------|
| **Tailwind CDN**     | Carregar CSS em desenvolvimento| Sim (dev)   | `https://cdn.tailwindcss.com`            |
| **Let's Encrypt**    | Certificado SSL gratuito       | Sim (prod)  | Renovação automática via Certbot         |
| **Alpine.js (CDN)**  | Em dev pode usar CDN           | Não (arquivo local disponível) | `static/alpinejs.min.js` |

**Nota de Segurança:** Em produção, o Tailwind CSS deve ser compilado localmente (via `npm` + PostCSS + PurgeCSS) para eliminar dependência de CDN externo.

---

## 5. Configuração de Implantação — Passo a Passo (Ubuntu 22.04)

### 5.1 Preparar o Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.11 e pip
sudo apt install python3.11 python3.11-venv python3-pip -y

# Instalar Nginx
sudo apt install nginx -y

# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y
```

### 5.2 Implantar a Aplicação

```bash
# Clonar ou copiar o projeto
git clone <url-do-repositorio> /opt/kanban_web
cd /opt/kanban_web/kanban_web

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências + gunicorn
pip install -r requirements.txt
pip install gunicorn
```

### 5.3 Configurar Systemd Service

Criar arquivo `/etc/systemd/system/kanban.service`:

```ini
[Unit]
Description=Kanban Web - FastAPI
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/kanban_web/kanban_web
Environment="PATH=/opt/kanban_web/kanban_web/venv/bin"
ExecStart=/opt/kanban_web/kanban_web/venv/bin/gunicorn \
    -k uvicorn.workers.UvicornWorker \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    main:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable kanban
sudo systemctl start kanban
```

### 5.4 Configurar Nginx

Criar arquivo `/etc/nginx/sites-available/kanban`:

```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    location /static/ {
        alias /opt/kanban_web/kanban_web/static/;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/kanban /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5.5 Habilitar HTTPS com Let's Encrypt

```bash
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
```

---

## 6. Variáveis de Ambiente (Produção)

| Variável            | Valor Padrão (dev)            | Valor Recomendado (prod)                     |
|---------------------|-------------------------------|----------------------------------------------|
| `DATABASE_URL`      | `sqlite:///./kanban.db`       | `postgresql://user:pass@localhost/kanban`    |
| `ALLOWED_ORIGINS`   | `["*"]` (hardcoded)           | `["https://seu-dominio.com"]`               |
| `WORKERS`           | 1 (uvicorn --reload)          | 4 (gunicorn workers)                         |

Gerenciar via arquivo `.env` com `python-dotenv` (adicionar ao `requirements.txt`) ou variáveis de ambiente do systemd.

---

## 7. Monitoramento e Observabilidade

| Aspecto             | Ferramenta             | Configuração                                  |
|---------------------|------------------------|-----------------------------------------------|
| **Logs de acesso**  | Nginx access.log       | `/var/log/nginx/access.log`                   |
| **Logs de erro**    | Nginx error.log        | `/var/log/nginx/error.log`                    |
| **Logs da app**     | Uvicorn stdout         | `journalctl -u kanban -f`                     |
| **Status do processo** | systemctl          | `systemctl status kanban`                     |
| **Uptime**          | UptimeRobot (externo)  | Ping HTTP gratuito a cada 5 min               |
| **Métricas de API** | FastAPI `/docs`        | Endpoint de saúde pode ser adicionado         |

---

## 8. Backup e Recuperação

| Item                | Estratégia                                                      |
|---------------------|-----------------------------------------------------------------|
| **Banco de dados**  | Cópia diária do arquivo `kanban.db` para armazenamento externo  |
| **Código-fonte**    | Git + repositório remoto (GitHub/GitLab)                        |
| **Config Nginx**    | Versionado junto ao repositório ou backup manual               |
| **Certificado SSL** | Renovação automática pelo Certbot (cron job instalado)         |

**Script de backup diário (cron):**
```bash
# Editar com: crontab -e
0 2 * * * cp /opt/kanban_web/kanban_web/kanban.db \
             /opt/backups/kanban_$(date +\%Y\%m\%d).db
```

---

## 9. Resumo — Requisitos por Ambiente

| Requisito           | Desenvolvimento Local              | Produção (Single Server)              |
|---------------------|------------------------------------|---------------------------------------|
| **Hardware**        | Notebook pessoal (4 GB RAM)        | VPS 512 MB RAM / 1 vCPU               |
| **SO**              | Windows / Linux / macOS            | Ubuntu Server 22.04 LTS               |
| **Python**          | 3.10+                              | 3.11                                  |
| **Servidor web**    | Uvicorn `--reload`                 | Gunicorn + Uvicorn workers + Nginx    |
| **Banco de dados**  | SQLite (arquivo local)             | SQLite (acadêmico) → PostgreSQL (prod)|
| **SSL**             | Não necessário                     | Let's Encrypt (gratuito)              |
| **Domínio**         | `localhost` / `127.0.0.1`          | Domínio público registrado            |
| **Custo mensal**    | R$ 0                               | R$ 0–30 (free tier ou VPS básico)     |

## Link
https://docs.google.com/document/d/1B7df3sIMN7XgWKAmk9EcM2z_KYSpxqxD8kM02CTXQck/edit?usp=sharing