# Room Booking System

## Requirements

- Python 3.7+
- Flask
- SQLAlchemy

## Setup

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd Room-Booking-System
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   ```sh
   flask db upgrade
   ```

4. **Run the application:**
   ```sh
   flask run
   ```

## Optional: Initialize Data and Test API

You can run the provided test file to initialize sample data in the database and verify that the API is working as expected.

```sh
python test.py
```