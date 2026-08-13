# Regras de Negócio

## RBAC

- Investidor não acessa dados de crédito.
- Cliente não acessa carteira de investimentos.
- Staff acessa módulos conforme role.

## Crédito

- Apenas analista_credito pode mover solicitação para approved.
- Apenas tesouraria pode mover solicitação para funded.
- Fluxo obrigatório: submitted -> under_review -> approved -> funded -> in_execution -> closed.

## Investimentos

- Produto tem limite mínimo de aporte.
- Produto tem limite por investidor.
- Produto tem limite total de captação.
- Produto pode estar open ou closed.
- Regra de alocação PF: se risco do projeto for alto, limite PF = 30% da captação.

## Ativos de Longo Prazo

- Funding para pesquisa, patentes, laboratorios e infraestrutura deve ser tratado como capital paciente.
- Ativos de propriedade intelectual devem ter trilha de governanca, validadacao juridica e priorizacao economica.
- Receita de PI pode vir de licenciamento, royalties, cessao e participacao societaria.
- Spin-offs exigem aprovacao de tese, valuation, compliance e plano de separacao operacional.

## Onboarding Investidor

- Cadastro inicial cria status pending.
- KYC obrigatório.
- Suitability obrigatório.
- Somente status approved libera ordens de investimento.

## Tesouraria

- Registrar entradas de investidores e saídas de financiamento.
- Saldo = entradas - saídas.

## Auditoria

- Ações críticas devem gerar trilha em audit_logs.
- Eventos mínimos: login, MFA, mudança de status de crédito, criação de ordem, movimentação de tesouraria, execução de jobs.
