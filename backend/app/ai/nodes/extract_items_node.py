from app.utils.parsing_utils import sum_prices


def extract_items_node(state: dict) -> dict:
    items = state.get("items", [])
    state["subtotal"] = sum_prices(item.get("price") for item in items)
    return state
