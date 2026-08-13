from prometheus_client import Counter

financial_decisions = Counter(
    "financial_decisions_total",
    "Financial runtime decisions"
)
