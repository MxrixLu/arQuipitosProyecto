# Hospital MRI Analysis System

This is a FastAPI-based system for managing and analyzing MRI images in a hospital setting. The system provides endpoints for uploading MRI images, generating diagnoses, and managing patient records.

## Features

- MRI image upload and storage
- Random diagnosis generation (for demonstration purposes)
- Patient record management
- JWT-based authentication
- MongoDB integration
- Modern React frontend with responsive design

## Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:
```
MONGODB_URL=mongodb://localhost:27017
SECRET_KEY=your-secret-key-here
EVENTOS_URL=http://localhost:8002
```

4. Start MongoDB:
Make sure MongoDB is running on your system.

5. Run the backend application:
```bash
uvicorn main:app --reload
```

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the frontend directory with:
```
REACT_APP_API_URL=http://localhost:8000
```

4. Start the frontend development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Project Structure

```
analisis/
├── main.py           # FastAPI entry point
├── models.py         # Data models
├── auth.py          # Authentication
├── requirements.txt  # Backend dependencies
└── frontend/        # React application
    ├── src/         # Source code
    ├── public/      # Static files
    └── package.json # Frontend dependencies
```

## API Endpoints

- `GET /`: Welcome message
- `POST /mri/upload`: Upload an MRI image
- `POST /mri/{mri_id}/analyze`: Generate a diagnosis for an MRI
- `GET /mri/{mri_id}/diagnosis`: Get diagnosis for an MRI
- `GET /patient/{patient_id}/mris`: Get all MRIs for a patient

## Authentication

The API uses JWT tokens for authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-token>
```

## Development Notes

- Both backend and frontend servers need to be running simultaneously during development
- Backend runs on port 8000 by default
- Frontend runs on port 3000 by default
- Make sure MongoDB is running before starting the backend
- The frontend requires the backend to be running for full functionality

## Note

This is a demonstration system. The diagnoses generated are random and should not be used for actual medical purposes. 