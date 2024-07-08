# badbot

Instagram bot that fetches the availability of courts at a badminton center.\
Badbot scrapes the [website](https://www.bnh.org.nz/play-badminton-2/) upon request, and returns information on the availability of courts through a direct message on Instagram.

## Installation

Create and activate virtual environment (optional), then install dependencies:
```
pip install -r requirements.txt
```

## Usage

Configure "base_config.py" and rename to "config.py".\
In "badbot.py" configure "mode" - defaults to "driver".\
Run "badbot.py".

### Driver mode

Uses [Selenium WebDriver](https://www.selenium.dev/) to handle Instagram direct messages.

### API mode

Uses [Instagram API](https://developers.facebook.com/docs/messenger-platform/instagram/) - requires Instagram API key and additional configuration.
