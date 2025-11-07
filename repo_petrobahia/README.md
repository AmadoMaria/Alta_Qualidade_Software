# PetroBahia S.A. - Sistema de Processamento de Pedidos

**PetroBahia S.A.** é uma empresa fictícia do setor de óleo e gás. Este projeto implementa um sistema para calcular preços de combustíveis, registrar clientes e processar pedidos.

## 🎯 Objetivos do Projeto

Este é um projeto acadêmico de **Qualidade de Software** focado em:
- Refatorar código legado para seguir princípios **SOLID**
- Implementar **Hexagonal Architecture** (Ports & Adapters)
- Aplicar **Clean Code** e **PEP8**
- Melhorar legibilidade, manutenibilidade e testabilidade

---

## 🏗️ Arquitetura

O projeto segue rigorosamente a **Arquitetura Hexagonal**, separando claramente as responsabilidades:

```
src/
├── domain/                          # Camada de Domínio (Núcleo)
│   ├── entities/                    # Entidades de negócio
│   │   ├── cliente.py
│   │   ├── pedido.py
│   │   └── produto.py
│   ├── value_objects/               # Objetos de valor
│   │   ├── email.py
│   │   └── cnpj.py
│   └── services/                    # Serviços de domínio
│       ├── pricing_service.py       # Cálculo de preços
│       ├── discount_service.py      # Aplicação de descontos
│       └── rounding_service.py      # Arredondamento de valores
│
├── application/                     # Camada de Aplicação
│   └── use_cases/                   # Casos de uso (orquestração)
│       ├── register_cliente_use_case.py
│       └── process_pedido_use_case.py
│
├── ports/                           # Portas (Interfaces)
│   ├── cliente_repository_port.py
│   ├── pedido_repository_port.py
│   └── notification_port.py
│
├── adapters/                        # Adaptadores (Infraestrutura)
│   ├── repositories/                # Adaptadores de persistência
│   │   ├── json_cliente_repository.py
│   │   └── json_pedido_repository.py
│   ├── notifications/               # Adaptadores de notificação
│   │   └── console_notification.py
│   └── cli/                         # Adaptador de entrada (CLI)
│       └── main_cli.py
│
├── main.py                          # Ponto de entrada
└── legacy/                          # Código legado (preservado)
    ├── clientes.py
    ├── pedido_service.py
    └── preco_calculadora.py
```

---

## 📋 Princípios SOLID Aplicados

### **S - Single Responsibility Principle**
Cada classe tem uma única responsabilidade:
- `PricingService`: calcula apenas preços base com descontos por volume
- `DiscountService`: aplica apenas descontos de cupons
- `RoundingService`: arredonda apenas valores finais
- `Email`: valida apenas emails
- `RegisterClienteUseCase`: orquestra apenas registro de clientes

### **O - Open/Closed Principle**
Sistema aberto para extensão, fechado para modificação:
- Novos tipos de produtos podem ser adicionados ao enum `TipoProduto`
- Novos cupons podem ser adicionados no `DiscountService`
- Novos adaptadores (SQL, API) podem ser criados sem modificar o core

### **L - Liskov Substitution Principle**
Subtipos podem substituir tipos base:
- Qualquer implementação de `ClienteRepositoryPort` funciona de forma intercambiável
- `JsonClienteRepository` pode ser substituído por `SqlClienteRepository` sem quebrar o código

### **I - Interface Segregation Principle**
Interfaces específicas e coesas:
- `ClienteRepositoryPort`: apenas operações de cliente
- `PedidoRepositoryPort`: apenas operações de pedido
- `NotificationPort`: apenas operações de notificação
- Sem interfaces "gordas" ou monolíticas

### **D - Dependency Inversion Principle**
Dependências apontam para abstrações:
- Use cases dependem de `Ports` (interfaces), não de implementações concretas
- `ProcessPedidoUseCase` depende de `PedidoRepositoryPort`, não de `JsonPedidoRepository`
- Inversão de controle aplicada em toda a arquitetura

---

## 🎨 Padrões de Design Aplicados

### **Repository Pattern**
- Abstração da camada de persistência através de `Ports`
- Implementações em `Adapters` (JSON, futuramente SQL, etc.)

### **Value Object Pattern**
- `Email`: validação e encapsulamento de emails
- `CNPJ`: validação e formatação de CNPJ

### **Use Case Pattern**
- Casos de uso isolados e testáveis
- Orquestração de serviços de domínio

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.13+
- Poetry

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

### Estrutura do código
- ✅ Type hints em todas as funções
- ✅ Dataclasses para entidades imutáveis
- ✅ Separação clara de responsabilidades
- ✅ Zero código duplicado
- ✅ Nenhuma lógica de negócio nos adapters

---

## 📊 Problemas do Código Legado

### ❌ Violações Identificadas

1. **Mistura de responsabilidades**
   - Lógica de negócio misturada com I/O
   - Validação misturada com persistência
   - Print statements em funções de negócio

2. **Deeply nested if-else**
   - `preco_calculadora.py`: 4 níveis de aninhamento
   - Difícil de ler e manter

3. **Violação de SOLID**
   - `processar_pedido()`: múltiplas responsabilidades
   - Lógica de cupons hardcoded (violação OCP)
   - Dependências concretas (violação DIP)

4. **Má qualidade**
   - Print statements espalhados
   - Sem type hints
   - Validação de email incorreta (aceita `ana@@petrobahia`)
   - Loop ineficiente para multiplicação (O(n) para operação O(1))

5. **Falta de separação**
   - Nenhuma camada de abstração
   - Dependências concretas diretamente acopladas
   - Impossível de testar unitariamente

---

## ✅ Melhorias Implementadas

### **Código Limpo**
- Nomes descritivos e significativos
- Funções pequenas e focadas (métodos privados para legibilidade)
- Sem duplicação (DRY)
- Type hints completos
- Dataclasses imutáveis com `frozen=True`

### **Arquitetura**
- Hexagonal Architecture implementada
- Camadas bem definidas e isoladas
- Domain puro (sem dependências externas)
- Fácil de testar e estender

### **SOLID**
- Cada classe tem uma responsabilidade
- Extensível sem modificação
- Interfaces segregadas e coesas
- Dependências invertidas

### **Manutenibilidade**
- Fácil adicionar novos produtos (adicionar no enum + service)
- Fácil adicionar novos cupons (adicionar no `DiscountService`)
- Fácil trocar implementações (JSON → SQL)
- Fácil testar (mocks nas portas)

---

## 🔮 Extensões Futuras

- Adicionar testes unitários e de integração
- Implementar adapter REST API
- Adicionar adapter SQL para persistência
- Implementar logging estruturado
- Adicionar validação de CNPJ com dígitos verificadores
- Adicionar relatórios e dashboards

---

## 📚 Referências

- **Clean Code** - Robert C. Martin
- **Clean Architecture** - Robert C. Martin
- **Hexagonal Architecture** - Alistair Cockburn
- **PEP8** - Python Enhancement Proposal
- **Domain-Driven Design** - Eric Evans

---

## 👥 Autores

Projeto acadêmico desenvolvido para o curso de **Alta Qualidade de Software**.
