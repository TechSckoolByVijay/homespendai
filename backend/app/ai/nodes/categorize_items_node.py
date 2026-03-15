from app.utils.parsing_utils import categorize_item


def categorize_items_node(state: dict) -> dict:
    items = state.get("items", [])
    for item in items:
        item["category"] = categorize_item(item.get("item_name", ""))
    state["items"] = items
    return state
