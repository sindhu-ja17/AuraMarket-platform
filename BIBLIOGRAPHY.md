# Bibliography: AuraMarket Mini-Project

This document outlines the technologies, frameworks, and external libraries utilized in the development of this project.

## 1. Programming Languages
*   **Python**: Core backend language.
*   **JavaScript (Vanilla)**: Client-side scripting for interactivity.
*   **HTML5 & CSS3**: Structure and styling of the web pages.

## 2. Backend Frameworks & Libraries (Python)
*   **[Flask](https://flask.palletsprojects.com/)**: The primary web framework used for routing, templating, and handling HTTP requests.
*   **[Werkzeug](https://werkzeug.palletsprojects.com/)**: A comprehensive WSGI web application library (used alongside Flask for utilities like secure filename handling).
*   **[google-genai](https://pypi.org/project/google-genai/)**: The Google GenAI Python SDK, leveraged in the `ai_engine.py` for features like Sentiment Analysis, Content Moderation, Smart Chatbots, and Product Recommendations.
*   **[python-dotenv](https://pypi.org/project/python-dotenv/)**: Used for loading environment variables from the `.env` file into `os.environ`.
*   **[SQLite3](https://docs.python.org/3/library/sqlite3.html)**: The built-in Python module used as the primary relational database system (`database.db`, `marketplace.db`).
*   **Standard Python Libraries**: `os`, `sys`, `hashlib`, `random`, `time`, `re`, `math`, `collections`, `shutil`, `urllib.parse`, `unittest`.

## 3. Frontend Libraries & Content Delivery Networks (CDNs)
*   **[Feather Icons](https://feathericons.com/)**: Used for scalable vector icons, served via `unpkg`.
*   **[Chart.js](https://www.chartjs.org/)**: JavaScript charting library utilized for data visualization, served via `jsdelivr`.
*   **[Firebase](https://firebase.google.com/)**: Specifically Firebase App and Analytics modules integrated into the platform for analytics tracking, served via `gstatic.com`.
*   **[Google Fonts](https://fonts.google.com/)**: Providing modern typography using the **Inter** and **Outfit** font families.

## 4. Tools & Environment
*   **[Visual Studio Code (VSCode)](https://code.visualstudio.com/)**: Code editor, indicated by the `.vscode` configuration directory.
*   **Virtual Environment (venv)**: Standard Python package for creating isolated virtual environments (present as `.venv`).
