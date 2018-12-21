RASA FormAction Example
=======================
- Define `utter_ask_{slot_name}` for slots

# train nlu and dialog
```bash
cd form_bot_run_coach
python train_nlu.py
python train_dialog.py 
```

# start conversation
```bash
cd form_bot_run_coach
sh start_conversation.sh
```

# Conversation example
```bash
hi
Hello! I'm your test bot <3
Select one of the options below.
1: Target Pace (/select_menu_item{"main_menu":"target"})
2: Race Strategy (/select_menu_item{"main_menu":"strategy"})
3: Predicted Finish Time (/select_menu_item{"main_menu":"predicted"})
127.0.0.1 - - [2018-11-27 14:08:16] "POST /webhooks/rest/webhook?stream=true&token= HTTP/1.1" 200 556 0.025918
/select_menu_item{"main_menu":"predicted"}
What's the distance you are running?
127.0.0.1 - - [2018-11-27 14:08:22] "POST /webhooks/rest/webhook?stream=true&token= HTTP/1.1" 200 204 0.098495
10k
Finish time?
127.0.0.1 - - [2018-11-27 14:08:33] "POST /webhooks/rest/webhook?stream=true&token= HTTP/1.1" 200 180 0.138662
50 min
What's the distance of your next race?
127.0.0.1 - - [2018-11-27 14:08:39] "POST /webhooks/rest/webhook?stream=true&token= HTTP/1.1" 200 206 0.144478
marathon
got slots:
 - distance: 26.2
 - next_race_distance: marathon
 - finish_time: 0:50:00

```