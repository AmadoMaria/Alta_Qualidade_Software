# PetroBahia S.A. - Sistema de Processamento de Pedidos

**PetroBahia S.A.** é uma empresa fictícia do setor de óleo e gás. Este projeto implementa um sistema para calcular preços de combustíveis, registrar clientes e processar pedidos com arquitetura limpa e testes focados nos serviços de domínio.

## 🎯 Objetivos do Projeto

Este é um projeto acadêmico de **Qualidade de Software** focado em:

- Refatorar código legado para seguir princípios **SOLID**
- Implementar **Hexagonal Architecture** (Ports & Adapters)
- Aplicar **Clean Code** e **PEP8**
- Melhorar legibilidade, manutenibilidade e testabilidade
- **Testes focados em serviços de domínio** (lógica de negócio)

---

## 🏗️ Arquitetura

O projeto segue rigorosamente a **Arquitetura Hexagonal**, separando claramente as responsabilidades:

```
repo_petrobahia/
├── src/
│   ├── domain/                              # Camada de Domínio (Núcleo)
│   │   ├── entities/                        # Entidades de negócio
│   │   │   ├── cliente.py                   # Cliente com validação Email/CNPJ
│   │   │   ├── pedido.py                    # Pedido com validação de quantidade
│   │   │   ├── produto.py                   # Produto e TipoProduto enum
│   │   │   └── cupom.py                     # Cupons enum (MEGA10, NOVO5, LUB2)
│   │   ├── value_objects/                   # Objetos de valor
│   │   │   ├── email.py                     # Email com regex validation
│   │   │   └── cnpj.py                      # CNPJ com formatação
│   │   └── services/                        # Serviços de domínio
│   │       ├── pricing_service.py           # Cálculo de preços + descontos volume
│   │       ├── discount_service.py          # Aplicação de cupons
│   │       ├── rounding_service.py          # Arredondamento por tipo produto
│   │       ├── client_service.py            # Lógica registro de clientes
│   │       └── pedido_service.py            # Orquestração processamento pedidos
│   │
│   ├── ports/                               # Portas (Interfaces)
│   │   ├── cliente_repository_port.py       # Interface para persistência clientes
│   │   ├── pedido_repository_port.py        # Interface para persistência pedidos
│   │   └── notification_port.py             # Interface para notificações
│   │
│   ├── adapters/                            # Adaptadores (Infraestrutura)
│   │   ├── repositories/                    # Adaptadores de persistência
│   │   │   ├── json_cliente_repository.py   # Implementação JSON para clientes
│   │   │   └── json_pedido_repository.py    # Implementação JSON para pedidos
│   │   ├── notifications/                   # Adaptadores de notificação
│   │   │   └── console_notification.py      # Implementação console
│   │   ├── use_cases/                       # Casos de uso (orquestração)
│   │   │   ├── register_cliente_use_case.py # Workflow registro cliente
│   │   │   └── process_pedido_use_case.py   # Workflow processamento pedido
│   │   └── cli/                             # Adaptador de entrada (CLI)
│   │       └── main_cli.py                  # Interface linha de comando
│   │
│   └── main.py                              # Ponto de entrada
│
├── tests/                                   # Testes automatizados (5 arquivos)
│   ├── conftest.py                          # Fixtures compartilhadas
│   └── unit/
│       └── domain/
│           └── services/                    # Testes serviços (5 arquivos)
│               ├── test_pricing_service.py
│               ├── test_discount_service.py
│               ├── test_rounding_service.py
│               ├── test_client_service.py
│               └── test_pedido_service.py
│
├── data/                                    # Armazenamento JSON
│   ├── clientes.json
│   └── pedidos.json
│
├── pyproject.toml                           # Configuração Poetry + pytest
├── .pre-commit-config.yaml                  # Hooks pre-commit (flake8, isort)
└── README.md
```

---

## 📋 Princípios SOLID Aplicados

### **S - Single Responsibility Principle**

