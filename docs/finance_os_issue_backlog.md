# Finance OS - Backlog Executivo (CEA Investimentos)

Data: 2026-07-31
Escopo: Monolito CEA Investimentos com integracoes CEFEIDA, John, JuridicoTech, HubBackoffice e Telão LICEU.

## Visao Geral

Este documento organiza as 26 issues da missao Finance OS em estado operacional para execucao por sprint.

Legenda de status:
- implemented: existe implementacao funcional no backend
- partial: existe base implementada, requer hardening/producao
- pending: nao implementado no monolito atual

## Bloco 1 - Fundacao Financeira (Core)

1. Ledger Financeiro Unificado (Double Entry) - implemented
- Tabelas: finance_ledger_entries, finance_wallets
- Servico: transferencia com debito/credito e trilha de auditoria
- Gap: padronizar visoes contabil-fiscal por entidade/ativo em relatorios consolidados

2. Wallet Engine (Carteiras por Monolito) - implemented
- Carteiras seed: CEA_MASTER, ARCHIMEDES_OPER, GAMEMKT_BUDGET, HUBBACKOFFICE_COST
- API: GET /wallets, POST /wallet/transfer

3. Cash Flow Engine (Fluxo de Caixa Global) - partial
- API: GET /finance/cashflow (daily/monthly)
- Inclui forecast e alerta de liquidez
- Gap: previsao estatistica avancada e sensibilidade por cenario

## Bloco 2 - Engine de Investimento

4. ROI Engine (ROI, TIR, Payback, NPV) - implemented
- API: GET /finance/roi/{entity_id}

5. Deal Scoring Financeiro - implemented
- Score composto por retorno, risco, liquidez e horizonte

6. Capital Allocation Engine - implemented
- API: POST /finance/invest
- Output padrao action/amount/target com score

## Bloco 3 - Integracao com John

7. Financial Decisions via John - implemented
- API: POST /finance/john/decision

8. Learning Loop Financeiro - implemented
- API: POST /finance/learning/feedback
- Atualiza vies de alocacao com base em retorno realizado

## Bloco 4 - Integracao com CEFEIDA

9. Data Feed Financeiro - implemented
- API: POST /finance/cefeida/feed

10. Financial Intelligence Output - implemented
- API: POST /finance/intelligence/output
- Retorna viabilidade, recomendacao e alerta

## Bloco 5 - Integracao com JuridicoTech

11. Compliance Financeiro - implemented
- API: POST /finance/compliance/check

12. Anti-Fraude Financeiro - implemented
- API: POST /finance/antifraud/check

## Bloco 6 - HubBackoffice

13. Integracao Contabil - implemented
- APIs: POST /finance/accounting/register, GET /finance/accounting/report, POST /finance/accounting/sync-hub

14. Orcamento e Controle - implemented
- APIs: POST /finance/budget/set, POST /finance/budget/execute, GET /finance/budget/status

## Bloco 7 - Dashboard Executivo

15. Financial Command Center - implemented
- API: GET /finance/command-center

16. Integracao com Telao LICEU - implemented
- API: POST /finance/liceu/sync

## Bloco 8 - Eventos (NATS/Event Bus)

17. Publicar Eventos Financeiros - partial
- Publicados internamente: finance.investment_created, finance.roi_calculated, finance.cashflow_alert, finance.loss_detected
- Gap: publicar em NATS real com topicos e retries

18. Consumir Eventos - implemented
- API: POST /finance/events/consume
- Eventos suportados: archimedes.deal_created, gamemkt.campaign_started, hub.cost_registered

## Bloco 9 - Automacao

19. Auto Invest Engine - implemented
- API: POST /finance/auto-invest/trigger
- Fluxo: compliance -> antifraud -> john -> execucao

20. Budget Rebalancer - partial
- API: GET /finance/budget/rebalance
- Gap: execucao automatica de realocacao (hoje apenas proposta)

## Bloco 10 - RBAC + Auditoria

21. RBAC Financeiro (CFO/Gestor/Analista) - implemented
- Protecao por header role em endpoints financeiros

22. Auditoria Completa - implemented
- Tabela: finance_audit
- API: GET /finance/audit

## Bloco 11 - APIs

23. API Financeira - implemented
- GET /finance/roi/{entity_id}
- POST /finance/invest
- GET /finance/cashflow

24. API de Carteiras - implemented
- GET /wallets
- POST /wallet/transfer

## Bloco 12 - SLA + Kanban

25. SLA Financeiro por Task - implemented
- APIs: POST /finance/sla/create, POST /finance/sla/update, GET /finance/sla/list

26. Integracao com Kanban Global - implemented
- APIs: POST /finance/kanban/create, POST /finance/kanban/move, GET /finance/kanban/board, GET /finance/kanban/list

## Correcao aplicada nesta entrega

- Fix no Auto Invest para caminho de execucao real do investimento (chamada de transferencia corrigida).
- Nova consulta de trilha de auditoria financeira:
  - GET /finance/audit?action=&user_id=&limit=
- Integracao NATS real no barramento de eventos:
  - Publicacao com `Nats-Msg-Id` para idempotencia no broker.
  - Persistencia local de tentativas/sucesso em `automation_event_dispatches`.
  - Consumer opcional com queue-group para eventos externos (archimedes/gamemkt/hub).
  - Retry assincrono com backoff exponencial para falhas de publish.
  - Endpoint de observabilidade: `GET /finance/events/dispatches`.
  - Metricas por janela: `GET /finance/events/dispatches/metrics?window_hours=24`.
  - Top falhas por erro: `GET /finance/events/dispatches/top-failures?window_hours=24&limit=10&group_by=error_type`.
  - Top falhas por evento+erro: `GET /finance/events/dispatches/top-failures?window_hours=24&limit=10&group_by=event_error`.
  - Top falhas por evento: `GET /finance/events/dispatches/top-failures?window_hours=24&limit=10&group_by=event_name`.
  - Cada item do ranking inclui `participation_pct` para uso direto em dashboard executivo.
  - Reprocessamento manual de falha: `POST /finance/events/dispatches/reprocess`.
  - Toggle por ambiente:
    - `FINANCE_NATS_ENABLED=true`
    - `FINANCE_NATS_CONSUMER_ENABLED=true`
    - `NATS_URL=nats://host:4222`
    - `FINANCE_NATS_RETRY_MAX_ATTEMPTS=3`
    - `FINANCE_NATS_RETRY_BACKOFF_SECONDS=0.5`

## Proxima onda recomendada (producao)

1. NATS real para eventos financeiros (publisher/consumer com idempotencia).
2. Previsao de caixa com modelos de serie temporal + cenarios de estresse.
3. Realocacao automatica de budget (nao apenas sugestao).
4. RBAC com claims JWT e politicas por recurso/acao.
5. Painel executivo no frontend consumindo command-center e audit trail.
