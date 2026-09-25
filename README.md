# ZeladorX APIs — Jardinagem e Limpeza Predial

> API corporativa da família **ZeladorX**, responsável por disponibilizar as regras de negócio, cadastros, permissões e operações de zeladoria para integrações e aplicações clientes.

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.16-A30000)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)

## Visão geral

O **ZeladorX APIs** é o terceiro projeto da família de ferramentas corporativas ZeladorX. Ele transforma o domínio compartilhado de gestão de zeladoria em uma API REST autenticada, atendendo principalmente às operações de **jardinagem** e **limpeza predial**.

O serviço preserva as mesmas entidades, migrações e regras de negócio dos sistemas irmãos. Assim, aplicações web, mobile ou integrações podem consultar e operar o mesmo ambiente corporativo sem duplicar lógica.

```text
                         Banco de dados corporativo compartilhado
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
      ┌───────▼────────┐        ┌────────▼────────┐       ┌─────────▼─────────┐
      │   ZeladorX     │        │  ChatChannels   │       │  ZeladorX APIs   │
      │ Gestão e       │        │ Comunicação e   │       │ Integrações e    │
      │ Kanban         │        │ colaboração     │       │ clientes REST    │
      └────────────────┘        └─────────────────┘       └───────────────────┘
```

## Responsabilidades da API

- autenticar usuários e invalidar tokens no logout;
- recuperar senha por token enviado por e-mail;
- respeitar a hierarquia de empresas, unidades, localidades e áreas;
- separar operações de jardinagem e limpeza predial;
- gerenciar catálogos, serviços configurados e serviços agendados;
- aplicar o fluxo de seis estágios do Kanban;
- registrar execução, evidências e checklists;
- controlar acesso por empresa, setor e permissão granular;
- disponibilizar terrenos, vegetação, dias da semana e configurações auxiliares;
- apoiar integrações com respostas JSON e paginação.

## Fluxo operacional de seis estágios

O mesmo serviço possui um **status persistido**, controlado pelo andamento da equipe, e uma **classificação temporal**, calculada pela API para os itens ainda ativos.

```text
Configuração recorrente ou criação manual
                    │
                    ▼
              Serviço agendado
                    │
       ┌────────────┼────────────┐
       │ classificação por data │
       ▼            ▼            ▼
  Agendados      Próximos     Atrasados
   > 7 dias       0–7 dias      data passada
       └────────────┬────────────┘
                    │ ação autorizada
                    ▼
              Em andamento
                 │       │
                 ▼       ▼
            Concluído  Cancelado
```

### Etapas automáticas por data

| Etapa | Regra |
|---|---|
| **Agendados** | início previsto para mais de 7 dias |
| **Próximos** | início previsto entre hoje e os próximos 7 dias |
| **Atrasados** | início previsto anterior ao momento atual |

### Etapas manuais por andamento

| Etapa | Uso |
|---|---|
| **Em andamento** | execução iniciada por um colaborador autorizado |
| **Concluído** | atividade finalizada e registrada |
| **Cancelado** | atividade interrompida ou retirada da programação |

As mudanças de status passam pelas permissões do usuário. O código associa as ações de agendar, acompanhar, concluir e cancelar a permissões distintas.

## Agendamento recorrente

Serviços configurados podem definir:

- área atendida;
- itens do catálogo que serão executados;
- dias da semana;
- duração média planejada;
- até sete horários por dia;
- situação **Mobilizado** ou **Desmobilizado**.

A rotina diária, programada para **00:15**, percorre apenas configurações, áreas, localidades, unidades e itens de catálogo mobilizados. Para o dia da semana correspondente, ela cria serviços do tipo `Automático`, calcula o horário previsto de conclusão e vincula os responsáveis definidos pelo sistema.

## Domínio corporativo

A autorização e a segmentação dos dados seguem a cadeia organizacional:

