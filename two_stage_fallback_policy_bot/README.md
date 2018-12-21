Two-stage Fallback Policy
=========================
rasa core introduced two-stage fallback policy in 
version 0.13.0a5.
The doc can be found [here](https://rasa.com/docs/core/master/policies/#two-stage-fallback-policy)

It handles low NLU confidence in multiple stages.
If the predicted confidence is lower than threshold
then it ask for affirmation. If affirmed, bot will continue
the conversation else bot will ask to rephrase.
User then enter intent again. If the intent confidence is low again
the bot will ask for affirmation again. If affirmed
bot will continue the conversation otherwise it will
go to ultimate fallback which by default
 "fallback_action_name" which by default utter `utter_default`.
Make sure to also include that in domain file.

To use this, add the following in your policy config
```yaml
policies:
  - name: TwoStageFallbackPolicy
    nlu_threshold: 0.3
    core_threshold: 0.3
    fallback_action_name: "action_default_fallback"
```

Rasa Core provides the default implementations
`action_default_ask_affirmation` and
`action_default_ask_rephrase` as in:

```python
class ActionDefaultAskAffirmation(Action):
    """Default implementation which asks the user to affirm his intent.
       It is suggested to overwrite this default action with a custom action
       to have more meaningful prompts for the affirmations. E.g. have a
       description of the intent instead of its identifier name.
    """

    def name(self) -> Text:
        return ACTION_DEFAULT_ASK_AFFIRMATION_NAME

    def run(self, dispatcher: 'Dispatcher', tracker: 'DialogueStateTracker',
            domain: 'Domain') -> List[Event]:
        intent_to_affirm = tracker.latest_message.intent.get('name')
        affirmation_message = "Did you mean '{}'?".format(intent_to_affirm)

        dispatcher.utter_button_message(text=affirmation_message,
                                        buttons=[{'title': 'Yes',
                                                  'payload': '/{}'.format(
                                                      USER_INTENT_AFFIRM)},
                                                 {'title': 'No',
                                                  'payload': '/{}'.format(
                                                      USER_INTENT_DENY)}])

        return []


class ActionDefaultAskRephrase(Action):
    """Default implementation which asks the user to rephrase his intent."""

    def name(self) -> Text:
        return ACTION_DEFAULT_ASK_REPHRASE_NAME

    def run(self, dispatcher: 'Dispatcher', tracker: 'DialogueStateTracker',
            domain: 'Domain') -> List[Event]:
        dispatcher.utter_template("utter_ask_rephrase", tracker,
                                  silent_fail=True)

        return []
```

Thus it is required to have the following intents in the domain
```yaml
- affirm
- deny
```

Also have template `utter_ask_rephrase` in `domain.yml`


# train nlu and dialog
```bash
cd two_stage_fallback_policy_bot
python train_nlu.py
sh train_dialog.sh 
```

# start conversation
```bash
cd two_stage_fallback_policy_bot
sh start_conversation.sh
```
