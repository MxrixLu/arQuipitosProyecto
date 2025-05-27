# Hospital MRI Analysis System

This is a FastAPI-based system for managing and analyzing MRI images in a hospital setting. The system provides endpoints for uploading MRI images, generating diagnoses, and managing patient records.

## Features

- MRI image upload and storage
- Random diagnosis generation (for demonstration purposes)
- Patient record management
- JWT-based authentication
- MongoDB integration

## Setup

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
```

4. Start MongoDB:
Make sure MongoDB is running on your system.

5. Run the application:
```bash
uvicorn main:app --reload
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

## Note

This is a demonstration system. The diagnoses generated are random and should not be used for actual medical purposes. 