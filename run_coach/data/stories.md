## intro
* greet
  - utter_greet
  - utter_show_menu

## target time happy path
* select_menu_item{"main_menu":"target"}
    - inform_form
    - form{"name": "inform_form"}
    - form{"name": null}
    - utter_slots_values
    - action_restart

## target time happy path
* select_menu_item{"main_menu":"predicted"}
    - inform_form
    - form{"name": "inform_form"}
    - form{"name": null}
    - utter_slots_values
    - action_restart

## strategy happy path
* select_menu_item{"main_menu":"strategy"}
    - inform_form
    - form{"name": "inform_form"}
    - form{"name": null}
    - utter_slots_values
    - action_restart
