# RecruitIQ — AI-Powered Resume Screening & Job Matching System

RecruitIQ is an AI-powered recruitment assistant that evaluates resumes against job descriptions and generates an intelligent candidate suitability score.

The system combines a fine-tuned Large Language Model (LoRA), local inference, and Groq-based AI inference to analyze candidate resumes, identify matching skills, detect skill gaps, and provide explainable recruitment insights.

---

## 🚀 Project Overview

RecruitIQ is designed to automate the initial stage of the recruitment process.

Traditionally, recruiters need to manually review a large number of resumes and compare them with job descriptions. This process can be time-consuming and inconsistent.

RecruitIQ addresses this problem by allowing a recruiter to:

1. Upload a candidate resume.
2. Provide a job description.
3. Extract text automatically from the resume.
4. Analyze the candidate against the job requirements.
5. Generate a compatibility score.
6. Identify matching skills.
7. Identify missing or weak skills.
8. Generate reasoning for the score.
9. Store previous evaluations.
10. Review candidate evaluation history.

---

## 🎯 Problem Statement

Recruiters often receive hundreds of resumes for a single job position.

Manual resume screening creates several challenges:

- High time consumption
- Repetitive manual work
- Difficulty maintaining consistent evaluation standards
- Important skills may be overlooked
- Comparing resumes against job descriptions can be inefficient
- Recruiters may struggle to identify skill gaps quickly

RecruitIQ provides an AI-assisted solution for faster and more consistent initial resume screening.

---

## 💡 Key Features

### 1. Resume Upload

Recruiters can upload candidate resumes for analysis.

Supported processing includes:

- PDF
- DOCX
- Text extraction
- OCR for scanned documents

### 2. Job Description Analysis

RecruitIQ accepts the job description and compares it with the candidate's resume.

The system evaluates:

- Required skills
- Technical skills
- Experience
- Relevant qualifications
- Candidate strengths
- Candidate gaps

### 3. AI Resume Scoring

The system generates a candidate suitability score between:

```text
0 - 100
```

Higher scores indicate stronger alignment between the resume and the job description.

Example:

```json
{
  "score": 82,
  "confidence": 91,
  "reasoning": "The candidate has strong Python and machine learning experience that closely matches the job requirements.",
  "key_matches": [
    "Python",
    "Machine Learning",
    "SQL"
  ],
  "key_gaps": [
    "AWS",
    "Docker"
  ]
}
```

### 4. Fine-Tuned LoRA Model

RecruitIQ uses a fine-tuned language model through a LoRA adapter.

The fine-tuned model is hosted separately on Hugging Face:

```text
Sriramkumarm95/recruitiq-lora-v2
```

The model is used specifically for resume-to-job-description evaluation.

### 5. Local AI Inference

During local development, RecruitIQ can send evaluation requests to a locally running inference service.

Architecture:

```text
RecruitIQ Flask App
        |
        v
LOCAL_MODEL_URL
        |
        v
Local Inference API
        |
        v
Base Language Model
        +
LoRA Adapter
        |
        v
Resume Evaluation
```

This allows the fine-tuned model to be tested locally without deploying the model inside the Flask application.

### 6. Groq Fallback

If the local fine-tuned model is unavailable, RecruitIQ can fall back to Groq inference.

The fallback model currently used is:

```text
openai/gpt-oss-120b
```

Architecture:

```text
                 ┌──────────────────────┐
                 │     RecruitIQ App    │
                 └──────────┬───────────┘
                            │
                            v
                 ┌──────────────────────┐
                 │ Local LoRA Inference │
                 └──────────┬───────────┘
                            │
                    Available?
                      /           \
                    YES            NO
                     |              |
                     v              v
              Fine-Tuned LoRA    Groq API
                     |              |
                     └──────┬───────┘
                            v
                    Resume Evaluation
```

This provides an additional layer of reliability during development and testing.

---

## 🧠 AI Evaluation Pipeline

The evaluation process follows this workflow:

