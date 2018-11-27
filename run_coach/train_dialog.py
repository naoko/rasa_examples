from rasa_core.policies import KerasPolicy, MemoizationPolicy, FallbackPolicy, FormPolicy
from rasa_core.agent import Agent

# there is a threshold for the NLU predictions as well as the action predictions

agent = Agent(
    'data/domain.yml',
    policies=[
        KerasPolicy(), MemoizationPolicy(),
        FallbackPolicy(), FormPolicy()])

# loading our neatly defined training dialogues
training_data = agent.load_data('data/stories.md')


agent.train(
    training_data,
    validation_split=0.0
)

agent.persist('models/dialogue')
