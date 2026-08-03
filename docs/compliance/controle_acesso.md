# Compliance e Controle de Acesso

## Matriz RBAC Institucional

| Funcao | Investimentos | Credito | Tesouraria | Compliance | ESG |
|---|---|---|---|---|---|
| analista_credito | leitura | editar | nao | leitura | leitura |
| compliance | leitura | leitura | leitura | editar | editar |
| tesouraria | leitura | leitura | editar | leitura | leitura |
| admin | total | total | total | total | total |
| colaborador | leitura | leitura | nao | nao | leitura |

## Regras de Seguranca
- MFA obrigatorio
- token de 15 minutos
- refresh token de 24 horas
- RBAC obrigatorio
- logs auditaveis obrigatorios

## Trilha de Auditoria
Campos obrigatorios:
- user_id
- action
- module
- timestamp
- ip
- old_value
- new_value

Exemplo:
- user_id: analista_credito
- action: approve_credit
- module: credito
- timestamp: 2026-03-01 14:32
- ip: 10.20.30.40
- old_value: under_review
- new_value: approved

## Restricoes Tecnicas
- aprovacao dupla obrigatoria para investimentos acima de R$ 5.000.000
- aprovacao dupla obrigatoria para financiamento acima de R$ 10.000.000
- aprovacao dupla obrigatoria para movimentacao de tesouraria
- quem aprova nao executa
- quem executa nao liquida
- auditor apenas leitura
