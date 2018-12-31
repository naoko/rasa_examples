## intro
* greet
  - utter_greet
  - utter_show_menu

## share secret
* select_menu{"main_menu":"share_secret"}
- auth_form
- form{"name": "auth_form"}
- form{"name": null}
- utter_share_secret

## just greeting - no auth required
* select_menu{"main_menu":"greet_me"}
  - utter_greet
  - action_restart
