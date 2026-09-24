# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is an AI-powered educational learning assistant.

The project provides:

- AI question answering
- Beginner-friendly concept explanation
- MCQ quiz generation
- Educational text summarization
- Personalized learning paths
- Simple web interface
- FastAPI REST API
- Google Gemini integration
- Optional local LaMini-Flan-T5 explanation

---

# Project Structure

```text
EduGenie/
│
├── main.py
├── gemini_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
├── __init__.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── tests/
    └── test_api.py