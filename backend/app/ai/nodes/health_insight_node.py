def health_insight_node(state: dict) -> dict:
    health_categories = {"health", "groceries"}
    spend = 0.0
    healthy_spend = 0.0

    for item in state.get("items", []):
        amount = float(item.get("price") or 0)
        spend += amount
        if item.get("category") in health_categories:
            healthy_spend += amount

    score = int((healthy_spend / spend) * 100) if spend > 0 else 0
    note = "Great healthy spending balance" if score >= 50 else "Try adding more healthy purchases"

    state["health_insight"] = {
        "health_score": score,
        "healthy_spend": round(healthy_spend, 2),
        "total_spend": round(spend, 2),
        "notes": [note],
    }
    return state