```text
Empresa primária
└── Empresa secundária / setor
    └── Unidade
        └── Localidade
            └── Área
                ├── Serviços configurados
                ├── Serviços agendados
                ├── Fatos de execução
                └── Checklists
```

Os registros públicos da API utilizam `id_random` como identificador funcional nas URLs, em vez de expor diretamente a chave numérica do banco.

## Principais módulos

| Módulo | Responsabilidade |
|---|---|
| `authenticate` | login, logout e recuperação de senha |
| `empresaprimaria` | empresas corporativas às quais o usuário tem acesso |
| `empresasecundario` | empresas operacionais e seus setores |
| `unidade` | unidades vinculadas às empresas |
| `localidade` | locais de atendimento de cada vertical |
| `areas` | áreas operacionais e último atendimento |
| `catalogo_de_servicos` | serviços disponíveis para jardinagem ou limpeza |
| `servicos` | configurações recorrentes, agenda, status e fatos de execução |
| `checklists` | itens de verificação associados aos serviços |
| `permissionscontrol` | permissões especiais e por vertical |
| `settings` | preferências operacionais dos gestores |
| `terrenos` | cadastro territorial utilizado pela jardinagem |
| `vegetacao` | catálogo de vegetação |
| `semana` | dias da semana usados nas recorrências |
| `zeladorx` | macroserviços habilitados para o usuário |
| `schedules` | geração automática das atividades recorrentes |
| `notifications` | notificações e recuperação de senha por e-mail |

## Autenticação e acesso

Por padrão, a API usa **Token Authentication** do Django REST Framework e exige usuário autenticado.

### Login

```http
POST /api/login
Content-Type: application/json

{
  "username": "usuario",
  "password": "senha"
}
```

Resposta de sucesso:

```json
{
  "token": "TOKEN_DE_AUTENTICACAO",
  "id_random": "IDENTIFICADOR_PUBLICO",
  "user_id": 1,
  "username": "usuario",
  "email": "usuario@empresa.com",
  "is_superuser": false
}
```

### Requisições autenticadas

```http
Authorization: Token TOKEN_DE_AUTENTICACAO
Content-Type: application/json
```

### Sessão e senha

| Método | Endpoint | Finalidade |
|---|---|---|
| `POST` | `/api/login` | autenticar e obter token |
| `POST` | `/api/logout/` | excluir o token atual |
| `POST` | `/api/reset-password/` | solicitar recuperação por e-mail |
| `POST` | `/api/confirm-reset-password/<url_token>/` | validar código e definir nova senha |

> A autenticação identifica o usuário, mas cada operação também pode exigir uma permissão funcional e vínculo com as empresas consultadas.

## Catálogo de APIs

O projeto registra **189 rotas**. A tabela abaixo agrupa os recursos para facilitar a navegação; os nomes completos estão nos arquivos `*/api/urls*.py`.

| Prefixo | Escopo | Operações principais |
|---|---|---|
| `/api/unidades/` | unidades | listar, detalhar, criar, atualizar, mobilizar/desmobilizar, validar e excluir |
| `/api/localidades/` | localidades | operações separadas para jardinagem e limpeza predial |
| `/api/areas/` | áreas | CRUD, vínculo por localidade e tempo desde o último atendimento |
| `/api/empresas_secundarias/` | empresas operacionais | CRUD e listas para formulários por vertical |
| `/api/catalogo_de_servicos/` | catálogo | CRUD, alteração de status e listas para formulários |
| `/api/settings/` | preferências | consultar e atualizar configurações por gestor e vertical |
| `/api/terrenos/` | terrenos | CRUD, alteração de status e listas auxiliares |
| `/api/vegetacao/` | vegetação | CRUD, alteração de status e listas auxiliares |
| `/api/gerentes/` | usuários operacionais | CRUD, status e associação por vertical |
| `/api/servicos/configurados/` | recorrências | configurar dias/horários, consultar, editar, mobilizar e excluir |
| `/api/servicos/agendados/` | agenda operacional | criar, listar, detalhar, editar, alterar status e excluir |
| `/api/servicos/fato/` | execução | registrar e consultar fatos/evidências por serviço |
| `/api/permissions/` | autorização | permissões de jardinagem, limpeza predial e especiais |
| `/api/checklist/` | checklists | CRUD e consulta por serviço |
| `/api/semana/` | recorrência | listar dias da semana |
| `/api/zeladorx/` | contexto | macroserviços e empresas primárias acessíveis |

