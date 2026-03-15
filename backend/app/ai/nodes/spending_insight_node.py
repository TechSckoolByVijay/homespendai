def spending_insight_node(state: dict) -> dict:
    total = state.get("total", 0.0)
    category_breakdown: dict[str, float] = {}
    for item in state.get("items", []):
        category = item.get("category", "other")
        category_breakdown[category] = category_breakdown.get(category, 0.0) + float(item.get("price") or 0)

    top_category = max(category_breakdown.items(), key=lambda x: x[1])[0] if category_breakdown else "other"
    state["spending_insight"] = {
        "total": total,
        "top_category": top_category,
        "category_breakdown": category_breakdown,
    }
    return state
