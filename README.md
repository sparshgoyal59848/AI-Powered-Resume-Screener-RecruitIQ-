# 🎯 RecruitIQ — AI-Powered Resume Screener

An intelligent resume screening system that parses resumes, matches skills to job descriptions, and ranks candidates using NLP and ML — with a beautiful HR dashboard.

---

## Features

- **PDF & TXT parsing** via PyPDF2 + file reading
- **Named Entity Recognition** for candidate name extraction (spaCy)
- **Skill extraction** across 50+ skills in 5 categories (programming, web, data, cloud/devops, soft skills)
- **TF-IDF semantic similarity** between resume and JD (scikit-learn)
- **Education scoring** (Bachelor → Master → PhD tier weighting)
- **Experience year detection** via regex
- **Composite scoring** with configurable weights (skill 40%, TF-IDF 35%, education 15%, experience 10%)
- **Recommendation tiers**: Strong Hire / Consider / Not Recommended
- **Strengths & weaknesses** per candidate
- **Web dashboard** — upload JD + resumes, view ranked results, filter by tier
- **CLI tool** for terminal-based screening

---

## Project Structure

```
resume-screener/
├── backend/
│   ├── app.py              # Flask API + NLP scoring engine
│   └── requirements.txt
├── frontend/
│   └── index.html          # Single-file dashboard (no build step)
├── sample_resumes/         # 3 demo resumes (txt)
│   ├── alex_morgan_senior_ml.txt
│   ├── priya_sharma_junior.txt
│   └── marcus_chen_backend.txt
├── screen_cli.py           # CLI screener
├── run.sh                  # One-command setup + start
└── README.md
```

---

## Quick Start

### Option A — Web Dashboard (recommended)

```bash
# 1. Make the run script executable
chmod +x run.sh

# 2. Run setup + server (creates venv automatically)
./run.sh

# 3. Open http://localhost:5000 in your browser
```

### Option B — Manual Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Download spaCy model
python3 -m spacy download en_core_web_sm

# Start server
cd backend && python3 app.py
```

### Option C — CLI Tool

```bash
# Screen all resumes in a folder
python3 screen_cli.py --jd my_jd.txt --resumes ./sample_resumes/

# Screen specific files, show top 5
python3 screen_cli.py --jd my_jd.txt --resumes cv1.pdf cv2.txt --top 5
```

---

## How It Works

### Scoring Algorithm

| Component         | Weight | Method                              |
|-------------------|--------|-------------------------------------|
| Skill Match       | 40%    | Keyword extraction + set overlap    |
| Content Relevance | 35%    | TF-IDF cosine similarity            |
| Education         | 15%    | Keyword tier matching               |
| Experience        | 10%    | Regex year extraction vs JD req     |

### Recommendation Tiers

| Score   | Tier             |
|---------|------------------|
| ≥ 75%   | ✅ Strong Hire   |
| 50–74%  | 🟡 Consider      |
| < 50%   | ❌ Not Recommended |

---

## API Endpoints

| Method | Endpoint     | Description                            |
|--------|--------------|----------------------------------------|
| POST   | /api/screen  | Upload JD + resumes, returns ranked JSON |
| GET    | /api/health  | Health check                           |

### POST /api/screen

**Form Data:**
- `jd` — job description text
- `resumes` — one or more PDF/TXT files

**Response:**
```json
{
  "total": 3,
  "jd_skills": ["python", "tensorflow", "aws"],
  "jd_exp_required": 5,
  "candidates": [
    {
      "rank": 1,
      "name": "Alex Morgan",
      "email": "alex.morgan@email.com",
      "final_score": 82.4,
      "recommendation": "Strong Hire",
      "matched_skills": ["python", "tensorflow", "aws"],
      "missing_skills": [],
      "strengths": ["Strong skill alignment", "Advanced education"],
      "weaknesses": []
    }
  ]
}
```

---

## Extending the Project

- **Add more skills** → edit `SKILL_KEYWORDS` in `backend/app.py`
- **Adjust weights** → edit `compute_final_score()` in `backend/app.py`
- **Support DOCX** → add `python-docx` and a handler in `extract_text()`
- **Add database** → connect SQLite/PostgreSQL to persist screening sessions
- **Export to CSV** → add `/api/export` route that returns CSV of results

---

## Tech Stack

| Layer      | Tech                                      |
|------------|-------------------------------------------|
| Backend    | Python 3, Flask, Flask-CORS               |
| NLP        | spaCy (en_core_web_sm), scikit-learn TF-IDF |
| PDF Parser | PyPDF2                                    |
| Frontend   | Vanilla HTML/CSS/JS (zero dependencies)   |

---

## Sample Demo

Use the 3 included sample resumes with the built-in "Load sample JD" button on the dashboard to see the screener in action immediately.
