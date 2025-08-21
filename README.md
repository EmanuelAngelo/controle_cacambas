# [cite_start]Projeto: Software de Controle de Saídas de Caçambas [cite: 1]

Este projeto é um sistema de software em nuvem projetado para gerenciar e registrar a saída de caminhões caçamba, controlando os produtos transportados e os veículos utilizados. O sistema é construído com uma API REST robusta no backend e preparado para ser consumido por um frontend moderno.

## Funcionalidades Principais

* [cite_start]**Gerenciamento de Produtos**: Cadastro, edição, ativação e desativação de produtos transportados (ex: Barro, Areia, Piçarra)[cite: 4].
* [cite_start]**Gerenciamento de Veículos**: Cadastro completo de veículos, incluindo Número Interno, Placa, Capacidade, Tipo e Marca[cite: 9, 10, 11, 12, 13].
* [cite_start]**Registro de Movimentações**: Endpoint para registrar as saídas de veículos, associando um veículo, um produto, uma quantidade e o operador responsável[cite: 5].
* **API REST Segura**: Todos os endpoints são protegidos e requerem autenticação via token para garantir a segurança dos dados.
* **Painel de Administração Completo**: Uma interface administrativa pronta para uso, permitindo o gerenciamento de todos os dados do sistema.
* [cite_start]**Geração de Relatórios**: O sistema foi projetado para permitir a extração de relatórios com filtros por veículo, produto e período[cite: 23].

## Tecnologias Utilizadas

* **Backend**: Python 3
* **Framework**: Django
* **API**: Django REST Framework
* **Banco de Dados**: SQLite (padrão de desenvolvimento)

## Instalação e Configuração

Siga os passos abaixo para configurar o ambiente de desenvolvimento.

**1. Pré-requisitos:**
* Python 3.8 ou superior
* `pip` (gerenciador de pacotes do Python)

**2. Clone o Repositório:**
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd gestao_cacambas
```

**3. Crie e Ative o Ambiente Virtual:**
```bash
# Criar o ambiente
python -m venv venv

# Ativar no Windows
.\venv\Scripts\activate

# Ativar no macOS/Linux
source venv/bin/activate
```

**4. Instale as Dependências:**
(Primeiro, crie um arquivo `requirements.txt` se ainda não tiver um)
```bash
pip freeze > requirements.txt
```
(Depois, instale a partir dele)
```bash
pip install -r requirements.txt
```

**5. Aplique as Migrações do Banco de Dados:**
```bash
python manage.py migrate
```

**6. Crie um Superusuário:**
Este usuário será usado para acessar o painel administrativo e para obter o primeiro token da API.
```bash
python manage.py createsuperuser
```
Siga as instruções para criar um nome de usuário, email e senha.

**7. Rode o Servidor de Desenvolvimento:**
```bash
python manage.py runserver
```
O servidor estará disponível em `http://127.0.0.1:8000/`.

## Documentação da API

A API é o núcleo deste projeto. Todos os endpoints estão sob o prefixo `/api/`.

### Autenticação

A API utiliza autenticação baseada em Token. Para acessar os endpoints protegidos, você deve primeiro obter um token e depois enviá-lo em todas as requisições subsequentes no cabeçalho `Authorization`.

**1. Obter o Token (Login)**

* **Endpoint**: `/api/login/`
* **Método**: `POST`
* **Corpo da Requisição (`x-www-form-urlencoded`)**:
    * `username`: "seu_usuario"
    * `password`: "sua_senha"
* **Resposta de Sucesso (200 OK)**:
    ```json
    {
        "token": "seu_token_de_acesso_aqui"
    }
    ```

**2. Usando o Token**

Em todas as outras requisições, inclua o seguinte cabeçalho (Header):

* **Key**: `Authorization`
* **Value**: `Token seu_token_de_acesso_aqui`

---

### Endpoints Disponíveis

#### Produtos
* **Endpoint**: `/api/produtos/`
* **Métodos**: `GET`, `POST`
* **Descrição**: Lista todos os produtos ou cria um novo produto.
* **Corpo para POST**:
    ```json
    {
        "nome": "Brita",
        "esta_ativo": true
    }
    ```

#### Veículos
* **Endpoint**: `/api/veiculos/`
* **Métodos**: `GET`, `POST`
* **Descrição**: Lista todos os veículos ou cria um novo veículo.
* **Corpo para POST**:
    ```json
    {
        "numero_interno": "105",
        "placa": "DEF5678",
        "capacidade": "18.00",
        "tipo": "Caçamba Grande",
        "marca": "Volvo"
    }
    ```

#### Movimentações
* **Endpoint**: `/api/movimentacoes/`
* **Métodos**: `GET`, `POST`
* **Descrição**: Lista todas as movimentações ou registra uma nova saída.
* **Corpo para POST**:
    * `veiculo`: (ID do Veículo, ex: `1`)
    * `produto`: (ID do Produto, ex: `2`)
    * `quantidade`: (Valor decimal, ex: `"17.50"`)
    * **Exemplo**:
        ```json
        {
            "veiculo": 1,
            "produto": 2,
            "quantidade": "17.50"
        }
        ```
* **Resposta para GET (Listagem)**: A resposta da listagem é enriquecida para facilitar a exibição no frontend.
    ```json
    [
        {
            "id": 1,
            "veiculo": "Volvo - DEF5678",
            "produto": "Areia",
            "operador": "nome_do_admin",
            "quantidade": "17.50",
            "data_hora_saida": "2025-08-21T19:30:00Z",
            "status": "CONCLUIDO"
        }
    ]
    ```
**Observação**: Para todos os endpoints acima, é possível acessar um recurso específico adicionando o `ID` à URL (ex: `/api/produtos/1/`) e usar os métodos `GET` (detalhe), `PUT` (atualização) e `DELETE` (remoção).