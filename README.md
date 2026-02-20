# FlaskAuthApp

A simple Flask authentication application with server-side validation.

## Features

- User Registration
- Server-side validation for:
    - Empty Name, Email, Password
    - Unique Email
    - Password Minimum Length (6 chars)
- Flash messages for errors and success

## Deployment

This app is designed to be deployed on Render.

## local Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
