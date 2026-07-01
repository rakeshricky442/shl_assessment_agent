# SHL Assessment Recommendation Agent

An AI-powered SHL Assessment Recommendation Agent built using FastAPI, FAISS, and Google's Gemini API.

The system helps recruiters identify the most suitable SHL assessments based on job requirements while supporting clarification, recommendation refinement, assessment comparison, and out-of-scope request handling.

---

## Features

- SHL catalog retrieval using FAISS vector search
- FastAPI REST API
- Stateless conversation handling
- Context extraction from conversation history
- AI-powered assessment recommendations using Gemini
- Assessment comparison using SHL catalog data
- Clarification for incomplete user queries
- Recommendation refinement when user changes requirements
- Refusal of non-SHL related requests

---

## Project Architecture

User
↓
FastAPI (/chat)
↓
Context Builder
↓
Planner
↓
Retriever (FAISS)
↓
Gemini LLM
↓
SHL Assessment Recommendations

---

## Tech Stack

- Python 3.11
- FastAPI
- Google Gemini API
- FAISS
- Sentence Transformers
- Pydantic
- Uvicorn

---

## Folder Structure

```
shl-assessment-agent/
│
├── app/
│   ├── agent.py
│   ├── planner.py
│   ├── context_builder.py
│   ├── retriever.py
│   ├── catalog_service.py
│   ├── llm.py
│   ├── main.py
│   └── conversation.py
│
├── scraper/
│   └── fetch_catalog.py
│
├── data/
│   └── catalog.json
│
├── vectorstore/
│   ├── faiss.index
│   └── metadata.pkl
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Installation

Clone the repository

```bash
[git clone https://github.com/rakeshricky442/shl_assessment_agent.git
]
cd shl_assessment_agent
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

Mac/Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

Example

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Run the Project

```bash
uvicorn app.main:app --reload
```

API

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Health Check

```
GET /health
```

Response

```json
{
    "status":"ok"
}
```

---

### Chat

```
POST /chat
```

Example Request

```json
{
  "messages":[
    {
      "role":"user",
      "content":"Recommend assessments for graduate Java developers."
    }
  ]
}
```

Example Response

```json
{
  "reply":"Recommended assessments...",
  "recommendations":[
    {
      "name":"Java 8 (New)",
      "url":"https://www.shl.com/...",
      "test_type":"K"
    }
  ],
  "end_of_conversation":true
}
```

---

## Supported Behaviors

- Clarify vague requests
- Recommend SHL assessments
- Refine previous recommendations
- Compare SHL assessments
- Refuse out-of-scope requests

---

## Testing

The project has been tested for:

- Health endpoint
- Clarification flow
- Recommendation flow
- Refinement flow
- Assessment comparison
- Stateless conversation handling
- Long job description parsing
- Out-of-scope request handling

---

## Author

Rakesh
