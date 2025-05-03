# HUMANIQ

## 📋 Sobre o Projeto

O HUMANIQ é uma aplicação web desenvolvida para auxiliar jovens entre 15 e 25 anos a desenvolver habilidades sociais relevantes para o mercado de trabalho. A plataforma oferece recursos interativos, exercícios práticos e conteúdo educacional focado no desenvolvimento de soft skills essenciais para o sucesso profissional.

### 🎯 Propósito

Nosso objetivo é preencher a lacuna entre a educação tradicional e as habilidades interpessoais exigidas pelo mercado de trabalho atual, proporcionando aos jovens:

- Desenvolvimento de comunicação eficaz
- Aprimoramento do trabalho em equipe
- Fortalecimento da inteligência emocional
- Capacitação em resolução de problemas
- Estímulo ao pensamento crítico

## 🚀 Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

### Frontend
- **React.js**: Biblioteca JavaScript para construção de interfaces
- **Tailwind CSS**: Framework CSS para design responsivo e moderno

### Backend
- **Python**: Linguagem de programação principal
- **Flask**: Framework web leve e flexível

### Banco de Dados
- **SQLite**: Sistema de gerenciamento de banco de dados relacional

### Infraestrutura
- **Docker**: Containerização da aplicação
- **Docker Compose**: Orquestração dos serviços

## 📁 Estrutura do Projeto

```
humaniq/
├── frontend/             # Aplicação React
│   ├── public/           # Arquivos estáticos
│   ├── src/              # Código-fonte do frontend
│   ├── Dockerfile        # Configuração Docker para o frontend
│   └── .gitignore        # Arquivos ignorados pelo Git (frontend)
│
├── backend/              # API Flask
│   ├── app/              # Código-fonte do backend
│   ├── database/         # Arquivos do banco de dados SQLite
│   ├── Dockerfile        # Configuração Docker para o backend
│   └── .gitignore        # Arquivos ignorados pelo Git (backend)
│
├── docker-compose.yml    # Configuração dos serviços Docker
└── README.md             # Este arquivo
```

## ⚙️ Pré-requisitos

Para executar este projeto localmente, você precisará ter instalado:

- [Docker](https://www.docker.com/get-started) (versão 20.10.0 ou superior)
- [Docker Compose](https://docs.docker.com/compose/install/) (versão 2.0.0 ou superior)
- [Git](https://git-scm.com/downloads) (opcional, para clonar o repositório)

## 🔧 Como Executar

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local:

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/humaniq.git
cd humaniq
```

### 2. Inicie os contêineres Docker

```bash
docker-compose up -d
```

Este comando irá:
- Construir as imagens Docker para o frontend e backend (na primeira execução)
- Criar e iniciar os contêineres
- Configurar a rede entre os serviços
- Iniciar a aplicação em modo destacado (background)

### 3. Verifique se os contêineres estão em execução

```bash
docker-compose ps
```

Você deverá ver dois serviços em execução: `humaniq-frontend` e `humaniq-backend`.

## 🌐 Acessando a Aplicação

Após a inicialização bem-sucedida dos contêineres, você pode acessar:

- **Frontend**: http://localhost:3000
- **API Backend**: http://localhost:5000

## 🛑 Parando a Aplicação

Para parar a execução dos contêineres:

```bash
docker-compose down
```

Para parar e remover volumes (isso apagará dados persistentes):

```bash
docker-compose down -v
```

## 🔄 Desenvolvimento

### Logs da Aplicação

Para visualizar os logs em tempo real:

```bash
# Todos os serviços
docker-compose logs -f

# Apenas frontend
docker-compose logs -f frontend

# Apenas backend
docker-compose logs -f backend
```

### Reconstruindo os Contêineres

Se você fizer alterações nos Dockerfiles ou no código-fonte:

```bash
docker-compose up -d --build
```

## 🤝 Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## 📞 Contato

Para mais informações sobre o projeto, entre em contato com a equipe de desenvolvimento.

---

Desenvolvido com ❤️ pela equipe HUMANIQ
