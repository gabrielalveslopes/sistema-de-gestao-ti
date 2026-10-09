# 🖥️ Sistema de Gestão de TI

Sistema em desenvolvimento para auxiliar no **controle de equipamentos de TI**, funcionários e movimentações de máquinas dentro de uma empresa.

O objetivo é centralizar informações sobre **quem está utilizando determinado equipamento**, registrar **entregas e retiradas** e, futuramente, integrar o sistema com a **API do Autentique** para automatizar a geração e o acompanhamento dos termos de responsabilidade.

> 🚧 **Status:** Em desenvolvimento

## 🎯 Objetivo

Automatizar e organizar processos internos do setor de TI relacionados à gestão de equipamentos.

O sistema pretende permitir:

- Cadastro de equipamentos;
- Cadastro de funcionários;
- Registro de entrega de equipamentos;
- Registro de retirada/devolução;
- Histórico de movimentações;
- Controle dos equipamentos vinculados aos funcionários;
- Geração automática de termos;
- Verificação da assinatura dos termos;
- Integração com o Autentique;
- Identificação de termos pendentes.

---

## 🛠️ Tecnologias

Atualmente o projeto utiliza:

- **Python**
- **PostgreSQL**
- **SQLAlchemy**
- **psycopg**
- **python-dotenv**
- **Git**
- **GitHub**

Tecnologias adicionais poderão ser incorporadas conforme o desenvolvimento do projeto.

---

## 🗄️ Banco de Dados

O banco de dados é desenvolvido utilizando **PostgreSQL**.

### Equipamento

Responsável por armazenar os equipamentos cadastrados.

Principais informações:

- ID
- Número de série
- Nome da máquina
- Fabricante

O número de série deve ser único para impedir o cadastro duplicado do mesmo equipamento.

### Funcionário

Responsável por armazenar os funcionários da empresa.

Principais informações:

- ID
- Nome
- E-mail institucional

### Movimentação

Responsável por registrar a relação entre um funcionário e um equipamento.

Principais informações:

- ID da movimentação
- Funcionário
- Equipamento
- Data e hora da entrega
- Data e hora da retirada

As tabelas são relacionadas através de **chaves estrangeiras (Foreign Keys)**.

---

## 📂 Estrutura do Projeto

```text
sistema-gestao-ti/
│
├── database/
│   └── ...
│
├── models/
│   └── ...
│
├── repositories/
│   ├── equipamento_repository.py
│   └── ...
│
├── services/
│   └── ...
│
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

A estrutura poderá sofrer alterações conforme novas funcionalidades forem implementadas.

---

## ⚙️ Configuração do Ambiente

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd sistema-gestao-ti
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Crie um banco no PostgreSQL para o projeto.

Depois, crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/nome_do_banco
```

> O arquivo `.env` não deve ser enviado para o GitHub.

---

## ▶️ Executando o Projeto

Com o ambiente virtual ativado:

```bash
python main.py
```

---

## ✅ Funcionalidades implementadas

Até o momento:

✅ **Configuração inicial do projeto**  
✅ **Conexão do Python com PostgreSQL**  
✅ **Modelagem inicial do banco de dados**  
✅ **Cadastro de equipamentos**  
✅ **Validação para impedir equipamentos duplicados**

⬜ Cadastro completo de funcionários  
⬜ Registro de movimentações  
⬜ Controle de entrega e retirada  
⬜ Histórico de equipamentos  
⬜ Integração com Autentique  
⬜ Geração automática de termos  
⬜ Verificação automática de assinatura  
⬜ Notificação de termos pendentes  
⬜ Interface do sistema  
⬜ Geração do executável

---

## 📄 Integração com Autentique

Uma das etapas futuras do projeto será integrar o sistema à API do **Autentique**.

O fluxo planejado é:

```text
Funcionário
     ↓
Equipamento
     ↓
Movimentação
     ↓
Geração do termo
     ↓
Envio para assinatura
     ↓
Autentique
     ↓
Verificação da assinatura
     ↓
Atualização do sistema
```

O objetivo é utilizar as informações cadastradas no banco para preencher automaticamente os termos, reduzindo o preenchimento manual realizado pelo setor de TI.

---

## 🔐 Segurança

Informações sensíveis não devem ser armazenadas diretamente no código.

Dados como:

- Senhas do PostgreSQL;
- Tokens;
- Chaves de API;
- Credenciais do Autentique;

devem ser armazenados em variáveis de ambiente através do arquivo `.env`.

O `.gitignore` deve conter:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

## 🚀 Próximas etapas

A próxima fase do desenvolvimento será concluir as operações relacionadas aos funcionários e começar o módulo de **movimentação de equipamentos**.

Depois disso, o projeto deverá avançar para:

**Movimentações → Termos → Autentique → Interface → Executável**

---

## 📌 Status do Projeto

O projeto está sendo desenvolvido de forma incremental, implementando e testando cada funcionalidade antes de avançar para a próxima etapa.

**Versão atual:** Desenvolvimento inicial  
**Foco atual:** Cadastro e persistência dos equipamentos no PostgreSQL
