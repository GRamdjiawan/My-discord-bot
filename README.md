
# My Discord Bot

This is my first encounter with the [Discord](https://discordpy.readthedocs.io/en/stable/index.html) library for python. My goal was to embed my friends input. In this case was it for facts of the day

note: The time zone is set to Amsterdam


## Installation

### 1. (optional) Create a virtual environment
```cmd
  cd /to/file/location
  python -m venv .venv
```
#### To activate your virtual environment use
 ```cmd
 .venv\Scripts\activate
 ```

### 2. Install libraries

```cmd
  cd /to/file/location
  pip install -r requirements.txt
```

### 3. Create a .env file
note: if changing the .env file also change the settings.py to match eachother

```vscode
DISCORD_LOG = 'THE LOG CHANNEL ID'
DISCORD_API_TOKEN = 'YOUR API TOKEN'
DISCORD_TARGET_USER = 'YOUR FRIENDS ID'
DISCORD_TARGET_CHANNEL = 'THE CHANNEL ID WHERE YOUR FRIENDS MESSAGE WILL SHOW'
```

    
