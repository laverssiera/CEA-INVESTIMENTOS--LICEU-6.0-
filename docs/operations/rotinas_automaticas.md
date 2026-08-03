# Rotinas Automáticas

## Objetivo

Definir a cadência de jobs institucionais e rotinas operacionais recorrentes.

## Jobs técnicos

- `daily_yield_calculation`: dias úteis às 08:10;
- `check_product_limits`: dias úteis às 08:30;
- `sync_liceu_projects`: a cada 2 horas;
- `refresh_governance_snapshot`: dias úteis às 18:00;
- `publish_esg_committee_pack`: último dia útil do mês às 19:30.

## Rotinas por área

- crédito e comitê: pré-análise, parecer técnico e dossiê;
- tesouraria: posição de caixa e funding;
- compliance: KYC, AML, suitability e restrições;
- governança: fechamento executivo, auditoria e KPI.

## Evidências

Cada execução deve gerar log auditável com horário, usuário responsável, escopo e resultado.
