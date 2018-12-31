RASA Bot with Authentication
============================
Goal is to build bot flow to 
- Ask for credential for actions that requires
- Don't ask for auth if already authenticated

Handle this with Checkpoint and FormAction

# train nlu and dialog
```bash
cd auth_required_actions
python train_nlu.py
python train_dialog.py 
```

# start conversation
```bash
cd auth_required_actions
sh start_conversation.sh
```

# Conversation example
```markdown
[User] Hi
[Bot] Hello, please select the following things I can do
1. just say hi (no auth required)
2. tell you secret (auth required)
[User] 1
[Bot] Hello
[User] 2
[Bot] What's your email address?
[User] my-name@email.com
[Bot] Okay, I sent you verification code to your email. Please enter the code.
[User] 12345
[Bot] Thank you. You are authorized.
[Bot] Here is the secret
[User] 2
[Bot] Here is my another secret
```
