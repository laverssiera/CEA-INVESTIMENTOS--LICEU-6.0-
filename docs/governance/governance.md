# Governanca CEA

## Estrutura

Diretoria
↓
Compliance
↓
Risco
↓
Operacoes
↓
Tecnologia

## Camadas Operacionais

### Camada 1 — Fachada (Public)
- site institucional
- trabalhe conosco
- ESG
- onboarding do investidor
- solicitacao de financiamento

Regra: sem autenticacao obrigatoria.

### Camada 2 — Cliente / Investidor
- dashboard do investidor
- dashboard do cliente financiamento
- carteira
- projetos
- home broker

Roles:
- investor_pf
- investor_pj
- cliente_financiamento

### Camada 3 — Colaborador Operacional
- analise de credito
- KYC
- compliance operacional
- acompanhamento de projetos
- atendimento ao cliente

Roles:
- analista_credito
- compliance
- tesouraria
- colaborador

### Camada 4 — Backoffice Institucional
- tesouraria institucional
- funding
- alocacao
- controle de risco
- auditoria
- ESG governance

Roles:
- admin
- risk_manager
- governance
- diretoria

### Camada 5 — Governanca e Auditoria
- logs
- trilha de auditoria
- controle de acesso
- relatorios regulatorios
- aprovacao dupla

## Comites
- Comite de credito
- Comite de investimento
- Comite ESG

## Regras de Segregacao
- quem aprova nao executa
- quem executa nao liquida
- auditor possui acesso somente leitura
- aprovacao dupla obrigatoria para operacoes criticas

## Restricoes Tecnicas
- aprovacao dupla obrigatoria para investimentos acima de R$ 5.000.000
- aprovacao dupla obrigatoria para financiamentos acima de R$ 10.000.000
- aprovacao dupla obrigatoria para movimentacoes de tesouraria
- MFA obrigatorio para perfis internos
- token de acesso com 15 minutos
- refresh token com 24 horas
- RBAC obrigatorio em todas as rotas protegidas
- logs auditaveis obrigatorios
