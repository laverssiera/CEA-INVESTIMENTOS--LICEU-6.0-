class ExecutiveRiskGrid:
    def calculate(self, financial, legal, operational, climate):
        score = (
            financial * 0.4 +
            legal * 0.25 +
            operational * 0.2 +
            climate * 0.15
        )


        return {
            "global_risk": score,
            "classification": self.classify(score)
        }


    def classify(self, score):
        if score < 25:
            return "LOW"
        if score < 50:
            return "MODERATE"
        if score < 75:
            return "HIGH"
        return "CRITICAL"
