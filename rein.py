from reinforcement_learning import *
import sys
from mdp import sequential_decision_environment

north = (0, 1)
south = (0,-1)
west = (-1, 0)
east = (1, 0)
policy = {(0, 2): east, (1, 2): east, (2, 2): east, (3, 2): None, (0, 1): north, (2, 1): north,
            (3, 1): None, (0, 0): north, (1, 0): west, (2, 0): west, (3, 0): west,}
agent = PassiveDUEAgent(policy, sequential_decision_environment)
for i in range(200):
    run_single_trial(agent,sequential_decision_environment)
    agent.estimate_U()
agent.U[(0, 0)] > 0.2
True


print("Direction Utility Agent")
print('\n'.join([str(k)+':'+str(v) for k, v in agent.U.items()]))
print("")


north = (0, 1)
south = (0,-1)
west = (-1, 0)
east = (1, 0)
policy = {(0, 2): east, (1, 2): east, (2, 2): east, (3, 2): None, (0, 1): north, (2, 1): north,
            (3, 1): None, (0, 0): north, (1, 0): west, (2, 0): west, (3, 0): west,}
agent = PassiveADPAgent(policy, sequential_decision_environment)
for i in range(100):
    run_single_trial(agent,sequential_decision_environment)

agent.U[(0, 0)] > 0.2
True
agent.U[(0, 1)] > 0.2
True


print("Adaptive Dynamic Programming Agent")
print('\n'.join([str(k)+':'+str(v) for k, v in agent.U.items()]))
print("")


north = (0, 1)
south = (0,-1)
west = (-1, 0)
east = (1, 0)
policy = {(0, 2): east, (1, 2): east, (2, 2): east, (3, 2): None, (0, 1): north, (2, 1): north,
            (3, 1): None, (0, 0): north, (1, 0): west, (2, 0): west, (3, 0): west,}
agent = PassiveTDAgent(policy, sequential_decision_environment, alpha=lambda n: 60./(59+n))
for i in range(200):
    run_single_trial(agent,sequential_decision_environment)
    
agent.U[(0, 0)] > 0.2
True
agent.U[(0, 1)] > 0.2
True


print("Passive Temporal Difference Agent")
print('\n'.join([str(k)+':'+str(v) for k, v in agent.U.items()]))
print("")


north = (0, 1)
south = (0,-1)
west = (-1, 0)
east = (1, 0)
policy = {(0, 2): east, (1, 2): east, (2, 2): east, (3, 2): None, (0, 1): north, (2, 1): north,
            (3, 1): None, (0, 0): north, (1, 0): west, (2, 0): west, (3, 0): west,}
q_agent = QLearningAgent(sequential_decision_environment, Ne=5, Rplus=2, alpha=lambda n: 60./(59+n))
for i in range(200):
    run_single_trial(q_agent,sequential_decision_environment)
    
q_agent.Q[((0, 1), (0, 1))] >= -0.5
True
q_agent.Q[((1, 0), (0, -1))] <= 0.5
True


print("Q-Learning Agent")
print('\n'.join([str(k)+':'+str(v) for k, v in q_agent.Q    .items()]))
