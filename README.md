# 📋 Frequência QR

Sistema distribuído de controle de frequência em sala de aula utilizando QR Code.

Desenvolvido como trabalho da disciplina de **Sistemas Distribuídos** — UFVJM.

---

## 📌 Sobre o projeto

O sistema permite que professores gerem QR Codes únicos para cada aula e que alunos registrem presença escaneando o código com seus dispositivos móveis.

O registro de presença só é aceito quando **todas** as validações abaixo passam:

- ✅ Aluno autenticado via Google
- ✅ Token do QR Code válido
- ✅ Horário dentro da janela da aula (±15 minutos)
- ✅ IP dentro da rede institucional
- ✅ Geolocalização dentro do raio permitido da sala

---

## 🛠️ Tecnologias

- **Python 3.12+**
- **Django 6.x**
- **Django REST Framework**
- **django-allauth** (autenticação com Google OAuth2)
- **PostgreSQL**
- **Tailwind CSS** (via CDN)

---

## ✅ Pré-requisitos

Certifique-se de ter instalado:

- Python 3.12+
- PostgreSQL 15+
- Git

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/frequencia_qr.git
cd frequencia_qr
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Acesse o PostgreSQL como superusuário:

```bash
sudo -u postgres psql
```

Execute os comandos abaixo:

```sql
CREATE DATABASE frequencia_db;
CREATE USER frequencia_user WITH PASSWORD 'suasenha';
ALTER ROLE frequencia_user SET client_encoding TO 'utf8';
ALTER ROLE frequencia_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE frequencia_USER SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE frequencia_db TO frequencia_user;
\c frequencia_db
GRANT ALL ON SCHEMA public TO frequencia_user;
ALTER SCHEMA public OWNER TO frequencia_user;
\q
```

### 5. Configure as variáveis de ambiente

Crie o arquivo `.env` na raiz do projeto:

```bash
cp .env.example .env
```

Edite o `.env` com seus dados:

```env
SECRET_KEY=django-insecure-troque-isso-por-uma-chave-forte
DEBUG=True
DB_NAME=frequencia_db
DB_USER=frequencia_user
DB_PASSWORD=suasenha
DB_HOST=localhost
DB_PORT=5432
```

> ⚠️ Nunca compartilhe o arquivo `.env` nem o envie para o repositório.

### 6. Aplique as migrações

```bash
python manage.py migrate
```

### 7. Crie o superusuário

```bash
python manage.py createsuperuser
```

### 8. Suba o servidor

```bash
python manage.py runserver
```

Acesse **http://127.0.0.1:8000**

---

## 🔑 Configurando o Login com Google

O sistema utiliza autenticação OAuth2 com o Google. Siga os passos abaixo para configurar:

### 1. Crie as credenciais no Google Cloud Console

1. Acesse [https://console.cloud.google.com](https://console.cloud.google.com)
2. Crie um novo projeto chamado `frequencia-qr`
3. Vá em **APIs e Serviços → Tela de consentimento OAuth**, escolha **Externo** e preencha as informações básicas
4. Vá em **APIs e Serviços → Credenciais → Criar Credenciais → ID do cliente OAuth**
5. Escolha **Aplicativo da Web** e configure:
   - **Origens JavaScript autorizadas:** `http://127.0.0.1:8000`
   - **URIs de redirecionamento autorizados:** `http://127.0.0.1:8000/accounts/google/login/callback/`
6. Salve e copie o **Client ID** e o **Client Secret**

### 2. Cadastre as credenciais no admin do Django

1. Acesse **http://127.0.0.1:8000/admin/socialaccount/socialapp/add/**
2. Preencha:
   - **Provider:** Google
   - **Name:** Google
   - **Client ID:** seu Client ID
   - **Secret key:** seu Client Secret
   - **Sites:** mova `example.com` para **Sites escolhidos**
3. Salve

Pronto! O botão **Entrar com Google** já estará funcional na tela de login.

---

## 👤 Tipos de usuário

| Tipo | Permissões |
|------|------------|
| **Admin** | Acesso total ao sistema |
| **Professor** | Gerencia suas próprias disciplinas e aulas, visualiza presenças |
| **Aluno** | Registra presença via QR Code, visualiza seu histórico |

> Novos usuários que fazem login pelo Google recebem automaticamente o tipo **Aluno**. Um administrador pode alterar o tipo pelo painel admin.

---

## 📱 Fluxo de registro de presença

1. O professor cria uma aula — o QR Code é gerado automaticamente
2. O professor exibe ou imprime o QR Code em sala
3. O aluno escaneia o QR Code com o celular
4. O sistema solicita login (se não estiver autenticado)
5. O sistema solicita permissão de geolocalização
6. O sistema valida horário, rede e localização
7. A presença é registrada e o aluno vê a confirmação

---

## 🌐 API REST

A API está disponível em `/api/`. Endpoints disponíveis:

### Públicos (sem autenticação)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/disciplinas/` | Lista todas as disciplinas |
| GET | `/api/professores/` | Lista todos os professores |
| GET | `/api/aulas/` | Lista todas as aulas |

### Restritos (requer autenticação)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET/POST | `/api/alunos/` | Lista e cria alunos |
| GET/PUT/DELETE | `/api/alunos/<id>/` | Detalhe de aluno |
| GET/POST | `/api/aulas/gerenciar/` | Lista e cria aulas |
| GET/PUT/DELETE | `/api/aulas/gerenciar/<id>/` | Detalhe de aula |
| GET/POST | `/api/presencas/` | Lista e cria presenças |

---

## 📁 Estrutura do projeto

```
frequencia_qr/
├── core/               # Configurações do projeto
├── usuarios/           # App de autenticação e perfis
├── aulas/              # App de disciplinas, salas e aulas
├── presencas/          # App de registro de presença
├── api/                # Endpoints da API REST
├── templates/          # Templates HTML
├── static/             # Arquivos estáticos
├── media/              # QR Codes gerados
├── .env.example        # Exemplo de variáveis de ambiente
├── requirements.txt    # Dependências do projeto
└── manage.py
```

---

## 🔒 Segurança

- Senhas nunca são armazenadas — autenticação exclusiva via Google OAuth2
- Tokens de QR Code são UUIDs únicos e gerados automaticamente
- Todas as ações do sistema são registradas em log de auditoria
- Presença só é registrada mediante validação simultânea de horário, rede e geolocalização

---

## 📝 Licença

Projeto acadêmico desenvolvido para a disciplina de Sistemas Distribuídos — UFVJM.
