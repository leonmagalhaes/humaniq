# Documentação da API HUMANIQ

Esta documentação descreve os endpoints disponíveis na API do projeto HUMANIQ.

## Base URL

```
http://localhost:5000/api
```

## Autenticação

A API utiliza autenticação JWT (JSON Web Token). Para acessar endpoints protegidos, é necessário incluir o token de acesso no cabeçalho da requisição:

```
Authorization: Bearer {seu_token_jwt}
```

### Endpoints de Autenticação

#### Registro de Usuário

- **URL**: `/auth/registro`
- **Método**: `POST`
- **Autenticação**: Não requerida
- **Corpo da Requisição**:
  ```json
  {
    "nome": "Nome Completo",
    "email": "email@exemplo.com",
    "senha": "senha123"
  }
  ```
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Usuário registrado com sucesso",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "usuario": {
      "id": 1,
      "nome": "Nome Completo",
      "email": "email@exemplo.com",
      "data_cadastro": "2023-05-01T12:00:00"
    }
  }
  ```

#### Login

- **URL**: `/auth/login`
- **Método**: `POST`
- **Autenticação**: Não requerida
- **Corpo da Requisição**:
  ```json
  {
    "email": "email@exemplo.com",
    "senha": "senha123"
  }
  ```
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Login realizado com sucesso",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "usuario": {
      "id": 1,
      "nome": "Nome Completo",
      "email": "email@exemplo.com",
      "data_cadastro": "2023-05-01T12:00:00"
    }
  }
  ```

#### Renovar Token

- **URL**: `/auth/refresh`
- **Método**: `POST`
- **Autenticação**: Requerida (refresh token)
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Token renovado com sucesso",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

#### Verificar Token

- **URL**: `/auth/verificar`
- **Método**: `GET`
- **Autenticação**: Requerida
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Token válido",
    "usuario": {
      "id": 1,
      "nome": "Nome Completo",
      "email": "email@exemplo.com",
      "data_cadastro": "2023-05-01T12:00:00"
    }
  }
  ```

## Usuários

### Obter Perfil

- **URL**: `/users/perfil`
- **Método**: `GET`
- **Autenticação**: Requerida
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Perfil obtido com sucesso",
    "perfil": {
      "id": 1,
      "nome": "Nome Completo",
      "email": "email@exemplo.com",
      "data_cadastro": "2023-05-01T12:00:00",
      "avaliacoes": [...],
      "resultados": [...]
    }
  }
  ```

### Atualizar Perfil

- **URL**: `/users/perfil`
- **Método**: `PUT`
- **Autenticação**: Requerida
- **Corpo da Requisição**:
  ```json
  {
    "nome": "Novo Nome",
    "email": "novo_email@exemplo.com",
    "senha_atual": "senha123",
    "nova_senha": "nova_senha123"
  }
  ```
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Perfil atualizado com sucesso",
    "usuario": {
      "id": 1,
      "nome": "Novo Nome",
      "email": "novo_email@exemplo.com",
      "data_cadastro": "2023-05-01T12:00:00"
    }
  }
  ```

### Obter Progresso

- **URL**: `/users/progresso`
- **Método**: `GET`
- **Autenticação**: Requerida
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Progresso obtido com sucesso",
    "progresso": {
      "total_desafios": 3,
      "desafios_concluidos": 1,
      "desafios_pendentes": 2,
      "pontuacao_total": 85,
      "resultados": [...]
    }
  }
  ```

## Avaliações

### Obter Perguntas do Teste

- **URL**: `/assessments/perguntas`
- **Método**: `GET`
- **Autenticação**: Requerida
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Perguntas obtidas com sucesso",
    "perguntas": [
      {
        "id": 1,
        "texto": "Eu me sinto confortável ao falar em público.",
        "categoria": "Comunicação",
        "ordem": 1
      },
      ...
    ]
  }
  ```

### Submeter Avaliação

- **URL**: `/assessments/submeter`
- **Método**: `POST`
- **Autenticação**: Requerida
- **Corpo da Requisição**:
  ```json
  {
    "respostas": {
      "1": 4,
      "2": 3,
      "3": 5,
      ...
    }
  }
  ```
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Avaliação submetida com sucesso",
    "avaliacao": {
      "id": 1,
      "usuario_id": 1,
      "data": "2023-05-01T12:00:00",
      "pontuacao": 75,
      "feedback": "Muito bom! Você possui boas habilidades interpessoais, mas ainda há espaço para crescimento.",
      "respostas": {
        "1": 4,
        "2": 3,
        ...
      }
    }
  }
  ```

### Obter Histórico de Avaliações

