# Validador de Senhas em Python (`password_validator`)

Motor determinístico, modular e resiliente de validação e avaliação de força de senhas, desenvolvido em conformidade com as melhores práticas de engenharia de software e segurança defensiva.

> **Origem do Software:** Este produto foi integralmente especificado, planejado, decomposto em tarefas, implementado, revisado e testado pela **Fábrica de Software Agêntica** (plataforma Google Antigravity), operando em arquitetura Hub-and-Spoke com seis subagentes especializados e governança baseada no GitHub Spec Kit (ciclo E0–E8).

---

## 1. Características do Produto

- **Zero Dependências Externas (SC-001):** Construído 100% com a Biblioteca Padrão do Python (*Python Standard Library*: `dataclasses`, `enum`, `re`, `typing`, `unittest`). Não requer `pip install` de pacotes de terceiros.
- **Garantia de Não Lançamento de Exceções (*No-Throw Guarantee*, FR-012):** Nunca lança exceções não tratadas (`TypeError`, `ValueError`, etc.) para o chamador, mesmo para entradas nulas (`None`), numéricas ou tipos arbitrários.
- **Alta Eficiência e Baixa Latência (SC-002):** Complexidade temporal linear $O(n)$, com tempo de resposta inferior a 1 milissegundo para senhas usuais.
- **Imutabilidade e Thread-Safety (SC-003):** Estruturas `@dataclass(frozen=True)` e catálogo em memória imutável (`frozenset`).
- **Suporte a Passphrases e Unicode (FR-011):** Preservação de espaços internos em frases secretas e suporte pleno a caracteres acentuados.

---

## 2. Requisitos e Instalação

- **Ambiente:** Python 3.10 ou superior.
- Não requer dependências externas. O módulo pode ser utilizado diretamente no Python Path:

```bash
# Execução direta de testes
python -m unittest discover -s tests -p "test_*.py"
```

---

## 3. Uso da API Pública

### 3.1 Validação Completa com Diagnóstico Estruturado

```python
from password_validator import validar_senha

resultado = validar_senha("C0mplex@Pass#2026")

print("Válida:", resultado.is_valid)       # True
print("Força:", resultado.forca)           # "FORTE"
print("Mensagens:", resultado.mensagens)   # []

# Conversão direta para dicionário serializável em JSON
dados_dict = resultado.to_dict()
```

### 3.2 Checagem Rápida (Helper Booleano)

```python
from password_validator import eh_senha_valida

if eh_senha_valida("Ab1!kQ9#"):
    print("Senha atende a todos os critérios de segurança!")
else:
    print("Senha reprovada!")
```

### 3.3 Tratamento Resiliente de Entradas Inválidas

```python
from password_validator import validar_senha

# Entrada nula (None)
res_null = validar_senha(None)
assert res_null.is_valid is False
assert res_null.forca == "FRACA"
assert "cadeia de texto (string)" in res_null.mensagens[0]

# Senha vazia ou composta unicamente por espaços
res_vazia = validar_senha("    ")
assert res_vazia.is_valid is False
assert "não pode ser vazia" in res_vazia.mensagens[0]
```

---

## 4. Tabela de Critérios Avaliados

| Código Canônico (`CodigoCriterio`) | Descrição do Critério | Requisito da Especificação |
|---|---|:---:|
| `TIPO_ENTRADA` | Validação de tipo de dado textual (`isinstance(senha, str)`). | FR-012 |
| `NAO_VAZIA` | Rejeição de senhas vazias ou compostas unicamente por espaços. | FR-011 |
| `TAMANHO_MINIMO` | Comprimento mínimo de 8 caracteres. | FR-001 |
| `MINUSCULAS` | Presença de pelo menos uma letra minúscula (suporte a Unicode). | FR-002 |
| `MAIUSCULAS` | Presença de pelo menos uma letra maiúscula (suporte a Unicode). | FR-003 |
| `NUMEROS` | Presença de pelo menos um dígito numérico decimal (`0-9`). | FR-004 |
| `ESPECIAIS` | Presença de pelo menos um caractere especial ou símbolo. | FR-005 |
| `SENHA_TRIVIAL` | Ausência de senhas conhecidas de dicionário ou termos vulneráveis. | FR-006 |
| `SEQUENCIA_SIMPLES` | Ausência de sequências alfanuméricas consecutivas de 3+ caracteres. | FR-007 |
| `REPETICAO_CARACTERES` | Ausência de 3 ou mais caracteres consecutivos idênticos. | FR-008 |

---

## 5. Classificação de Força (`NivelForca`)

- **`FRACA`:** A senha violou qualquer critério estrutural ou de segurança obrigatório.
- **`MEDIA`:** A senha atendeu a todos os critérios e possui comprimento entre 8 e 11 caracteres.
- **`FORTE`:** A senha atendeu a todos os critérios e possui comprimento igual ou superior a 12 caracteres.

---

## 6. Estrutura do Repositório

```text
validador-senhas/
├── README.md                          # Este documento
├── .gitignore                         # Arquivos ignorados pelo Git
├── src/
│   └── password_validator/            # Pacote Python do validador
│       ├── __init__.py                # Exportação da API pública
│       ├── models.py                  # Dataclasses imutáveis e Enums
│       ├── rules.py                   # Regras de validação (linear O(n))
│       ├── trivial_passwords.py       # Catálogo em frozenset de senhas triviais
│       ├── validator.py               # Orquestrador determinístico
│       └── README.md                  # Documentação do pacote interno
├── tests/
│   ├── __init__.py
│   ├── integration/                   # Testes de integração e aceite (QA)
│   │   ├── __init__.py
│   │   └── test_acceptance.py         # 23 cenários de aceite (FR-xxx / SC-xxx)
│   └── unit/                          # Testes unitários (Desenvolvedor)
│       ├── __init__.py
│       ├── test_models.py             # Testes de modelos e imutabilidade
│       ├── test_rules.py              # Testes exaustivos das regras
│       └── test_validator.py          # Testes do motor de validação
└── specs/
    └── 001-validador-senhas/          # Ciclo completo de governança Spec Kit
        ├── spec.md                    # Especificação de requisitos (E1)
        ├── checklists/requirements.md # Rastreabilidade e critérios
        ├── plan.md                    # Plano técnico e arquitetura (E2)
        ├── research.md                # Decisões de design e benchmarks
        ├── data-model.md              # Modelagem de dados
        ├── quickstart.md              # Guia rápido de implementação
        ├── contracts/validator_api.md # Contrato da API pública
        ├── tasks.md                   # 20 tarefas em 7 fases (E3)
        ├── review-report.md           # Parecer do Revisor de Código (E5)
        ├── qa-report.md               # Parecer e testes de QA (E6)
        └── state.json                 # Estado canônico do ciclo de vida
```

---

## 7. Execução dos Testes e Qualidade

O projeto conta com suíte completa de testes unitários e de integração/aceite:

```bash
# Executar todos os 50 testes
python -m unittest discover -s tests -p "test_*.py" -v

# Verificar integridade e compilação
python -m compileall -q src tests
```

**Resultado:**
- 50 testes passando (100% de sucesso).
- Tempo total de execução: ~0.09s.
- Zero dependências externas.

## Demonstração

O projeto disponibiliza o arquivo `demonstracao.py`, que apresenta exemplos práticos de validação de senhas com diferentes níveis de força.

Para executar a demonstração, na raiz do projeto, utilize:

```bash
set PYTHONPATH=src
python demonstracao.py