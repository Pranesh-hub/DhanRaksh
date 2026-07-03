def calculate_fraud(
    amount,
    merchant,
    location,
    count_1m,
    count_5m,
    count_1h
):
    score = 0

    reasons = []

    if amount > 10000:
        score += 40
        reasons.append("High Amount")

    if merchant.risk_score >= 50:
        score += merchant.risk_score * 0.3

        reasons.append(
            "High Risk Merchant"
        )

    if count_1m >= 5:
        score += 25
        reasons.append("High Velocity (1 Minute)")

    if count_5m >= 15:
        score += 20
        reasons.append("High Velocity (5 Minutes)")

    if count_1h >= 20:
        score += 15
        reasons.append("High Velocity (1 Hour)")

    return score, reasons

def risk_level(score):

    if score >= 80:
        return "CRITICAL"

    if score >= 50:
        return "HIGH"

    if score >= 20:
        return "MEDIUM"

    return "LOW"