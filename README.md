# nimbus

Little slack bot for Overcast Network's slack channel

# running
1. `git clone https://github.com/bcbwilla/nimbus`
2. `cd nimbus/`
3. `pip install -r requirements.txt` (preferably in a 
[virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/))
3. Put your [authentication token](https://api.slack.com/web) in the config file (an example config is [example_config.yaml](example_config.yaml))
4. `python nimbus.py config.yaml`

# contributing
Feel free to add functionality that you think would be useful!

## guidelines
- Follow [PEP8](https://www.python.org/dev/peps/pep-0008/) style guidelines (most importantly, 
`underscore_names` for things that aren't classes)
- For now, pack the new functionality neatly (like in a function, or somewhere else if it is more
complicated (e.g. [link_expander.py](link_expander.py)) and call it from the `process_message` function
- Probably should discuss the functionality in Slack or via issues here to determine if it's
a good idea before spending time on it

# suggestions
- pm me on Slack or create an issue here

# license
[MIT](LICENSE.txt)

