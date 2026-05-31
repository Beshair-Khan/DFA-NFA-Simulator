# visualizer/analytics.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def build_steps_dataframe(steps, mode="DFA"):
    
    rows = []
    for step in steps:
        if mode == "DFA":
            rows.append({
                "Step"    : step["step"],
                "State"   : step["state"],
                "Symbol"  : step["symbol"] if step["symbol"] else "START",
                "Accepted": "✅ Yes" if step["accepted"] else "❌ No"
            })
        else:
            rows.append({
                "Step"    : step["step"],
                "States"  : str(step["states"]),
                "Symbol"  : step["symbol"] if step["symbol"] else "START",
                "Accepted": "✅ Yes" if step["accepted"] else "❌ No"
            })

    return pd.DataFrame(rows)


def plot_state_visits(steps, mode="DFA"):

    if mode == "DFA":
        states_visited = [s["state"] for s in steps]
    else:
        states_visited = [state for s in steps for state in s["states"]]

    visit_counts = pd.Series(states_visited).value_counts().reset_index()
    visit_counts.columns = ["State", "Visit Count"]

    fig = px.bar(
        visit_counts,
        x="State",
        y="Visit Count",
        color="State",
        title="How Many Times Each State Was Visited",
        text="Visit Count"
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False)

    return fig


def plot_acceptance_pie(results):

    accepted = sum(1 for r in results if r is True)
    rejected = len(results) - accepted

    fig = px.pie(
        names=["Accepted", "Rejected"],
        values=[accepted, rejected],
        color=["Accepted", "Rejected"],
        color_discrete_map={"Accepted": "#2ecc71", "Rejected": "#e74c3c"},
        title="Accepted vs Rejected Strings"
    )

    return fig


def plot_transition_heatmap(transitions, states):

    alphabet = sorted({sym for trans in transitions.values() for sym in trans.keys() if sym != "ε"})
    state_list = sorted(states)

    matrix = []
    for from_state in state_list:
        row = []
        for symbol in alphabet:
            to = transitions.get(from_state, {}).get(symbol, None)
            row.append(1 if to else 0)
        matrix.append(row)

    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=alphabet,
        y=state_list,
        colorscale="Blues",
        showscale=False,
        text=[[str(transitions.get(r, {}).get(c, "—")) for c in alphabet] for r in state_list],
        texttemplate="%{text}",
        textfont={"size": 12}
    ))

    fig.update_layout(
        title="Transition Heatmap (which state goes where on each symbol)",
        xaxis_title="Symbol",
        yaxis_title="From State"
    )

    return fig

