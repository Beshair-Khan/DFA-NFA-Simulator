# app.py

import streamlit as st
import matplotlib.pyplot as plt
from automata.dfa import DFA
from automata.nfa import NFA
from visualizer.graph import draw_automaton
from visualizer.analytics import (
    build_steps_dataframe,
    plot_state_visits,
    plot_acceptance_pie,
    plot_transition_heatmap
)

# PAGE CONFIG 
st.set_page_config(page_title="DFA/NFA Simulator", layout="wide")
st.title("DFA / NFA Simulator")
st.markdown("Build your automaton, test input strings, and explore analytics.")

# SIDEBAR 
st.sidebar.header("Automaton Setup")

mode = st.sidebar.radio("Select Mode", ["DFA", "NFA"])

states_input = st.sidebar.text_input("States (comma separated)", "q0, q1, q2")
alphabet_input = st.sidebar.text_input("Alphabet (comma separated)", "0, 1")
start_state = st.sidebar.text_input("Start State", "q0")
accept_input = st.sidebar.text_input("Accept States (comma separated)", "q2")

st.sidebar.markdown("---")
st.sidebar.subheader("Transitions")
st.sidebar.markdown("Format: `from_state, symbol, to_state` — one per line")

default_transitions = "q0, 0, q0\nq0, 1, q1\nq1, 0, q0\nq1, 1, q2\nq2, 0, q2\nq2, 1, q2"
transitions_input = st.sidebar.text_area("Transitions", default_transitions, height=180)

st.sidebar.markdown("---")
input_string = st.sidebar.text_input("Test Input String", "011")
run_button = st.sidebar.button("▶ Run Simulation")

# PARSE INPUTS 
states = {s.strip() for s in states_input.split(",")}
alphabet = {a.strip() for a in alphabet_input.split(",")}
accept_states = {a.strip() for a in accept_input.split(",")}

transitions = {}
for line in transitions_input.strip().split("\n"):
    parts = [p.strip() for p in line.split(",")]
    if len(parts) == 3:
        from_state, symbol, to_state = parts
        if from_state not in transitions:
            transitions[from_state] = {}
        if mode == "NFA":
            if symbol not in transitions[from_state]:
                transitions[from_state][symbol] = set()
            transitions[from_state][symbol].add(to_state)
        else:
            transitions[from_state][symbol] = to_state

# TABS
tab1, tab2, tab3 = st.tabs(["Simulation", "Analytics", "Transition Table"])

# TAB 1: SIMULATION
with tab1:
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader("Automaton Graph")
        fig = draw_automaton(
            states=states,
            transitions=transitions,
            start_state=start_state,
            accept_states=accept_states,
            title=f"{mode} Graph"
        )
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("Simulation Result")

        if run_button:
            if mode == "DFA":
                automaton = DFA(states, alphabet, transitions, start_state, accept_states)
            else:
                automaton = NFA(states, alphabet, transitions, start_state, accept_states)

            steps, accepted = automaton.run(input_string)

            if accepted:
                st.success(f"✅ ACCEPTED — '{input_string}'")
            else:
                st.error(f"❌ REJECTED — '{input_string}'")

            st.markdown("### Step by Step")
            df = build_steps_dataframe(steps, mode=mode)
            st.dataframe(df, width="stretch")

            # redraw graph with current state highlighted
            if mode == "DFA":
                current = {steps[-1]["state"]}
            else:
                current = steps[-1]["states"]

            st.subheader("Final State Highlighted")
            fig2 = draw_automaton(
                states=states,
                transitions=transitions,
                start_state=start_state,
                accept_states=accept_states,
                current_states=current,
                title=f"Final State"
            )
            st.pyplot(fig2)
            plt.close()
        else:
            st.info("Set up your automaton and press ▶ Run Simulation")

#TAB 2: ANALYTICS 
with tab2:
    st.subheader("Simulation Analytics")

    if run_button:
        col3, col4 = st.columns(2)

        with col3:
            st.plotly_chart(plot_state_visits(steps, mode=mode), width="stretch")

        with col4:
            results = [accepted]
            st.plotly_chart(plot_acceptance_pie(results), width="stretch")
    else:
        st.info("Run a simulation first to see analytics")

# TAB 3: TRANSITION TABLE
with tab3:
    st.subheader("Transition Heatmap")
    st.plotly_chart(plot_transition_heatmap(transitions, states), width="stretch")