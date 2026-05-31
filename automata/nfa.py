class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
    def epsilon_closure(self, states):
        closure=set(states)
        stack=list(states)
        while stack:
            state=stack.pop()
            eps_trgets=self.transitions.get(state, {}).get("ε", set())
            for target in eps_trgets:
                if target not in closure:
                    closure.add(target)
                    stack.append(target)
        return closure
    def move(self, states, symbol):
        result=set()
        for state in states:
            targets=self.transitions.get(state, {}).get(symbol,set())
            result.update(targets)
        return result
    def run(self, input_string):
        current_states=self.epsilon_closure({self.start_state})
        steps=[]
        steps.append({
            "step":0,
            "states": set(current_states),
            "symbol": None,
            "accepted": bool(current_states & self.accept_states)
        })
        for i, symbol in enumerate(input_string):

            if symbol not in self.alphabet:
                steps.append({
                    "step": i + 1,
                    "states": set(),
                    "symbol": symbol,
                    "accepted": False
                })
                return steps, False
            moved = self.move(current_states, symbol)
            current_states = self.epsilon_closure(moved)

            steps.append({
                "step": i + 1,
                "states": set(current_states),
                "symbol": symbol,
                "accepted": bool(current_states & self.accept_states)
            })

        accepted = bool(current_states & self.accept_states)
        return steps, accepted
    