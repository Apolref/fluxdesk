# FluxDesk - Sistema de Gestão de Chamados

O **FluxDesk** é uma API REST moderna e robusta para automação de suporte técnico, desenvolvida com foco em escalabilidade, segurança e controle de acesso granular. 

Este projeto faz parte de um roadmap intensivo de desenvolvimento backend, aplicando as melhores práticas de mercado utilizadas em grandes empresas de tecnologia.

---

## Stack Tecnológica

* **Linguagem:** [Python 3.13+](https://www.python.org/)
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Alta performance e documentação automática)
* **Banco de Dados:** [PostgreSQL](https://www.postgresql.org/)
* **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
* **Migrações:** [Alembic](https://alembic.sqlalchemy.org/)
* **Segurança:** Autenticação via **OAuth2 + JWT** (JSON Web Tokens) e Hash de senhas com **Passlib**

---

## Funcionalidades Implementadas

### Segurança e Acesso
* **RBAC (Role-Based Access Control):** Diferenciação de permissões entre `cliente`, `tecnico` e `admin`.
* **Tokens Expiráveis:** Gestão de sessão segura via JWT.

### Gestão de Tickets
* **Fluxo de Vida:** Criação, atribuição de técnicos e atualização de status (Aberto, Em Atendimento, Fechado).
* **Comentários & Histórico:** Sistema de chat interno em cada chamado para troca de informações.
* **Logs Automáticos:** O sistema registra automaticamente no histórico do ticket sempre que um técnico altera o status.

---

## Como Executar o Projeto

### 1. Preparar o Ambiente
Certifique-se de ter o Python e o PostgreSQL instalados (ou utilize o Docker).

```bash
# Clone o repositório
git clone [https://github.com/Apolref/fluxdesk.git](https://github.com/Apolref/fluxdesk.git)
cd fluxdesk

# Crie e ative o ambiente virtual
python -m venv venv
./venv/Scripts/activate  # Windows
source venv/bin/activate # Linux/Mac

# Instale as dependências
pip install -r requirements.txt