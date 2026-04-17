# NetflixIQ — Netflix Analytics Dashboard

A **production-ready full-stack Django web application** that analyzes the Netflix dataset and delivers rich, interactive insights through beautiful charts and dashboards.

---

## Features

| Feature | Details |
|---|---|
| **Analytics Dashboard** | 8+ interactive Chart.js charts — pie, line, bar, histogram |
| **Summary KPIs** | Total titles, movies, TV shows, top country, top genre |
| **Content Growth** | Year-over-year trend line for movies and TV shows |
| **Search & Filter** | Filter by title, type, year, rating, genre, country |
| **Recommendation Engine** | TF-IDF cosine similarity via scikit-learn |
| **REST API** | JSON endpoints for chart data, search, recommendations |
| **Modern UI** | Dark Netflix-inspired theme, Bootstrap 5, animated charts |

---

## Tech Stack

- **Backend**: Django 4.2
- **Data**: Pandas, NumPy
- **ML**: scikit-learn (TF-IDF + cosine similarity)
- **Charts**: Chart.js 4
- **Styling**: Bootstrap 5, custom CSS
- **DB**: SQLite

---

## Quick Start

```bash
# 1. Extract and enter the project
cd netflix_analysis_project

# 2. Run the automated setup
bash setup.sh
```

Then open **http://127.0.0.1:8000** in your browser.

---

## Manual Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

---

## Project Structure

```
netflix_analysis_project/
├── manage.py
├── requirements.txt
├── setup.sh
├── README.md
│
├── netflix_project/            # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── analysis_app/               # Main application
│   ├── views.py                # All views + API endpoints
│   ├── urls.py
│   ├── models.py
│   ├── apps.py
│   ├── services/
│   │   ├── data_loader.py      # CSV loading & caching
│   │   ├── analysis.py         # All analytics computations
│   │   └── recommendation.py   # ML recommendation engine
│   └── templates/analysis_app/
│       ├── base.html
│       ├── dashboard.html
│       ├── search.html
│       └── detail.html
│
└── dataset/
    └── netflix_titles.csv      # Netflix dataset
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Analytics dashboard |
| `/search/` | GET | Browse + filter titles |
| `/detail/<show_id>/` | GET | Title detail page |
| `/api/chart-data/` | GET | All chart data as JSON |
| `/api/recommendations/?title=X` | GET | Similar title recommendations |
| `/api/search/?q=X` | GET | Autocomplete search |

---

## Pages

### Dashboard (`/`)
- KPI cards: Total Titles, Movies, TV Shows, Top Country, Top Genre
- 8 interactive charts: type distribution, content growth, top countries, genres, ratings, duration histogram, monthly additions, top directors

### Browse (`/search/`)
- Full-text title search
- Filters: Type, Rating, Year, Genre, Country
- Results table with recommendation modal on click

---

## Dataset

The included `dataset/netflix_titles.csv` is a representative sample dataset with 800 titles containing all required fields:
`show_id`, `type`, `title`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `duration`, `listed_in`, `description`

To use the real Kaggle Netflix dataset, replace the CSV file with the one from:
https://www.kaggle.com/datasets/shivamb/netflix-shows

---

## License

MIT — Free to use and modify.