Cada classe tem uma única responsabilidade:

- `PricingService`: calcula apenas preços base com descontos por volume
- `DiscountService`: aplica apenas descontos de cupons
- `RoundingService`: arredonda apenas valores finais (diesel=0, outros=2 decimais)
- `Email`: valida apenas emails com regex
- `CNPJ`: valida e formata apenas CNPJs
- `ClientService`: orquestra apenas registro de clientes
- `PedidoService`: orquestra apenas processamento de pedidos

### **O - Open/Closed Principle**

Sistema aberto para extensão, fechado para modificação:

- Novos tipos de produtos: adicionar ao enum `TipoProduto` e regras nos serviços
- Novos cupons: adicionar ao enum `Cupom` sem alterar `DiscountService`
- Novos adaptadores: criar SQL/API sem modificar domain

### **L - Liskov Substitution Principle**

Subtipos podem substituir tipos base:

- Qualquer implementação de `ClienteRepositoryPort` funciona intercambiavelmente
- `JsonClienteRepository` pode ser substituído por `SqlClienteRepository` sem quebrar código
- Mesma garantia para `PedidoRepositoryPort` e `NotificationPort`

### **I - Interface Segregation Principle**

Interfaces específicas e coesas:

- `ClienteRepositoryPort`: apenas operações de cliente (save, find_by_id, find_by_email, exists_by_email)
- `PedidoRepositoryPort`: apenas operações de pedido (save, find_by_id, find_by_cliente_id)
- `NotificationPort`: apenas operações de notificação (send_welcome_email, send_order_confirmation)

### **D - Dependency Inversion Principle**

Dependências apontam para abstrações:

- Use cases dependem de `Ports`, não de implementações concretas
- `ProcessPedidoUseCase` depende de `PedidoRepositoryPort`, não de `JsonPedidoRepository`
- Services recebem ports via construtor (Dependency Injection)

---

## 🎨 Padrões de Design Aplicados

### **Repository Pattern**
- Abstração da camada de persistência através de `Ports`
- Implementações em `Adapters` (JSON atual, SQL futuro)

### **Value Object Pattern**
- `Email`: validação e encapsulamento de emails
- `CNPJ`: validação e formatação de CNPJ (remove caracteres especiais)

### **Use Case Pattern**
- Casos de uso isolados e testáveis
- Orquestração de serviços de domínio com tratamento de erros

### **Strategy Pattern (implícito)**
- `PricingService`: diferentes estratégias de desconto por tipo de produto
- Diesel: desconto progressivo por volume (>500: 5%, >1000: 10%)
- Gasolina: desconto fixo R$100 se quantidade >200
- Etanol: desconto 3% se quantidade >80

---

## 🧪 Testes Automatizados

### Foco em Serviços de Domínio

O projeto possui testes focados nos **serviços de domínio** (camada de lógica de negócio):

#### Services Testados (5 arquivos)
- ✅ `test_pricing_service.py` - 20+ testes de cálculo de preços e descontos por volume
- ✅ `test_discount_service.py` - 25+ testes de aplicação de cupons de desconto
- ✅ `test_rounding_service.py` - 25+ testes de arredondamento por tipo de produto
- ✅ `test_client_service.py` - 15+ testes de registro de clientes
- ✅ `test_pedido_service.py` - 20+ testes de orquestração completa de pedidos

### O que é testado

**PricingService**:
- Cálculo de preço base × quantidade
- Descontos progressivos por volume (diesel: >500: 5%, >1000: 10%)
- Descontos por quantidade (gasolina: >200: R$100, etanol: >80: 3%)
- Validação de quantidade positiva
- Tratamento de produtos inválidos

**DiscountService**:
- Aplicação de cupons percentuais (MEGA10: 10%, NOVO5: 5%)
- Aplicação de cupons fixos (LUB2: R$2)
- Restrições por produto (LUB2 apenas para lubrificante)
- Case-insensitive para códigos de cupom
- Cupons inválidos retornam preço original

