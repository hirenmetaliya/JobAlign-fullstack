# JobAlign - AI-Powered Job Matching Platform

JobAlign is a full-stack application that helps job seekers find their perfect match using AI technology. It features resume parsing, skill analysis, and intelligent job matching using Google's Gemini AI.

## Features

- Resume parsing and analysis
- AI-powered job matching
- User authentication
- Skill extraction and matching
- Job listing management
- Subscription-based matching system

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Node.js 16 or higher
- PostgreSQL 12 or higher
- Tesseract OCR (for resume parsing)
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/JobAlign-fullstack.git
cd JobAlign-fullstack
```

### 2. Backend Setup

1. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env` in the backend directory
   - Update the following variables in `.env`:
     ```
     DJANGO_SECRET_KEY=your_secret_key
     DJANGO_DEBUG=True
     DB_NAME=jobalign
     DB_USER=your_db_user
     DB_PASSWORD=your_db_password
     DB_HOST=localhost
     DB_PORT=5432
     GOOGLE_GEMINI_API_KEY=your_gemini_api_key
     TESSERACT_CMD=path_to_tesseract_executable
     ```

4. Set up PostgreSQL:
   - Create a new database named 'jobalign'
   - Update the database credentials in `.env`

5. Run database migrations:
```bash
cd backend
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

7. Start the backend server:
```bash
python manage.py runserver
```

### 3. Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## Running the Application

1. Start the backend server (from the backend directory):
```bash
python manage.py runserver
```

2. Start the frontend development server (from the frontend directory):
```bash
npm run dev
```

3. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Admin interface: http://localhost:8000/admin

## Additional Setup Notes

### Tesseract OCR Installation

#### Windows:
1. Download the installer from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install to default location (C:\Program Files\Tesseract-OCR)
3. Add Tesseract to your system PATH

#### macOS:
```bash
brew install tesseract
```

#### Linux:
```bash
sudo apt-get install tesseract-ocr
```

### Google Gemini API

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add the API key to your `.env` file

## Project Structure

```
JobAlign-fullstack/
├── backend/                 # Django backend
│   ├── jobalign/           # Main Django project
│   ├── authentication/     # User authentication app
│   ├── resume_parser/      # Resume parsing app
│   ├── job_matcher/        # Job matching app
│   └── scraper/           # Job scraping utilities
├── frontend/               # React frontend
├── venv/                   # Python virtual environment
├── .env                    # Environment variables (not in git)
├── .env.example           # Example environment variables
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Troubleshooting

1. Database Connection Issues:
   - Ensure PostgreSQL is running
   - Verify database credentials in `.env`
   - Check if the database 'jobalign' exists

2. Tesseract OCR Issues:
   - Verify Tesseract installation
   - Check the path in `.env` matches your system
   - Ensure Tesseract is in your system PATH

3. Frontend Build Issues:
   - Clear node_modules and reinstall:
     ```bash
     rm -rf node_modules
     npm install
     ```

4. Backend Server Issues:
   - Check if all environment variables are set
   - Verify virtual environment is activated
   - Ensure all dependencies are installed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 