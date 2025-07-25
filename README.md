# tupae-1.0

A simple, all-in-one social media management tool.

## Features
- Post messages to Twitter, Facebook, or Instagram.
- Schedule posts to be sent at a later time.

## Requirements
- Python 3.8 or higher
- `requests` library (optional, for real API calls)

## Usage
Set environment variables for your API tokens before running:

```bash
export TWITTER_TOKEN=your_token
export FACEBOOK_TOKEN=your_token
export INSTAGRAM_TOKEN=your_token
```

Run the tool from the command line:

```bash
# Post immediately to Twitter
python social_media_manager.py post twitter "Hello World"

# Schedule a Facebook post after 60 seconds
python social_media_manager.py schedule facebook "Scheduled message" 60
```

This project is a minimal example and uses placeholder API calls.