```text
Candidate Resume
       |
       v
Resume Text Extraction
       |
       v
Job Description
       |
       v
Resume + Job Description
       |
       v
AI Evaluation
       |
       v
Score Generation
       |
       +------------------+
       |                  |
       v                  v
Key Matches          Key Gaps
       |                  |
       +--------+---------+
                |
                v
          AI Reasoning
                |
                v
        Final Evaluation
```

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
                         │     Recruiter       │
                         └──────────┬──────────┘
                                    │
                                    v
                         ┌─────────────────────┐
                         │    RecruitIQ UI     │
                         │      Flask App      │
                         └──────────┬──────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   │                │                │
                   v                v                v
             Resume Upload     Google OAuth      Evaluation
                   │                │                │
                   v                │                v
            Text Extraction         │          AI Evaluation
                   │                │                │
                   │                │        ┌───────┴────────┐
                   │                │        │                │
                   │                │        v                v
                   │                │   Local LoRA         Groq
                   │                │   Inference          Fallback
                   │                │        │                │
                   │                │        └───────┬────────┘
                   │                │                │
                   └────────────────┼────────────────┘
                                    v
                              Evaluation Result
                                    │
                       ┌────────────┼────────────┐
                       │            │            │
                       v            v            v
                    Score      Key Matches   Key Gaps
                       │            │            │
                       └────────────┼────────────┘
                                    v
                              Supabase DB
                                    │
                                    v
                              History Page
```

---

## 🔄 End-to-End Workflow

### Step 1 — User Authentication

The recruiter signs into RecruitIQ using Google authentication.

```text
User
  |
  v
Google OAuth
  |
  v
RecruitIQ
```

### Step 2 — Resume Upload

The recruiter uploads the candidate's resume.

```text
Resume
  |
  v
RecruitIQ
```

### Step 3 — Text Extraction

RecruitIQ extracts the resume content.

For PDF files, the system can use:

- PDF text extraction
- OCR when required

For DOCX files, document text is extracted programmatically.

```text
Resume File
     |
     v
File Detection
     |
     +------ PDF ------> PDF Text Extraction
     |
     +------ DOCX -----> DOCX Text Extraction
     |
     +-- Scanned PDF --> OCR
     |
     v
Resume Text
```

### Step 4 — Job Description Input

The recruiter provides the job description.

The system receives:

```text
Resume Text
+
Job Description
```

### Step 5 — AI Evaluation

RecruitIQ attempts to use the local fine-tuned LoRA model first.

```text
Local Model Available?
       |
   +---+---+
   |       |
  YES      NO
   |       |
   v       v
 LoRA     Groq
   |       |
   +---+---+
       |
       v
Evaluation Result
```

### Step 6 — Candidate Score

The AI generates:

- Overall score
- Confidence
- Reasoning
- Key matching skills
- Key skill gaps

### Step 7 — Store Evaluation

Evaluation information can be stored in Supabase for future reference.

### Step 8 — View History

Recruiters can review previous evaluations through the history functionality.

---

# 🧩 Technology Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Web Framework | Flask |
| Frontend | HTML / CSS / JavaScript |
| Authentication | Google OAuth |
| Authentication Framework | Flask-Dance |
| Session Management | Flask-Login |
| Database | Supabase |
| Resume Processing | pdfplumber |
| DOCX Processing | python-docx |
| OCR | Tesseract / pytesseract |
| PDF Image Conversion | pdf2image |
| Primary AI Model | Fine-Tuned LoRA Model |
| Model Adapter | LoRA / PEFT |
| Local Inference | FastAPI-based inference service |
| AI Fallback | Groq |
| Groq Model | openai/gpt-oss-120b |
| Model Hosting | Hugging Face |
| Development Tunnel | ngrok |
| Environment Configuration | python-dotenv |
| Deployment Target | Hugging Face Spaces |
| Version Control | Git / GitHub |

---

# 🤖 AI Model Architecture

RecruitIQ separates the web application from AI model inference.

```text
                    RecruitIQ
                       |
                       v
              Flask Web Application
                       |
                       v
              Local Inference API
                       |
                       v
                Base Model
                       +
                 LoRA Adapter
                       |
                       v
              Fine-Tuned Model
                       |
                       v
             Resume Evaluation
