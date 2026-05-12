# PROMPT 01 — CRIAÇÃO DA ESTRUTURA INICIAL DO NEXOR ERP

Com base no arquivo de contexto principal do projeto **Nexor ERP**, crie a estrutura inicial completa do sistema.

O objetivo é gerar a base profissional do projeto, pronta para evolução futura, seguindo arquitetura modular, segura, escalável e manutenível.

---

# OBJETIVO

Criar a estrutura inicial do sistema **Nexor ERP**, contendo:

- Backend em Django + Django REST Framework
- Frontend em React + Vite + TailwindCSS
- Banco PostgreSQL
- Docker e Docker Compose
- Redis
- Celery
- Estrutura modular por domínio
- Organização preparada para autenticação JWT e RBAC
- Separação clara entre camadas

---

# REQUISITOS OBRIGATÓRIOS

A entrega deve conter:

1. Estrutura completa de pastas
2. Comandos para criação do projeto
3. Arquivos principais iniciais
4. Configuração base do backend
5. Configuração base do frontend
6. Dockerfile do backend
7. Dockerfile do frontend
8. docker-compose.yml
9. .env.example
10. requirements.txt
11. Configuração inicial do PostgreSQL
12. Configuração inicial do Redis
13. Configuração inicial do Celery
14. README.md inicial
15. Explicação técnica das decisões

---

# BACKEND

Utilizar:

- Python 3.13+
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- django-cors-headers
- python-decouple ou python-dotenv
- Celery
- Redis

Criar estrutura:

backend/
├── apps/
│   ├── accounts/
│   ├── core/
│   ├── estoque/
│   ├── compras/
│   ├── financeiro/
│   ├── fiscal/
│   ├── ordens_servico/
│   ├── clientes/
│   ├── fornecedores/
│   ├── relatorios/
│   └── auditoria/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   ├── celery.py
│   ├── wsgi.py
│   └── asgi.py
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── docker/
├── .env.example
├── manage.py
└── Dockerfile

---

# FRONTEND

Utilizar:

- React
- Vite
- TailwindCSS
- Axios
- React Router DOM

Criar estrutura:

frontend/
├── src/
│   ├── api/
│   ├── assets/
│   ├── components/
│   ├── layouts/
│   ├── pages/
│   ├── routes/
│   ├── services/
│   ├── hooks/
│   ├── contexts/
│   ├── store/
│   ├── utils/
│   ├── styles/
│   └── constants/
├── public/
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── Dockerfile


# ARQUITETURA

Aplicar:

- SOLID
- DRY
- KISS
- Separation of Concerns
- Service Layer Pattern
- Repository Pattern quando necessário
- Clean Architecture simplificada
- Modularização por domínio
- Baixo acoplamento
- Alta coesão


# PADRÕES BACKEND

O backend deve seguir:

- Apps desacopladas
- Services para regras de negócio
- Serializers separados
- Views enxutas
- URLs organizadas por módulo
- Configuração por ambiente
- Logs estruturados
- Preparação para testes automatizados

Estrutura interna esperada por app:

apps/estoque/
├── migrations/
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── services.py
├── selectors.py
├── repositories.py
├── views.py
├── urls.py
├── permissions.py
├── tests/
└── validators.py


# PADRÕES FRONTEND

Frontend deve seguir:

- Componentização reutilizável
- Separação entre layout e regra
- Hooks customizados
- Context API para autenticação
- Services para chamadas HTTP
- Páginas desacopladas
- Estrutura preparada para Zustand ou Redux futuramente


# SEGURANÇA

A configuração inicial deve considerar:

- Variáveis de ambiente
- SECRET_KEY fora do código
- DEBUG separado por ambiente
- CORS configurável
- JWT preparado
- Rate limit preparado
- Permissões RBAC preparadas
- Banco configurável
- Sem credenciais fixas
- Cookies seguros preparados
- Headers de segurança preparados

# API

Preparar padrão:

/api/v1/

Estrutura futura:

/api/v1/auth/
/api/v1/estoque/
/api/v1/compras/
/api/v1/financeiro/
/api/v1/fiscal/
/api/v1/os/
/api/v1/clientes/
/api/v1/fornecedores/
/api/v1/relatorios/

A API deve seguir:

- RESTful
- Responses padronizadas
- Versionamento
- Paginação
- Filtros
- Ordenação
- Tratamento global de erros

# BANCO DE DADOS

Utilizar PostgreSQL obrigatoriamente.

Preparar estrutura para:

- Multiempresa futura
- Auditoria
- Soft delete
- Índices
- Constraints
- Integridade relacional

Não utilizar SQLite.

# DOCKER

Criar ambiente completo com:

- backend
- frontend
- postgres
- redis
- celery
- celery-beat futuramente preparado

O docker-compose.yml deve permitir:

docker compose up --build

# CELERY

Preparar Celery para futuras tarefas assíncronas:

- Emissão de NFe
- Geração de relatórios
- Processamento de arquivos
- Envio de emails
- Rotinas automáticas
- Integrações externas

# README

Criar README profissional contendo:

- Nome do projeto
- Descrição
- Objetivos
- Tecnologias
- Arquitetura
- Estrutura de pastas
- Como rodar localmente
- Como rodar com Docker
- Variáveis de ambiente
- Convenções do projeto
- Status do projeto

# PADRÃO VISUAL

O frontend deve utilizar:

- Design moderno
- Interface corporativa
- TailwindCSS
- Layout clean
- Responsividade
- Componentes reutilizáveis

Paleta sugerida:

- Azul escuro
- Grafite
- Branco
- Roxo para destaque

# NÃO FAZER

- Não usar SQLite
- Não criar lógica de negócio nas views
- Não misturar responsabilidades
- Não criar código acoplado
- Não deixar credenciais no código
- Não usar arquitetura improvisada
- Não criar frontend desorganizado
- Não criar APIs sem padronização
- Não ignorar separação entre ambientes
- Não criar monólito bagunçado

# QUALIDADE

O projeto deve estar preparado para:

- Testes automatizados
- Escalabilidade
- CI/CD
- Logs
- Monitoramento
- Deploy futuro
- SaaS multiempresa futuramente


# FORMATO DA RESPOSTA

A resposta deve vir organizada em:

1. Visão geral da arquitetura
2. Estrutura completa de diretórios
3. Comandos de criação
4. Configuração backend
5. Configuração frontend
6. Configuração PostgreSQL
7. Configuração Docker
8. Configuração Redis
9. Configuração Celery
10. Arquivos iniciais
11. README inicial
12. Explicação técnica das decisões
13. Próximos passos recomendados


# IMPORTANTE

A resposta deve ser extremamente profissional.

Pensar como um ERP real de mercado.

Priorizar:

- Segurança
- Escalabilidade
- Organização
- Clareza
- Manutenibilidade

Evitar qualquer tipo de improvisação arquitetural.