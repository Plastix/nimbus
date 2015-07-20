# Nimbus
Little Slack bot for Overcast Network's slack channel

## Running
1. `git clone https://github.com/bcbwilla/nimbus`
2. `cd nimbus/`
3. `pip install -r requirements.txt` (preferably in a 
[virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/))
3. Put your [authentication token](https://api.slack.com/web) in the config file (an example config is [example_config.yaml](example_config.yaml))
4. `python nimbus.py config.yaml`

## Contributing
- Feel free to add functionality that you think would be useful!
- Follow [PEP8](https://www.python.org/dev/peps/pep-0008/) style guidelines (most importantly, 
`underscore_names` for things that aren't classes)

## Plugins & Commands
- To add a new plugin, create a new python module in `/plugins/` and include a top level class that extends either
`Plugin` or `CommandPlugin`. The bot will automatically load the plugin when it starts up
- Read the documentation in [Plugin.py](https://github.com/bcbwilla/nimbus/blob/master/plugin.py) to learn about the structure
of Nimbus plugins
- [Echo.py](https://github.com/bcbwilla/nimbus/blob/master/plugins/echo.py) is a simple example plugin

## Suggestions & Bugs
- Create an issue on Github

## License
[MIT License](LICENSE.txt)