```

The LoRA adapter allows the base model to be specialized for the recruitment/resume evaluation task without requiring the entire base model to be fine-tuned.

---

# 📁 Project Structure

```text
recruitiq/
│
├── app.py
│
├── local_inference.py
│
├── templates/
│   ├── login.html
│   ├── index.html
│   ├── history.html
│   └── ...
│
├── Dockerfile
│
├── Procfile
│
├── requirements.txt
│
├── README.md
│
├── test_model.py
│
├── .gitignore
│
└── recruitiq-lora-v2/
    └── Local model files
```

### Important

The local LoRA model directory is intentionally excluded from GitHub.

Large model files such as:

```text
*.safetensors
*.bin
*.pt
*.pth
*.gguf
```

are ignored by Git.

The model is hosted separately on Hugging Face.

---

# 🔐 Environment Variables

RecruitIQ uses environment variables for API keys and configuration.

Example:

```env
GROQ_API_KEY=your_groq_api_key

SUPABASE_URL=your_supabase_url

SUPABASE_KEY=your_supabase_key

GOOGLE_CLIENT_ID=your_google_client_id

GOOGLE_CLIENT_SECRET=your_google_client_secret

LOCAL_MODEL_URL=your_local_model_url
```

Never commit real API keys, OAuth secrets, or credentials to GitHub.

The `.env` file is excluded using `.gitignore`.

---

# 💻 Local Setup

## 1. Clone the repository

```bash
git clone https://github.com/Sriramkumar-35/recruitiq.git
cd recruitiq
```

## 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

## 4. Configure environment variables

Create:

```text
.env
```

Add the required configuration values.

## 5. Run RecruitIQ

```powershell
python app.py
```

The Flask application will start locally.

---

# 🧪 Local AI Inference

The local fine-tuned model runs through the inference service.

The inference service exposes an evaluation endpoint:

```text
POST /score_local
```

Example request:

```json
{
  "resume": "Python developer with 3 years of experience...",
  "jd": "Looking for a Python developer with Flask and SQL experience..."
}
```

Example response:

```json
{
  "score": 82,
  "confidence": 90,
  "reasoning": "The candidate demonstrates strong alignment with the required technical skills.",
  "key_matches": [
    "Python",
    "Flask",
    "SQL"
  ],
  "key_gaps": [
    "AWS"
  ],
  "model_used": "fine-tuned-lora-v2"
}
```

---

# 🌐 Local Model Through ngrok

During development, the local inference service can be exposed using ngrok.

Architecture:

```text
RecruitIQ Flask App
       |
       v
     ngrok
       |
       v
Local Inference Service
       |
       v
Fine-Tuned LoRA Model
```

The application uses:

```env
LOCAL_MODEL_URL=https://your-ngrok-url
```

The application automatically sends requests to:

```text
/score_local
```

---

# 🔁 AI Fallback Strategy

RecruitIQ follows a fallback architecture.

### Primary

```text
Fine-Tuned LoRA Model
```

### Fallback

```text
Groq
openai/gpt-oss-120b
```

This allows the application to continue performing evaluations when the local inference service is unavailable.

---

# 📊 Evaluation Output

RecruitIQ produces several important evaluation fields.

### Score

Represents the overall suitability of the candidate.

```text
0 – 100
```

### Confidence

Represents the model's confidence in the evaluation.

```text
0 – 100
```

### Reasoning

Provides an explanation of why the candidate received the score.

### Key Matches

Lists skills and qualifications that match the job description.

### Key Gaps

Lists important skills or requirements that are missing or insufficiently demonstrated.

---

# 🗄️ Data Storage

Supabase is used as the application's database backend.

Evaluation history can include information such as:

```text
Candidate Evaluation
        |
        +-- Score
        +-- Confidence
        +-- Reasoning
        +-- Key Matches
        +-- Key Gaps
        +-- Evaluation History
