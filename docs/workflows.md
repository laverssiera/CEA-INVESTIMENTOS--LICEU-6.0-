# Workflows

## Investidor PF

Cadastro
-> KYC
-> suitability
-> aprovação
-> escolher produto
-> investir
-> acompanhar obra
-> receber retorno

## Crédito

Cliente solicita
-> análise
-> aprovação
-> funding
-> execução LICEU
-> liquidação

## Operacional Backoffice

1. analista_credito revisa solicitações
2. compliance valida KYC/AML
3. tesouraria libera fundos
4. monitoramento acompanha progresso da obra
5. auditoria registra trilha

## Automações (cron)

- daily_yield_calculation: atualiza rendimento diário
- check_product_limits: fecha produto ao atingir cap
- sync_liceu_projects: atualiza progresso dos projetos LICEU
