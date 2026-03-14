# Sistema de Controle de Estoque em Python

Aplicação desktop desenvolvida em **Python + Tkinter + SQLite** para controle de entrada e saída de produtos e materiais.

## Funcionalidades
- Login com perfis **Administrador** e **Comum**
- Cadastro de produtos
- Atualização de dados do produto
- Movimentação de estoque (entrada e saída)
- Validação de campos numéricos
- Lista de alertas para estoque abaixo do mínimo
- Cadastro de usuários **somente por administrador**
- Senha com **hash SHA-256**
- Banco de dados SQLite local

## Estrutura do projeto
```bash
estoque_project/
├── app/
│   ├── models/
│   ├── services/
│   ├── ui/
│   └── utils/
├── docs/
├── database.sql
├── estoque.db   # gerado automaticamente ao executar
├── main.py
└── README.md
```

## Como executar
1. Tenha o Python 3 instalado.
2. Extraia o arquivo ZIP.
3. Abra a pasta do projeto no VS Code ou terminal.
4. Execute:
```bash
python main.py
```
5. Use o login padrão:
- **Usuário:** admin
- **Senha:** admin123

## Requisitos atendidos
- Interface amigável com Tkinter
- Conexão com banco de dados SQLite
- Sessão de usuário após login
- Perfis de acesso
- Validação de campos obrigatórios
- Destaque visual para baixo estoque

## Sugestão para o vídeo pitch
Mostre rapidamente:
1. Tela de login
2. Cadastro de produto
3. Entrada e saída de estoque
4. Alerta de estoque mínimo
5. Cadastro de novo usuário como administrador