```

This allows recruiters to review previous candidate evaluations.

---

# 🔑 Authentication

RecruitIQ supports Google authentication using:

```text
Google OAuth
       |
       v
Flask-Dance
       |
       v
Flask-Login
       |
       v
Authenticated Recruiter
```

OAuth credentials are stored as environment variables and should never be committed to the repository.

---

# 🐳 Docker Support

RecruitIQ includes a Dockerfile for containerized deployment.

The Docker architecture is:

```text
Docker Container
       |
       +-- Flask Application
       |
       +-- Python Dependencies
       |
       +-- Application Configuration
```

The application is designed to listen on the port provided by the deployment environment.

---

# ☁️ Deployment Architecture

The application can be deployed to Hugging Face Spaces.

The planned production architecture is:

```text
                   User
                    |
                    v
          Hugging Face Space
                    |
                    v
             RecruitIQ Flask
                    |
                    v
          Local Model Inference
                    |
                    v
        Hugging Face Model Hub
                    |
                    v
          Fine-Tuned LoRA Model
```

In production, the local development ngrok connection is not required.

---

# 🔒 Security Considerations

The project follows several security practices:

- API keys are stored in environment variables.
- OAuth secrets are not stored in source code.
- `.env` is excluded from Git.
- Large model files are excluded from Git.
- Model files are hosted separately.
- Authentication is required for protected functionality.

Never commit:

```text
.env
API keys
OAuth client secrets
Model weights
Access tokens
Private credentials
```

---

# 🧪 Testing

The project contains:

```text
test_model.py
```

for testing model-related functionality.

Basic Python syntax validation can be performed using:

```powershell
python -m py_compile app.py
```

To verify the local inference service, test:

```text
POST /score_local
```

---

# 🚀 Current Development Status

| Component | Status |
|-----------|--------|
| Flask Application | ✅ Implemented |
| Resume Upload | ✅ Implemented |
| PDF Text Extraction | ✅ Implemented |
| DOCX Text Extraction | ✅ Implemented |
| OCR Support | ✅ Implemented |
| Google Authentication | ✅ Implemented |
| Supabase Integration | ✅ Implemented |
| Fine-Tuned LoRA Model | ✅ Available |
| Local Model Inference | ✅ Working |
| ngrok Local Connection | ✅ Working |
| Groq Fallback | ✅ Implemented |
| Evaluation Scoring | ✅ Implemented |
| Evaluation History | ✅ Implemented |
| Docker Configuration | ✅ Available |
| GitHub Repository | ✅ Available |
| Production Deployment | 🔄 Planned |

---

# 📈 Future Enhancements

Potential future improvements include:

- Batch resume evaluation
- Candidate ranking
- Job-specific scoring criteria
- Advanced skill extraction
- Resume-to-job semantic similarity
- Recruiter analytics dashboard
- Candidate comparison
- Automated interview question generation
- Evaluation report export
- Improved model evaluation and benchmarking
- Production GPU inference
- Monitoring and logging
- More robust structured AI output validation

---

# 🎯 Project Goals

The main goals of RecruitIQ are:

1. Reduce manual resume screening time.
2. Improve consistency in candidate evaluation.
3. Provide explainable AI-assisted recruitment decisions.
4. Identify candidate strengths and skill gaps.
5. Enable recruiters to review evaluation history.
6. Provide a scalable architecture for future recruitment automation.

---

# ⚠️ Disclaimer

RecruitIQ is an AI-assisted recruitment tool intended to support human decision-making.

AI-generated scores and explanations should not be treated as the sole basis for employment decisions. Recruiters should independently review candidates and consider appropriate hiring policies and applicable laws.

---

# 👨‍💻 Author

**Sriramkumar M**

GitHub:

https://github.com/Sriramkumar-35

Project:

https://github.com/Sriramkumar-35/recruitiq

---

# 📜 License

This project is intended for educational, development, and demonstration purposes.

Add an appropriate open-source license before distributing the project publicly.
