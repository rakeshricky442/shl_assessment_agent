# SHL Assessment Recommendation Agent

An AI-powered FastAPI application that recommends relevant SHL assessments based on a candidate's job description or role requirements.

## Features

- Recommend SHL assessments using AI
- Semantic search using FAISS and Sentence Transformers
- Supports natural language job descriptions
- FastAPI REST API
- Interactive Swagger documentation
- Deployed on Railway

## Tech Stack

- Python 3.11
- FastAPI
- Google Gemini API
- FAISS
- Sentence Transformers
- BeautifulSoup
- Railway
- GitHub

## Live Demo

API Base URL:

https://shlassessmentagent-production.up.railway.app

Swagger Documentation:

https://shlassessmentagent-production.up.railway.app/docs

## Installation

Clone the repository:

```bash
git clone https://github.com/rakeshricky442/shl_assessment_agent.git
cd shl_assessment_agent
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application:

```bash
python -m uvicorn app.main:app --reload
```

## API Endpoints

### Home

```
GET /
```

### Health Check

```
GET /health
```

### Chat

```
POST /chat
```

Example request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Recommend SHL assessments for a Python Data Analyst."
    }
  ]
}
```

## Project Structure

```
app/
├── agent.py
├── planner.py
├── retriever.py
├── context_builder.py
├── catalog_service.py
├── llm.py
├── main.py

data/
vectorstore/
scraper/

requirements.txt
README.md
```

## Deployment

The application is deployed on Railway and is publicly accessible.

## Author

Rakesh
