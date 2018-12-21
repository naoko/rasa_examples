from rasa_core.policies import KerasPolicy, MemoizationPolicy, FallbackPolicy, FormPolicy
from rasa_core.agent import Agent

if __name__ == '__main__':
    agent = Agent("data/domain.yml",
                  policies=[KerasPolicy(), MemoizationPolicy(),
                            FallbackPolicy(), FormPolicy()])

    agent.visualize("data/stories.md",
                    output_file="graph.html", max_history=2)
