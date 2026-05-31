import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import networkx as nx

def draw_automaton(states, transitions, start_state, accept_states, current_states=None, title="Automaton"):
    
    # build a directed graph
    G = nx.DiGraph()
    G.add_nodes_from(states)

    # add edges
    edge_labels = {}
    for from_state, trans in transitions.items():
        for symbol, to_states in trans.items():
            if isinstance(to_states, str):
                to_states = {to_states}
            for to_state in to_states:
                if G.has_edge(from_state, to_state):
                    edge_labels[(from_state, to_state)] += f", {symbol}"
                else:
                    G.add_edge(from_state, to_state)
                    edge_labels[(from_state, to_state)] = symbol

    # layout — positions of nodes on the canvas
    pos = nx.spring_layout(G, seed=42)

    # figure size
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.axis("off")

    # color each node based on its role
    node_colors = []
    for state in G.nodes():
        if current_states and state in current_states:
            node_colors.append("#f39c12")      # orange = currently active
        elif state in accept_states:
            node_colors.append("#2ecc71")      # green = accept state
        elif state == start_state:
            node_colors.append("#3498db")      # blue = start state
        else:
            node_colors.append("#bdc3c7")      # grey = normal state

    # draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1500, ax=ax)

    # draw state name labels
    nx.draw_networkx_labels(G, pos, font_size=11, font_weight="bold", ax=ax)

    # draw arrows
    nx.draw_networkx_edges(G, pos, ax=ax, arrows=True,
                           arrowstyle="-|>", arrowsize=25,
                           edge_color="#2c3e50", width=2,
                           connectionstyle="arc3,rad=0.1")

    # draw transition labels on arrows
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 font_size=9, ax=ax)

    # legend
    legend_elements = [
        mpatches.Patch(color="#3498db", label="Start State"),
        mpatches.Patch(color="#2ecc71", label="Accept State"),
        mpatches.Patch(color="#f39c12", label="Current State"),
        mpatches.Patch(color="#bdc3c7", label="Normal State"),
    ]
    ax.legend(handles=legend_elements, loc="upper left", fontsize=9)

    plt.tight_layout()
    return fig

# Example usage:
states = {"q0", "q1","q2"}

transitions = {
    "q0": {"0": "q0", "1": "q1"},
    "q1": {"0": "q0", "1": "q1"},
    "q2": {"0": "q2", "1": "q2"}
}

start_state = "q0"
accept_states = {"q2"}
fig = draw_automaton(
    states,
    transitions,
    start_state,
    accept_states,
    current_states={"q2"},
    title="My DFA"
)
plt.show()