class BankingReputationRuntime:
    def get_reputation(self, bank_id: str):
        print(f"⭐ [Reputation] Consultando reputação bancária federada de {bank_id}...")
        return {"bank": bank_id, "score": 9.9}

if __name__ == "__main__":
    r = BankingReputationRuntime()
    print(r.get_reputation("CEA-CENTRAL"))
