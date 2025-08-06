# FastAPI Database Application

This project is a FastAPI application that connects to a database using SQLAlchemy. It provides a simple user management system with CRUD operations.

## Project Structure

```
fastapi-db-app
├── src
│   ├── main.py          # Entry point of the FastAPI application
│   ├── db
│   │   └── database.py  # Database connection logic
│   ├── models
│   │   └── user.py      # User model definition
│   ├── routes
│   │   └── user.py      # User-related routes
│   └── types
│       └── index.py     # Custom types and interfaces
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fastapi-db-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the FastAPI application, execute the following command:

```
uvicorn src.main:app --reload
```

You can access the API documentation at `http://127.0.0.1:8000/docs`.

## Contributing

Feel free to submit issues or pull requests for any improvements or features you would like to see in this project.