### Padrão das operações de cadastro

A maior parte dos recursos segue um vocabulário consistente:

```text
List<Resource>/
<Resource>Detail/<id_random>/
Create<Resource>/
<Resource>Update/<id_random>/
<Resource>AlterStatus/<id_random>/
IfDelete<Resource>/<id_random>/
Delete<Resource>/<id_random>/
List<Resource>FromForms/
```

`IfDelete...` verifica se o registro pode ser removido antes do `DELETE`, protegendo relacionamentos já utilizados. As listagens usam paginação global de **15 itens** e, conforme o recurso, pesquisa e ordenação do DRF.

### Exemplos importantes

```http
GET  /api/servicos/agendados/ListServicoJardinagemAgendadoAnotados/
PUT  /api/servicos/agendados/AlterStatusServicoJardinagem/<id_random>/
GET  /api/servicos/fato/ListFatoServicoJardinagemByservico/<id_random>/
GET  /api/areas/TempoDesdeUltimoAtendimentoJardinagem/
GET  /api/zeladorx/MyMacroServices/
```

Alteração de andamento:

```http
PUT /api/servicos/agendados/AlterStatusServicoJardinagem/ABC123/
Authorization: Token TOKEN_DE_AUTENTICACAO
Content-Type: application/json

{
  "status": "Em andamento"
}
```

Os valores aceitos pelo serviço são `Agendado`, `Em andamento`, `Concluido` e `Cancelado`. As categorias `Próximo` e `Atrasado` são calculadas nas consultas e não gravadas como andamento.

## Respostas, filtros e erros

As respostas de cadastro normalmente seguem esta estrutura:

```json
{
  "success": true,
  "message": "Operação realizada com sucesso.",
  "data": {}
}
```

Listagens paginadas seguem o padrão do Django REST Framework:

```json
{
  "count": 42,
  "next": "https://api.exemplo.com/recurso/?page=2",
  "previous": null,
  "results": []
}
```

Códigos HTTP esperados:

| Código | Significado |
|---:|---|
| `200` | consulta ou atualização concluída |
| `201` | registro criado |
| `400` | dados inválidos ou transição não permitida |
| `401` | token ausente ou inválido |
| `403` | usuário autenticado sem permissão funcional |
| `404` | registro inexistente ou fora das empresas acessíveis |

## Permissões funcionais

Além do acesso por token, a API filtra dados pelas empresas primárias e secundárias associadas ao usuário e valida permissões por vertical. Entre as permissões aplicadas ao ciclo de serviços estão:

| Código | Ação |
|---:|---|
| `320` | agendar novos serviços |
| `321` | editar serviços agendados |
| `322` | visualizar serviços agendados |
| `323` | excluir serviços agendados |
| `324` | acompanhar serviços agendados |
| `326` | concluir serviços em andamento |
| `328` | cancelar serviços agendados |
| `361` | acompanhar apenas serviços destinados ao próprio usuário |
| `370–375` | criar, editar, visualizar, excluir, desmobilizar e reabilitar configurações |
| `390–391` | visualizar e editar o detalhamento da execução |

## Tecnologias

- Python 3.11+
- Django 5.1
- Django REST Framework 3.16
- autenticação por token do DRF
- PostgreSQL
- Gunicorn
- WhiteNoise
- Pillow para imagens
- ReportLab, OpenPyXL e XlsxWriter para documentos e relatórios
- bibliotecas geoespaciais e de otimização presentes no ambiente do projeto

## Instalação local

### Pré-requisitos

