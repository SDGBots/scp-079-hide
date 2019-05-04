# SCP-079-WATCH-HIDE

This bot is used to hide the real watcher.

## How to use

See [this article](https://scp-079.org/watch/).

## To Do List

- [x] Forward messages

## Requirements

- Python 3.6 or higher.
- `requirements.txt` : APScheduler pyrogram[fast]

## Files

- plugins
    - functions
        - `channel.py` : Send messages to channel
        - `etc.py` : Miscellaneous
        - `filters.py` : Some filters
        - `telegram.py` : Some telegram functions
        - `timers.py` : Timer functions
    - handlers
        - `command` : Handle commands
        - `message.py`: Handle messages
    - `glovar.py` : Global variables
- `.gitignore` : Ignore
- `config.ini.example` -> `config.ini` : Configures
- `LICENSE` : GPLv3
- `main.py` : Start here
- `README.md` : This file
- `requirements.txt` : Managed by pip

## Contribute

Welcome to make this project even better. You can submit merge requests, or report issues.

## License

Licensed under the terms of the [GNU General Public License v3](LICENSE).