**RoundingService**:
- Diesel: arredonda para 0 casas decimais (inteiro)
- Outros produtos: arredondam para 2 casas decimais
- Tratamento de valores positivos e negativos

**ClientService**:
- Registro de clientes com validação Email/CNPJ
- Integração com repositório (mocked)
- Envio de notificação de boas-vindas
- Tratamento de falhas de persistência

**PedidoService**:
- Pipeline completo: pricing → discount → rounding
- Validação de cliente existente
- Validação de quantidade positiva
- Combinação de descontos (volume + cupom)
- Persistência de pedidos

### Executar Testes

```bash
# Todos os testes com cobertura e relatórios HTML
python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html --html=reports/test_report.html --self-contained-html -v

# Apenas testes (sem cobertura)
python -m pytest tests/ -v

# Testes específicos
python -m pytest tests/unit/domain/services/test_pricing_service.py -v

# Executar testes em modo silencioso
python -m pytest tests/ -q

# Parar no primeiro erro
python -m pytest tests/ -x
```

### Relatórios Gerados

Após executar os testes, os seguintes relatórios são gerados:

1. **Relatório HTML de Testes** (`reports/test_report.html`)
   - Visão detalhada de todos os testes executados
   - Status de cada teste (PASSED/FAILED)
   - Tempo de execução
   - Informações do ambiente
   - Abrir: `reports/test_report.html` no navegador

2. **Relatório HTML de Cobertura** (`htmlcov/index.html`)
   - Percentual de cobertura por arquivo
   - Linhas cobertas e não cobertas
   - Navegação interativa pelo código
   - Abrir: `htmlcov/index.html` no navegador

### Tecnologias de Teste

- **pytest**: Framework de testes
- **pytest-cov**: Relatórios de cobertura de código
- **pytest-html**: Relatórios HTML de execução de testes
- **pytest-mock / unittest.mock**: Mocking para isolamento de testes
- **conftest.py**: Fixtures compartilhadas (clientes, pedidos, mocks)

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.12+ (projeto requer >=3.12)
- Poetry (gerenciador de dependências)

### Instalação

```bash
cd repo_petrobahia
poetry install
```

### Execução

```bash
poetry run python src/main.py
```

### Saída Esperada

```
============================================================
PetroBahia S.A. - Order Processing System
============================================================

Registering customers...
------------------------------------------------------------
[EMAIL] Welcome message sent to contato@translog.com.br
✓ TransLog registered successfully
[EMAIL] Welcome message sent to vendas@movemais.com
✓ MoveMais registered successfully
[EMAIL] Welcome message sent to suporte@ecofrota.com.br
✓ EcoFrota registered successfully
[EMAIL] Welcome message sent to comercial@petropark.com
✓ PetroPark registered successfully

Processing orders...
------------------------------------------------------------
✓ Order ORD001: Diesel x1200 (Coupon: MEGA10) = R$ 4310
✓ Order ORD002: Gasolina x300 = R$ 1457.00
✓ Order ORD003: Etanol x50 (Coupon: NOVO5) = R$ 170.52
✓ Order ORD004: Lubrificante x12 (Coupon: LUB2) = R$ 298.00

------------------------------------------------------------
TOTAL: R$ 6235.52
============================================================
```

---

## 🔍 Validação de Qualidade

### Verificar conformidade PEP8

```bash
poetry run flake8 src/
```

### Executar pre-commit hooks

```bash
poetry run pre-commit run --all-files
```

### Estrutura do código

- ✅ Type hints em todas as funções
- ✅ Pydantic BaseModel para entidades imutáveis (`frozen=True`)
- ✅ Dataclasses para value objects imutáveis
- ✅ Separação clara de responsabilidades
- ✅ Zero código duplicado
- ✅ Nenhuma lógica de negócio nos adapters
- ✅ **95%+ cobertura de testes**

---

## 💼 Regras de Negócio

