# Matriz RBAC Técnica

## Princípios

- segregação entre originação, aprovação e execução financeira;
- acesso por menor privilégio;
- MFA obrigatório para perfis internos;
- trilha de auditoria para eventos críticos.

## Escopos

| Perfil | Investimentos | Crédito | Tesouraria | Compliance | ESG |
|---|---|---|---|---|---|
| admin | approve | approve | supervise | read | read |
| risk_manager | read | approve | read | review | review |
| governance | read | review | read | approve | approve |
| diretoria | approve | approve | approve | read | approve |
| tesouraria | none | none | execute | read | none |
| compliance | read | veto | none | execute | read |

## Restrições

- tesouraria não delibera crédito;
- compliance pode bloquear dossiês pendentes;
- governance mantém leitura global e aprovação de rito;
- diretoria concentra deliberação final em temas críticos.
