# Tracko Backend

A Django REST API for managing school bus tracking and student transportation.

## Features

- User authentication with JWT
- Role-based access control (Admin, Bus Staff, Teacher, Parent)
- Student management
- Bus and route management
- Student attendance tracking
- RESTful API endpoints

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Tracko/backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the `backend` directory with the following variables:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=tracko
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## API Documentation

### Authentication

#### Register a new user
```http
POST /api/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "password2": "securepassword",
  "first_name": "John",
  "last_name": "Doe",
  "role": "teacher"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

### Available Endpoints

- **Students**: `/api/v1/students/`
- **Buses**: `/api/v1/buses/`
- **Routes**: `/api/v1/routes/`
- **Student Route Assignments**: `/api/v1/student-route-assignments/`
- **Attendance Records**: `/api/v1/attendance-records/`

## Testing

Run the test suite with:
```bash
python manage.py test
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
