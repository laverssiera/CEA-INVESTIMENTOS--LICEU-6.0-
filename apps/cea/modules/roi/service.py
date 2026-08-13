def calculate_roi(investment: float, return_value: float) -> float:
    if investment <= 0:
        raise ValueError("investment must be greater than zero")
    return (return_value - investment) / investment


def calculate_payback(investment: float, monthly_return: float) -> float:
    if monthly_return <= 0:
        raise ValueError("monthly_return must be greater than zero")
    return investment / monthly_return
