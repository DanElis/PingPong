class Agent:
    def __init__(self, policy):
        self._policy = policy

    def get_action(self, state):
        return self._policy(state)

    def set_policy(self, new_policy):
        self._policy = new_policy

    def get_policy(self):
        return self._policy
