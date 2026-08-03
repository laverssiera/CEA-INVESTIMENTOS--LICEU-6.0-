# API — CEA INVESTIMENTOS

## Autenticação

- POST /auth/login
- POST /auth/mfa/verify
- POST /auth/refresh

## Roles

- investor_pf
- investor_pj
- cliente_financiamento
- admin
- analista_credito
- compliance
- tesouraria

## Onboarding Investidor

- POST /api/investor/signup
- POST /api/investor/kyc
- POST /api/investor/suitability
- GET /api/investor/onboarding

Regra:
- status pending: não pode investir
- status approved: libera investimento

## Investimentos

- GET /api/investments/products
- POST /api/investments/products
- POST /api/investments/orders
- GET /api/investments/positions
- GET /api/rules/allocation/{product_id}

## Crédito / Financiamento

- POST /api/financing/request
- GET /api/credit/requests
- POST /api/credit/requests/{request_id}/status
- GET /api/credit/score
- POST /api/credit/score

Pipeline:
- submitted
- under_review
- approved
- funded
- in_execution
- closed

## Dashboards

- GET /investor/dashboard
- GET /api/backoffice/dashboard

## LICEU 6.0

- GET /liceu/project/{id}
- GET /liceu/progress/{id}

## Tesouraria

- POST /api/treasury/transactions
- GET /api/treasury/transactions
- GET /api/treasury/balance

## Auditoria e Jobs

- GET /api/audit/logs
- POST /api/jobs/run/{job_name}

Jobs:
- daily_yield_calculation
- check_product_limits
- sync_liceu_projects
