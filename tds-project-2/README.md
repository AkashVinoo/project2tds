
# Data Analyst Agent Flexible

A FastAPI-based backend service that analyzes Wikipedia tables or Indian High Court case data
from uploaded questions and attachments. It returns structured answers and visualizations via API.

## Features

- 📊 Wikipedia table analysis (top-grossing movies, correlations, etc.)
- ⚖️ Indian High Court delay analytics using Parquet files
- 🧠 Intelligent task routing based on user input
- 🖼️ Auto-generated scatterplots with regression line (base64 PNG)
- 📦 Clean FastAPI architecture

## How to Run

```bash
git clone https://github.com/YOUR_USERNAME/data_analyst_agent_flexible.git
cd data_analyst_agent_flexible

python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
```

## API Endpoint

`POST /api/`

**Body (multipart/form-data):**
- `question_file`: .txt file containing instructions or a URL
- `attachments`: (optional) Parquet files if needed

## Example Usage

Send a Wikipedia URL like:

```
https://en.wikipedia.org/wiki/List_of_highest-grossing_films
```

Or Indian High Court task like:

```
Analyze Indian High Court delays using attached .parquet file.
```

---

## License

MIT
