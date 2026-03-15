import importlib

from app.ai.nodes.categorize_items_node import categorize_items_node
from app.ai.nodes.extract_items_node import extract_items_node
from app.ai.nodes.health_insight_node import health_insight_node
from app.ai.nodes.spending_insight_node import spending_insight_node

StateGraph = None
START = None
END = None

try:
    langgraph = importlib.import_module("langgraph.graph")
    StateGraph = langgraph.StateGraph
    START = langgraph.START
    END = langgraph.END
except ImportError:
    pass


if StateGraph:
    graph_builder = StateGraph(dict)
    graph_builder.add_node("extract_items", extract_items_node)
    graph_builder.add_node("categorize_items", categorize_items_node)
    graph_builder.add_node("spending_insight", spending_insight_node)
    graph_builder.add_node("health_insight", health_insight_node)

    graph_builder.add_edge(START, "extract_items")
    graph_builder.add_edge("extract_items", "categorize_items")
    graph_builder.add_edge("categorize_items", "spending_insight")
    graph_builder.add_edge("spending_insight", "health_insight")
    graph_builder.add_edge("health_insight", END)

    receipt_graph = graph_builder.compile()
else:
    receipt_graph = None


def run_receipt_graph(state: dict) -> dict:
    if receipt_graph:
        return receipt_graph.invoke(state)

    state = extract_items_node(state)
    state = categorize_items_node(state)
    state = spending_insight_node(state)
    state = health_insight_node(state)
    return state
