# tupae-1.0

A simple social media management tool with both CLI and web interfaces.

## Features

- Multi-brand account management
- Schedule posts with optional time
- View and run scheduled posts
- Simple web dashboard with sign up and login

## Usage

Run commands using Python:

```bash
python3 social_manager.py brand add MyBrand
python3 social_manager.py account add MyBrand twitter myusername
python3 social_manager.py post schedule MyBrand twitter "Hello World" --time "2025-01-01 12:00"
python3 social_manager.py post list
python3 social_manager.py post run
```

Run the web dashboard:

```bash
python3 app.py
```

All data is stored locally in `social_data.json`.
