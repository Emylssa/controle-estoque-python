# Documentação Teórica — Sistema de Controle de Estoque

## 1. Contextualização
O controle de estoque é essencial para garantir organização, redução de perdas, atendimento à demanda e apoio às decisões da empresa. A aplicação desenvolvida permite cadastrar produtos, controlar entrada e saída de itens, consultar o estoque atual e visualizar alertas de reposição.

## 2. Modelagem da Aplicação
### Entidades
- **Usuários**: responsáveis por acessar o sistema. Possuem perfil Administrador ou Comum.
- **Produtos**: itens armazenados no estoque, com quantidade atual e quantidade mínima.
- **Movimentações**: histórico de entradas e saídas realizadas no sistema.

### Relacionamentos
- Um usuário pode registrar várias movimentações.
- Um produto pode possuir várias movimentações.
- Cada movimentação pertence a um produto e a um usuário.

### Modelo relacional
- **users**(id, name, username, password_hash, profile, created_at)
- **products**(id, name, category, quantity, min_quantity, unit, created_at)
- **movements**(id, product_id, movement_type, quantity, user_id, note, created_at)

## 3. Fluxo lógico da aplicação
1. Usuário acessa a tela de login.
2. O sistema valida usuário e senha no banco de dados.
3. Após autenticação, o sistema abre a tela principal.
4. O usuário pode:
   - cadastrar produto;
   - atualizar produto;
   - registrar entrada;
   - registrar saída;
   - consultar alertas de estoque baixo.
5. Caso o usuário seja administrador, ele também pode cadastrar novos usuários.

## 4. Fluxograma textual
```text
Início
  ↓
Tela de login
  ↓
Validar credenciais
  ├── Inválido → Exibir erro → Volta ao login
  └── Válido → Abrir sistema
                  ↓
          Escolher operação
                  ↓
   ├── Cadastrar produto → Salvar no banco
   ├── Atualizar produto → Atualizar no banco
   ├── Entrada de estoque → Somar quantidade + registrar movimento
   ├── Saída de estoque → Validar saldo → Subtrair + registrar movimento
   ├── Visualizar alertas → Destacar itens abaixo do mínimo
   └── Cadastrar usuário (somente admin) → Salvar no banco
                  ↓
                 Fim
```

## 5. Benefícios de digitalizar o controle de estoque
O principal benefício é a confiabilidade das informações em tempo real. Com isso, a empresa reduz erros manuais, evita excesso ou falta de produtos, melhora o planejamento de compras e diminui o uso de papéis e registros físicos.

## 6. Prós e contras
### Prós
- Rapidez na consulta e atualização de dados;
- Menor risco de erro humano em controles manuais;
- Histórico das movimentações;
- Mais segurança com login e perfil de usuário;
- Redução de papel e ganho ambiental.

### Contras
- Custo de implantação e treinamento;
- Resistência de alguns funcionários à mudança;
- Dependência do correto cadastro das informações;
- Necessidade de manutenção da aplicação.

## 7. Barreiras de implementação
- Investimento inicial;
- Mudança cultural na empresa;
- Treinamento da equipe;
- Padronização dos cadastros;
- Garantia da qualidade dos dados lançados no sistema.

## 8. Considerações finais
A aplicação foi desenvolvida para atender aos requisitos essenciais de um sistema de estoque acadêmico: autenticação, perfis de acesso, cadastro de produtos, movimentações, alertas visuais e persistência em banco de dados. A decisão por Tkinter e SQLite foi tomada por serem tecnologias simples, leves e adequadas para um projeto educacional.
