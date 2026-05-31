class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states=states
        self.alphabet=alphabet
        self.transitions=transitions
        self.start_state=start_state
        self.accept_states=accept_states
    def run(self, input_string):
        current_state=self.start_state
        step=[]
        step.append({
            "step": 0,
            "state": current_state,
            "symbol":None,
            "accepted":current_state in self.accept_states
        })
        for i, symbol in enumerate(input_string):
            if symbol not in self.alphabet:
                step.append({
                    "step": i+1,
                    "state": "DEAD",
                    "symbol": symbol,
                    "accepted": False
                })
                return step, False
            if symbol not in self.transitions.get(current_state, {}):
                step.append({
                    "step": i+1,
                    "state": "DEAD",
                    "symbol": symbol,
                    "accepted": False
                })
                return step, False
            current_state=self.transitions[current_state][symbol]
            step.append({
                "step": i+1,
                "state": current_state,
                "symbol": symbol,
                "accepted":current_state in self.accept_states
            })
        accepted=current_state in self.accept_states
        return step, accepted
    
