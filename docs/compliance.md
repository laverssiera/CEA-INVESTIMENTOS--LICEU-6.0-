# Compliance

## KYC

Campos mínimos:
- CPF/CNPJ
- endereço
- renda
- patrimônio
- origem de recursos

## AML

- Verificar flags de lavagem de dinheiro.
- Marcar casos para revisão manual.
- Bloquear fluxo quando houver alerta crítico.

## Controles por Role

- compliance e admin podem executar checks de compliance.
- analista_credito avalia risco de crédito.
- tesouraria só libera recursos após aprovação.

## Segurança

- Rate limit no login (roadmap de produção)
- MFA para perfis internos
- Logs de auditoria em ações críticas
- Trilha de aprovação de crédito

## Estruturas

Tabela lógica:
- audit_logs

Campos recomendados:
- id
- timestamp
- action
- username
- role
- payload