- Python 3.11 ou superior
- PostgreSQL
- compiladores e bibliotecas de sistema exigidos pelas dependências geoespaciais, quando aplicável

### 1. Clone e entre no projeto

```bash
git clone https://github.com/Markosalves12/zeladorxV2APIs-Jardinagem.git
cd zeladorxV2APIs-Jardinagem
```

### 2. Crie o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure o ambiente

Crie um `.env` local, nunca versionado:

```dotenv
SECRET_KEY=troque-por-uma-chave-segura
EMAIL_HOST=smtp.exemplo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=usuario
EMAIL_HOST_PASSWORD=senha
```

A conexão PostgreSQL está atualmente declarada em `setup/settings.py`. Para ambientes reais, mova nome, usuário, senha, host e porta para variáveis de ambiente antes do deploy.

### 5. Prepare e execute

```bash
python manage.py migrate
python manage.py runserver
```

A API estará disponível, por padrão, em `http://127.0.0.1:8000/api/`.

## Migrações e banco compartilhado

Este repositório pertence à mesma família do **ZeladorX** e do **ChatChannels** e compartilha modelos, tabelas e migrações de aplicações comuns. Por isso, uma migração incompatível ou duplicada pode interromper todos os sistemas.

Regras de manutenção:

1. nunca crie migrações concorrentes para o mesmo app em repositórios diferentes;
2. uma migração de app compartilhado deve conservar o mesmo nome, dependências e conteúdo em todos os membros da família;
3. publique primeiro código compatível com o esquema atual;
4. execute `migrate` uma única vez por ambiente, em um fluxo controlado;
5. valide ZeladorX, ChatChannels e esta API antes de remover colunas ou alterar contratos;
6. não use `makemigrations` automaticamente no processo de publicação.

## Deploy

O `Procfile` inicia a aplicação com Gunicorn:

```text
web: gunicorn setup.wsgi
```

Antes de publicar:

- defina `DEBUG=False`;
- restrinja `ALLOWED_HOSTS`;
- injete todas as credenciais por variáveis de ambiente;
- execute `collectstatic` quando necessário;
- configure armazenamento persistente para arquivos enviados;
- confirme o processo responsável pela rotina diária das 00:15;
- valide migrações contra todos os sistemas da família.

## Segurança

Este repositório já contém material sensível versionado, incluindo `.env`, credenciais de banco no arquivo de configuração e uma chave de serviço do Google Cloud. Esses dados devem ser considerados comprometidos.

Ações obrigatórias:

1. revogar e gerar novas credenciais no provedor correspondente;
2. trocar senhas e chaves utilizadas pelos ambientes;
3. remover os arquivos sensíveis do histórico Git, não apenas do commit atual;
4. adicionar `.env`, chaves JSON e outros segredos ao `.gitignore`;
5. usar variáveis de ambiente no desenvolvimento e na publicação;
6. manter `DEBUG=False` e hosts explícitos em produção.

## Testes

Os módulos possuem arquivos `tests.py`, mas ainda não há uma suíte automatizada relevante. Antes de mudanças nas regras compartilhadas, priorize testes para:

- isolamento de dados por empresa e setor;
- permissões de cada transição de status;
- fronteiras temporais de 0, 7 e mais de 7 dias;
- geração diária sem duplicidade;
- exclusão de registros com dependências;
- paridade entre jardinagem e limpeza predial;
- compatibilidade das migrações entre os três repositórios.

## Projetos relacionados

- [ZeladorX](https://github.com/Markosalves12/zeladorxV2) — gestão operacional, Kanban, calendários, mapas e relatórios;
- [ChatChannels](https://github.com/Markosalves12/CHATCHANNELS) — comunicação corporativa em tempo real;
- **ZeladorX APIs** — camada REST para integrações e aplicações clientes.

---

Este projeto é parte de uma arquitetura corporativa compartilhada. Mudanças em modelos, migrações, permissões e regras de negócio devem ser avaliadas no conjunto da família ZeladorX.
