# ToDo Application with FastAPI

## Overview
This repository hosts a to-do application built using **FastAPI**, a modern Python web framework. The application provides a simple yet effective solution for managing tasks, demonstrating key concepts of API development and deployment.

## Features
- **Task Management**: Add, update, delete, and list tasks.
- **FastAPI**: Utilizes FastAPI for creating APIs with fast performance.
- **Database Integration**: Supports SQLite for persistent data storage.
- **Frontend**: Integrates HTML, CSS and JavaScript for a responsive user interface.
- **Docker Support**: Includes a Dockerfile for containerization.

## Technologies Used
- **Backend**: FastAPI, Python
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Containerization**: Docker

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/marouan-boumchahate/ToDo-FastAPI.git
   cd ToDo-FastAPI
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   uvicorn TodoApp.main:app --reload
   ```
   The application will be accessible at `http://127.0.0.1:8000`.

## Docker Support
To run the application in a Docker container:
1. Build the Docker image:
   ```bash
   docker build -t todo-fastapi .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 todo-fastapi
   ```

## File Structure
- `main.py`: Entry point of the application.
- `Dockerfile`: Configuration for building a Docker image.
- `requirements.txt`: List of Python dependencies.
- `todosapp.db`: SQLite database file.
- `templates/`: Contains HTML templates for the frontend.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your proposed changes.

## Contact
For questions or feedback, feel free to reach out:
- **GitHub**: [marouan-boumchahate](https://github.com/marouan-boumchahate)
- **Linkedin**: [marouan boumchahate](https://www.linkedin.com/in/marouan-boumchahate-843543249/)

