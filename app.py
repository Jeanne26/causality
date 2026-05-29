import json

import dash
from dash import Input, Output, State, callback, dcc, html
import dash_cytoscape as cyto
import networkx as nx
import pickle

app = dash.Dash(__name__)

# Example graph - replace with your own
G =pickle.load(open('graphs/ac_p0.pickle', 'rb'))

for node in G.nodes():
    G.nodes[node]["info"] = f"State {node}"


def build_elements():
    elements = []
    for node in G.nodes():
        elements.append(
            {
                "data": {
                    "id": str(node),
                    "label": str(node),
                    "predicates": " ; ".join(sorted(G.nodes[node].get("predicates", []))),
                },
            }
        )

    for u, v, data in G.edges(data=True):
        elements.append(
            {
                "data": {
                    "id": f"{u}->{v}",
                    "source": str(u),
                    "target": str(v),
                    "label": data.get("label", ""),
                    "weight": data.get("weight", ""),
                    "action": data.get("action", ""),
                }
            }
        )
    return elements


BASE_STYLESHEET = [
    {
        "selector": "node",
        "style": {
            "label": "data(label)",
            "background-color": "#3182bd",
            "color": "#1f2937",
            "font-size": "14px",
            "text-valign": "top",
            "text-halign": "center",
            "width": 34,
            "height": 34,
            "border-width": 2,
            "border-color": "#1d4ed8",
        },
    },
    {
        "selector": "edge",
        "style": {
            "curve-style": "bezier",
            "target-arrow-shape": "triangle",
            "target-arrow-color": "#94a3b8",
            "line-color": "#94a3b8",
            "width": 2,
            "label": "data(label)",
            "font-size": "12px",
            "text-rotation": "autorotate",
            "text-background-color": "white",
            "text-background-opacity": 0.8,
            "text-background-padding": "2px",
        },
    },
]


def _parse_path(path_input):
    if not path_input:
        return []
    nodes = []
    for raw in path_input.split(","):
        value = raw.strip()
        if value:
            nodes.append(value)
    return nodes


def _parse_policy(policy_input):
    if not policy_input:
        return {}
    try:
        parsed = json.loads(policy_input)
    except json.JSONDecodeError:
        return {}

    policy_edges = {}
    for node, action in parsed.items():
        for u, v, data in G.edges(data=True):
            edge_action = data.get("label", data.get("label", ""))
            if str(u) == str(node) and str(edge_action).lower() == str(action).lower():
                policy_edges[(str(u), str(v))] = True
    return policy_edges


def build_stylesheet(highlighted_path, policy_edges):
    stylesheet = list(BASE_STYLESHEET)

    for (u, v) in policy_edges:
        stylesheet.append(
            {
                "selector": f'edge[source = "{u}"][target = "{v}"]',
                "style": {
                    "line-color": "#ef4444",
                    "target-arrow-color": "#ef4444",
                    "width": 4,
                },
            }
        )

    for i in range(len(highlighted_path) - 1):
        u = highlighted_path[i]
        v = highlighted_path[i + 1]
        stylesheet.append(
            {
                "selector": f'edge[source = "{u}"][target = "{v}"]',
                "style": {
                    "line-color": "#2563eb",
                    "target-arrow-color": "#2563eb",
                    "width": 4,
                },
            }
        )

    for node in highlighted_path:
        stylesheet.append(
            {
                "selector": f'node[id = "{node}"]',
                "style": {
                    "background-color": "#22c55e",
                    "border-color": "#16a34a",
                    "width": 38,
                    "height": 38,
                },
            }
        )

    return stylesheet


def build_layout(spacing_factor=1.0):
    roots = "#S0" if "S0" in G.nodes else f"#{next(iter(G.nodes))}"
    return {
        "name": "breadthfirst",
        "roots": roots,
        "directed": True,
        "padding": 30,
        "spacingFactor": spacing_factor,
        "animate": True,
        "animationDuration": 300,
    }


