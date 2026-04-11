# StudyBuddy API Reference

## Authentication Endpoints

### Login
```
POST /login
Content-Type: application/json
Body: {"username": "user@example.com", "password": "password"}
Response: Redirects to /dashboard
```

### Register
```
POST /register
Content-Type: application/json
Body: {"username": "newuser", "email": "user@example.com", "password": "password", "confirm_password": "password"}
Response: Redirects to /login
```

### Logout
```
GET /logout
Response: Redirects to /login
```

## Document Endpoints

### Upload PDF
```
POST /upload
Content-Type: multipart/form-data
Body: pdf_file (binary)
Response: {
  "message": "Success",
  "document_id": 1,
  "summary": "Generated 2-3 paragraph summary",
  "flashcards": [
    {"front": "question", "back": "answer"},
    ...
  ],
  "quiz": [
    {
      "question": "question text",
      "options": ["A. option1", "B. option2", "C. option3", "D. option4"],
      "answer": "A"
    },
    ...
  ],
  "audio_url": "/audio/filename.mp3"
}
```

### Get User Documents
```
GET /api/user/documents
Authentication: Required (cookie-based)
Response: [
  {
    "id": 1,
    "filename": "document.pdf",
    "summary": "...",
    "flashcards": 15,  // count
    "quizzes": 8,      // count
    "created_at": "2026-04-08T14:00:00"
  },
  ...
]
```

### Get Document Flashcards
```
GET /api/document/{document_id}/flashcards
Authentication: Required
Response: [
  {
    "id": 1,
    "front": "What is photosynthesis?",
    "back": "The process by which plants convert light energy into chemical energy",
    "times_reviewed": 3
  },
  ...
]
```

### Get Document Quizzes
```
GET /api/document/{document_id}/quizzes
Authentication: Required
Response: [
  {
    "id": 1,
    "question": "What is the capital of France?",
    "options": ["A. London", "B. Paris", "C. Berlin", "D. Madrid"],
    "correct_answer": "B"
  },
  ...
]
```

## Chat Endpoints

### Send Message (AI Chat)
```
POST /api/chat
Content-Type: application/json
Authentication: Required
Body: {
  "message": "What is photosynthesis?",
  "document_id": 1  // optional, for context
}
Response: {
  "user_message": "What is photosynthesis?",
  "ai_response": "Photosynthesis is the process...",
  "timestamp": "2026-04-08T14:05:00"
}
```

### Get Chat History
```
GET /api/chat/history
Authentication: Required
Query Parameters:
  - document_id (optional) - Filter by document
Response: [
  {
    "user": "What is photosynthesis?",
    "ai": "Photosynthesis is...",
    "time": "2026-04-08T14:05:00"
  },
  ...
]
```

## User Profile Endpoints

### Get User Profile
```
GET /api/user/profile
Authentication: Required
Response: {
  "id": 1,
  "username": "student",
  "email": "student@example.com",
  "full_name": "John Doe",
  "bio": "Computer Science student",
  "stats": {
    "total_documents": 5,
    "total_flashcards": 75,
    "total_quizzes": 40,
    "join_date": "2026-04-01"
  }
}
```

### Update User Profile
```
PUT /api/user/profile
Content-Type: application/json
Authentication: Required
Body: {
  "full_name": "John Doe",
  "bio": "Updated bio"
}
Response: {"message": "Profile updated"}
```

## Health & Status

### Health Check
```
GET /health
Response: {"status": "healthy"}
```

## Error Responses

All endpoints return error responses in this format:

```json
{
  "error": "Error message describing what went wrong"
}
```

Common HTTP Status Codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (invalid input)
- `401`: Unauthorized (not logged in)
- `403`: Forbidden (no permission)
- `404`: Not Found (resource doesn't exist)
- `500`: Server Error

## Rate Limiting

Current implementation has these limits:
- PDF file size: 50MB max
- PDF text extraction: 20,000 characters (truncated)
- Chat history: Last 50 messages
- Flashcards per PDF: 15 max
- Quizzes per PDF: 10 max

## Authentication

All protected endpoints require Flask-Login session authentication via cookies. When you login, a session cookie is automatically set. Subsequent requests automatically include this cookie for authentication.

## Example Usage (JavaScript)

```javascript
// Login
const loginRes = await fetch('/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({username: 'user@example.com', password: 'pass'})
});

// Upload PDF
const formData = new FormData();
formData.append('pdf_file', pdfFile);
const uploadRes = await fetch('/upload', {method: 'POST', body: formData});
const uploadData = await uploadRes.json();

// Get documents
const docsRes = await fetch('/api/user/documents');
const docs = await docsRes.json();

// Get flashcards
const fcRes = await fetch(`/api/document/${docId}/flashcards`);
const flashcards = await fcRes.json();

// Chat
const chatRes = await fetch('/api/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({message: 'Hello', document_id: docId})
});
const chatData = await chatRes.json();
```

## Notes

- All timestamps are ISO 8601 format
- Document IDs are unique per user
- Chat messages are stored with user_id isolation
- JSON parsing errors are handled with regex fallback extraction
- API keys (GEMINI_API_KEY) are stored in .env file
