from collections.abc import Iterable


CATEGORY_KEYWORDS = {
    "groceries": ["market", "grocery", "produce", "supermart"],
    "health": ["salad", "fruit", "yogurt", "vitamin"],
    "dining": ["restaurant", "cafe", "burger", "pizza", "meal"],
    "transport": ["fuel", "gas", "uber", "taxi"],
}


def normalize_text(value: str | None) -> str:
    return (value or "").strip().lower()


def categorize_item(item_name: str) -> str:
    name = normalize_text(item_name)
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in name for keyword in keywords):
            return category
    return "other"


def sum_prices(values: Iterable[float | None]) -> float:
    return round(sum(v or 0 for v in values), 2)
