# Pirate Bay scraper
This tool scrapes The Pirate Bay and adds torrents automatically to Transmission

## Installing
It's recommended to use a virtualenv.

### External dependencies
You'll need to have `chromedriver` in your PATH.

### Python dependencies
```bash
pip install -r requirements.txt
```

## Configuring
Change `localhost` to whatever host Transmission is running on.

## Running
Start Transmission and configure it to enable remote control (RPC).

Then run the script:
```bash
./scraper.py "your search query"
```

## TODO
- support RPC authentication
- everything else