app.layout = html.Div(
    [
        html.H1("NetworkX Graph Visualization"),
        html.P("Tu peux déplacer les nœuds directement à la souris."),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Path (comma-separated nodes):"),
                        dcc.Input(
                            id="path-input",
                            type="text",
                            placeholder="0,1,2",
                            style={"marginRight": "10px", "width": "260px"},
                        ),
                        html.Button("Highlight Path", id="path-btn", n_clicks=0),
                    ],
                    style={"marginBottom": "10px"},
                ),
                html.Div(
                    [
                        html.Label("Policy (JSON format {node: action}):"),
                        dcc.Input(
                            id="policy-input",
                            type="text",
                            placeholder='{"0": "action_a", "1": "action_b"}',
                            style={"marginRight": "10px", "width": "360px"},
                        ),
                        html.Button("Apply Policy", id="policy-btn", n_clicks=0),
                    ],
                    style={"marginBottom": "10px"},
                ),
                html.Div(
                    [
                        html.Label("Repulsion / espacement entre les nœuds:"),
                        dcc.Slider(
                            id="repulsion-slider",
                            min=0.5,
                            max=3.0,
                            step=0.1,
                            value=1.4,
                            marks={
                                0.5: "0.5",
                                1.0: "1",
                                1.5: "1.5",
                                2.0: "2",
                                2.5: "2.5",
                                3.0: "3",
                            },
                        ),
                    ],
                    style={"marginBottom": "18px"},
                ),
            ],
            style={"padding": "10px", "border": "1px solid #ddd", "borderRadius": "8px"},
        ),
        cyto.Cytoscape(
            id="graph",
            elements=build_elements(),
            stylesheet=BASE_STYLESHEET,
            layout=build_layout(1.4),
            style={"width": "100%", "height": "700px", "border": "1px solid #e5e7eb"},
            minZoom=0.2,
            maxZoom=3,
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Attributs du nœud survolé"),
                        html.Pre(id="hover-node-output", style={"whiteSpace": "pre-wrap"}),
                    ],
                    style={"flex": "1", "minWidth": "320px"},
                ),
                html.Div(
                    [
                        html.H3("Attributs de l'arête survolée"),
                        html.Pre(id="hover-edge-output", style={"whiteSpace": "pre-wrap"}),
                    ],
                    style={"flex": "1", "minWidth": "320px"},
                ),
            ],
            style={"display": "flex", "gap": "16px", "marginTop": "16px"},
        ),
        dcc.Store(id="graph-store", data={"path": [], "policy": {}}),
    ],
    style={"padding": "20px", "fontFamily": "Arial, sans-serif"},
)


@callback(
    Output("graph", "layout"),
    Output("graph", "stylesheet"),
    Output("graph-store", "data"),
    Input("path-btn", "n_clicks"),
    Input("policy-btn", "n_clicks"),
    Input("repulsion-slider", "value"),
    State("path-input", "value"),
    State("policy-input", "value"),
    State("graph-store", "data"),
)
def update_graph(path_clicks, policy_clicks, repulsion_value, path_input, policy_input, store_data):
    del path_clicks, policy_clicks

    if not store_data:
        store_data = {"path": [], "policy": {}}

    highlighted_path = _parse_path(path_input)
    policy_edges = _parse_policy(policy_input)

    store_data["path"] = highlighted_path
    store_data["policy"] = {f"{u}->{v}": True for u, v in policy_edges}

    return build_layout(repulsion_value), build_stylesheet(highlighted_path, policy_edges), store_data


@callback(
    Output("hover-node-output", "children"),
    Output("hover-edge-output", "children"),
    Input("graph", "mouseoverNodeData"),
    Input("graph", "mouseoverEdgeData"),
)
def show_hover_attributes(node_data, edge_data):
    node_text = json.dumps(node_data, indent=2, ensure_ascii=False) if node_data else "Survole un nœud pour voir ses attributs."
    edge_text = json.dumps(edge_data, indent=2, ensure_ascii=False) if edge_data else "Survole une arête pour voir ses attributs."
    return node_text, edge_text


if __name__ == "__main__":
    app.run(debug=True)