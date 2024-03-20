# README

Bem-vindo ao projeto da Imobiliária Koru!

Este repositório contém um projeto principalmente focado no desenvolvimento backend utilizando Flask, um framework web em Python. O objetivo principal é criar um site para uma imobiliária, onde as funcionalidades serão implementadas usando Flask, além de aplicar o Bootstrap para o estilo CSS.

## Funcionalidades

O projeto segue a estrutura CRUD, que significa:

- **C**reate (Criar): Capacidade de criar novos registros, como listagens de imóveis.
- **R**ead (Ler): Capacidade de ler, visualizar ou buscar informações existentes, como detalhes de um imóvel.
- **U**pdate (Atualizar): Capacidade de atualizar informações existentes, como alterar o preço de um imóvel.
- **D**elete (Excluir): Capacidade de excluir registros existentes, como remover uma listagem de imóvel que já foi vendida.

## Estrutura do Projeto Flask

O projeto segue uma estrutura padrão para projetos Flask, com os seguintes diretórios e arquivos principais:

```
meu_projeto_flask/
│
├── app/
│   ├── static/          # Arquivos estáticos, como CSS, JS, imagens
│   ├── templates/       # Modelos HTML usando Jinja2
│   ├── models.py        # Definição dos modelos de dados
│   ├── views.py         # Lógica de visualização das rotas
│   └── __init__.py      # Inicialização do aplicativo Flask
│
├── migrations/          # Migrações do banco de dados (se estiver usando Flask-Migrate)
│
├── tests/               # Testes automatizados
│
├── config.py            # Configurações do aplicativo
├── requirements.txt     # Lista de dependências do Python
└── run.py               # Arquivo de inicialização do aplicativo
```

## Como Executar

1. Certifique-se de ter o Python instalado em seu sistema. Você pode baixá-lo em [python.org](https://www.python.org/).

2. Clone este repositório:

   ```
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   ```

3. Navegue até o diretório do projeto:

   ```
   cd nome-do-repositorio
   ```

4. Instale as dependências do Python:

   ```
   pip install -r requirements.txt
   ```

5. Execute o aplicativo:

   ```
   python run.py
   ```

6. Abra seu navegador e acesse `http://localhost:5000` para visualizar o site da imobiliária.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