- **URL**: `/assessments/historico`
- **Método**: `GET`
- **Autenticação**: Requerida
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Histórico obtido com sucesso",
    "avaliacoes": [
      {
        "id": 1,
        "usuario_id": 1,
        "data": "2023-05-01T12:00:00",
        "pontuacao": 75,
        "feedback": "Muito bom! Você possui boas habilidades interpessoais, mas ainda há espaço para crescimento.",
        "respostas": {...}
      },
      ...
    ]
  }
  ```

## Desafios

### Listar Desafios

- **URL**: `/desafios/`
- **Método**: `GET`
- **Autenticação**: Requerida
- **Parâmetros de Consulta**:
  - `status`: Filtrar por status (ativo, inativo)
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Desafios obtidos com sucesso",
    "desafios": [
      {
        "id": 1,
        "titulo": "Comunicação Assertiva",
        "descricao": "Aprenda a se comunicar de forma clara, direta e respeitosa...",
        "video_url": "https://www.youtube.com/embed/exemplo1",
        "status": "ativo",
        "data_criacao": "2023-05-01T12:00:00",
        "progresso": {
          "status": "pendente",
          "data_inicio": "2023-05-02T10:00:00",
          "data_conclusao": null,
          "pontuacao": 0
        }
      },
      ...
    ]
  }
  ```

### Obter Desafio

- **URL**: `/desafios/{desafio_id}`
- **Método**: `GET`
- **Autenticação**: Requerida
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Desafio obtido com sucesso",
    "desafio": {
      "id": 1,
      "titulo": "Comunicação Assertiva",
      "descricao": "Aprenda a se comunicar de forma clara, direta e respeitosa...",
      "video_url": "https://www.youtube.com/embed/exemplo1",
      "status": "ativo",
      "data_criacao": "2023-05-01T12:00:00",
      "perguntas": [...],
      "desafio_pratico": "Identifique uma situação recente em que você não se comunicou de forma assertiva...",
      "progresso": {...}
    }
  }
  ```

### Iniciar Desafio

- **URL**: `/desafios/{desafio_id}/iniciar`
- **Método**: `POST`
- **Autenticação**: Requerida
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Desafio iniciado com sucesso",
    "resultado": {
      "id": 1,
      "usuario_id": 1,
      "desafio_id": 1,
      "status": "pendente",
      "data_inicio": "2023-05-02T10:00:00",
      "data_conclusao": null,
      "pontuacao": 0,
      "respostas_quiz": null,
      "resposta_pratica": null
    }
  }
  ```

### Submeter Desafio

- **URL**: `/desafios/{desafio_id}/submeter`
- **Método**: `POST`
- **Autenticação**: Requerida
- **Corpo da Requisição**:
  ```json
  {
    "respostas_quiz": {
      "1": "Expressar-se sem agredir ou submeter-se",
      "2": "Manipulação",
      "3": "A assertiva respeita os direitos dos outros, a agressiva não"
    },
    "resposta_pratica": "Em uma reunião recente, eu não consegui expressar minha opinião de forma clara..."
  }
  ```
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Desafio submetido com sucesso",
    "resultado": {
      "id": 1,
      "usuario_id": 1,
      "desafio_id": 1,
      "status": "concluído",
      "data_inicio": "2023-05-02T10:00:00",
      "data_conclusao": "2023-05-02T11:30:00",
      "pontuacao": 30,
      "respostas_quiz": {...},
      "resposta_pratica": "Em uma reunião recente, eu não consegui expressar minha opinião de forma clara..."
    }
  }
  ```

### Obter Desafio em Destaque

- **URL**: `/desafios/destaque`
- **Método**: `GET`
- **Autenticação**: Requerida
- **Resposta de Sucesso**:
  ```json
  {
    "message": "Desafio em destaque obtido com sucesso",
    "desafio": {
      "id": 1,
      "titulo": "Comunicação Assertiva",
      "descricao": "Aprenda a se comunicar de forma clara, direta e respeitosa...",
      "video_url": "https://www.youtube.com/embed/exemplo1",
      "status": "ativo",
      "data_criacao": "2023-05-01T12:00:00",
      "perguntas": [...],
      "desafio_pratico": "Identifique uma situação recente em que você não se comunicou de forma assertiva...",
      "progresso": {...}
    }
  }
  ```

## Códigos de Status

- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `400 Bad Request`: Requisição inválida ou dados incompletos
- `401 Unauthorized`: Autenticação necessária ou falha na autenticação
- `404 Not Found`: Recurso não encontrado
- `409 Conflict`: Conflito (ex: email já cadastrado)
- `500 Internal Server Error`: Erro interno do servidor
