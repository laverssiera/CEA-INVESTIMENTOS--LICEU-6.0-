import math

def calculate_irr(cash_flows, iterations=1000):
    rate = 0.1
    for _ in range(iterations):
        npv = sum(cf / (1 + rate)**i for i, cf in enumerate(cash_flows))
        if abs(npv) < 0.0001:
            return rate
        derivative = sum(-i * cf / (1 + rate)**(i + 1) for i, cf in enumerate(cash_flows))
        if derivative == 0:
            break
        rate = rate - npv / derivative
    return rate

def analyze_geo_satellite_mission():
    print("### CEA - Análise de Missão de Recuperação Orbital")
    print("-" * 40)
    print("Problema:")
    print("  Satélite GEO")
    print("  Combustível baixo")
    print("  Desvio orbital")
    print("  Perda parcial de potência")
    print("-" * 40)

    # Parâmetros simulados
    investment = 50.0  # M$
    annual_revenue = 15.0 # M$
    life_extension = 5 # Anos
    discount_rate = 0.10

    cash_flows = [-investment] + [annual_revenue] * life_extension

    # Cálculos
    npv = sum(cf / (1 + discount_rate)**i for i, cf in enumerate(cash_flows))
    irr = calculate_irr(cash_flows)
    payback = investment / annual_revenue

    print(f"Calculando:")
    print(f"  NPV: ${npv:.2f} M")
    print(f"  IRR: {irr:.2%}")
    print(f"  Payback: {payback:.2f} anos")
    print("-" * 40)

    print("Resultado esperado:")
    print(f"  +{life_extension} anos de vida útil")
    print(f"  ROI {'positivo' if npv > 0 else 'negativo'} ({((annual_revenue * life_extension - investment) / investment):.2%})")
    print("  Missão aprovada" if npv > 0 and irr > discount_rate else "  Missão rejeitada")
    print("-" * 40)

if __name__ == "__main__":
    analyze_geo_satellite_mission()