### Produtos e Preços Base

| Produto       | Preço Base |
|---------------|------------|
| Diesel        | R$ 3,99    |
| Gasolina      | R$ 5,19    |
| Etanol        | R$ 3,59    |
| Lubrificante  | R$ 25,00   |

### Descontos por Volume

**Diesel:**
- Quantidade > 1000: 10% de desconto
- Quantidade > 500: 5% de desconto

**Gasolina:**
- Quantidade > 200: R$ 100,00 de desconto fixo

**Etanol:**
- Quantidade > 80: 3% de desconto

### Cupons de Desconto

| Cupom   | Tipo        | Valor     | Restrição         |
|---------|-------------|-----------|-------------------|
| MEGA10  | Percentual  | 10%       | Todos produtos    |
| NOVO5   | Percentual  | 5%        | Todos produtos    |
| LUB2    | Fixo        | R$ 2,00   | Apenas Lubrificante |

### Arredondamento

- **Diesel**: arredondado para 0 casas decimais (número inteiro)
- **Outros produtos**: arredondados para 2 casas decimais

### Pipeline de Cálculo

```
Preço Base × Quantidade
    ↓
Desconto por Volume (se aplicável)
    ↓
Desconto de Cupom (se aplicável)
    ↓
Arredondamento por Tipo
    ↓
Preço Final
```

---

## 📊 Problemas do Código Legado (Resolvidos)

### ❌ Violações Identificadas

1. **Mistura de responsabilidades**
   - Lógica de negócio misturada com I/O
   - Validação misturada com persistência
   - Print statements em funções de negócio

2. **Deeply nested if-else**
   - 4 níveis de aninhamento
   - Difícil de ler e manter

3. **Violação de SOLID**
   - Múltiplas responsabilidades em uma função
   - Lógica de cupons hardcoded (violação OCP)
   - Dependências concretas (violação DIP)

4. **Má qualidade**
   - Sem type hints
   - Validação de email incorreta
   - Sem testes automatizados

---

## ✅ Melhorias Implementadas

### **Código Limpo**
- Nomes descritivos e significativos
- Funções pequenas e focadas
- Type hints completos
- Pydantic para validação automática
- Imutabilidade garantida (`frozen=True`)

### **Arquitetura**
- Hexagonal Architecture completa
- Camadas bem definidas e isoladas
- Domain puro (sem dependências externas)
- Fácil de testar e estender

### **SOLID**
- Cada classe tem uma responsabilidade
- Extensível sem modificação
- Interfaces segregadas e coesas
- Dependências invertidas

### **Testabilidade**
- **Testes focados em serviços de domínio** (lógica de negócio crítica)
- Mocks para isolamento de dependências externas
- Fixtures reutilizáveis em conftest.py
- Testes de unidade para regras de negócio
- Cobertura de casos de sucesso e edge cases
- Relatórios HTML com pytest-html

---

## 🔮 Extensões Futuras

- [ ] Implementar adapter REST API (FastAPI)
- [ ] Adicionar adapter SQL para persistência (PostgreSQL)
- [ ] Implementar logging estruturado (structlog)
- [ ] Adicionar validação de CNPJ com dígitos verificadores
- [ ] Criar dashboard de relatórios
- [ ] Implementar custom exceptions com error codes
- [ ] Adicionar campo `final_price` em `Pedido`
- [ ] CI/CD com GitHub Actions
- [ ] Containerização com Docker

---

## 📚 Referências

- **Clean Code** - Robert C. Martin
- **Clean Architecture** - Robert C. Martin
- **Hexagonal Architecture** - Alistair Cockburn
- **PEP8** - Python Enhancement Proposal
- **Domain-Driven Design** - Eric Evans
- **Test-Driven Development** - Kent Beck

---

## 👥 Autores

Projeto acadêmico desenvolvido para o curso de **Alta Qualidade de Software**.

---

## 📝 Licença

Projeto educacional - uso livre para fins acadêmicos.
