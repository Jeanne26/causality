class LTS(object):
    def __init__(self, jsonfile):
        self.states = jsonfile['states']
        self.transitions = jsonfile['transitions']
        self.name = jsonfile['name']
    

class Policy(object):
    def __init__(self, jsonfile):
        self.name = jsonfile['name']
        self.policy = jsonfile['policy']
        self.lts_name = jsonfile['lts']


    def get_state_events(self, state,time):
        return self.policy[state]
    
class CausalSetting(object):
    def __init__(self,policy, jsonfile):
        self.name = jsonfile['name']
        self.policy = policy
        self.context = jsonfile['context']