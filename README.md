# Discord Clone

## Overview
A clone of the popular communication platform Discord, built using Django.

## Features
- User authentication (sign up, login)
- Real-time messaging
- Channel creation and management
- User profiles

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hussein-saad/discord_clone.git
   cd discord_clone
2. **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
4. **Apply migrations:**
    ```bash
    python3 manage.py migrate
5. **Run the development server:**
   ```bash
   python manage.py runserver
6. **Access the application:**
    Open your web browser and go to http://127.0.0.1:8000/.

## Usage
- Sign up for a new account or log in with an existing account.
- Create or join channels to start messaging.

## Deployment

The application is deployed at https://husseinsaad.pythonanywhere.com/.

