import json

def save_automaton(states, alphabet, transitions, start_state, accept_states, mode, filepath):
    
    # convert sets to lists because JSON doesn't support sets
    data = {
        "mode"         : mode,
        "states"       : list(states),
        "alphabet"     : list(alphabet),
        "start_state"  : start_state,
        "accept_states": list(accept_states),
        "transitions"  : {}
    }

    for from_state, trans in transitions.items():
        data["transitions"][from_state] = {}
        for symbol, to in trans.items():
            if isinstance(to, set):
                data["transitions"][from_state][symbol] = list(to)
            else:
                data["transitions"][from_state][symbol] = to

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

    return True


def load_automaton(filepath):

    with open(filepath, "r") as f:
        data = json.load(f)

    # convert lists back to sets
    states        = set(data["states"])
    alphabet      = set(data["alphabet"])
    accept_states = set(data["accept_states"])
    mode          = data["mode"]
    start_state   = data["start_state"]

    transitions = {}
    for from_state, trans in data["transitions"].items():
        transitions[from_state] = {}
        for symbol, to in trans.items():
            if isinstance(to, list):
                transitions[from_state][symbol] = set(to)
            else:
                transitions[from_state][symbol] = to

    return states, alphabet, transitions, start_state, accept_states, mode