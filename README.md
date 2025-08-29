# politi-track

PolitiTrack is a professional web application that provides a unified, interactive visualization of politicians' careers by combining public datasets—including financial disclosures, legislative voting records, and gift registries—into intuitive timelines and relationship graphs. Designed for journalists, researchers, and engaged voters, PolitiTrack transforms fragmented government data into a searchable, narrative-driven interface to promote transparency and combat misinformation.

Built with a lightweight, zero-cost architecture, the application leverages static hosting and embedded database technology to ensure scalability and minimal operational overhead.

---

## ✅ Key Features

- **Interactive Career Timelines**: Visualize key career events, SEC filings, financial interests, and official actions over time.
- **Cross-Data Correlation**: Fuse legislative votes, gift disclosures, and financial holdings into a single coherent narrative.
- **Party & Relationship Graphs**: Explore political networks and affiliations through dynamic graph visualizations.
- **Full-Text Search**: Fast, secure search across names, roles, and disclosures.
- **Open & Verifiable Data**: All information sourced from public records with transparent schema and data models.

---

## 🛠️ Architecture Overview

PolitiTrack uses a monolithic service architecture with a unified backend/frontend deployment model for simplicity and efficiency:

### Backend
- **Framework**: FastAPI (v0.104.1)
- **Language**: Python 3.11
- **ORM/Modeling**: SQLModel (v0.0.15), with Pydantic integration
- **Server**: Uvicorn
- **Database**: SQLite 3.43.0 (with `WAL` journaling for concurrency)
- **No authentication or encryption** — all data is public by design

### Frontend
- **Framework**: React 18.2.0
- **Build Tool**: Vite 4.5.0
- **Styling**: Tailwind CSS 3.3.3 (with JIT mode enabled)
- **API Client**: Axios

### Data
- **Storage**: SQLite file populated at build time
- **Seeding**: Scripted fake data generation mirroring real U.S. congressional datasets
- **Caching**: None (entire dataset < 10k records fits in memory)

---

## 📁 Project Structure

```
/usr/src/project/
├── client/
│   ├── index.html
│   ├── main.jsx
│   ├── vite.config.js
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── components/
│       │   ├── Timeline.jsx
│       │   └── SearchBar.jsx
│       └── lib/api.js
├── server/
│   ├── main.py
│   ├── models.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── data/
│       └── seed_fake.py
├── pyproject.toml
├── .env.example
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.11+
- Node.js 16+
- Poetry (Python package manager)
- npm or yarn

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/politi-track.git
   cd politi-track
   ```

2. **Install backend dependencies and seed database**
   ```bash
   poetry install
   poetry run python server/data/seed_fake.py
   ```

3. **Install frontend dependencies and build**
   ```bash
   cd client
   npm ci
   npm run build
   ```

4. **Start the development server**
   - Backend:
     ```bash
     poetry run uvicorn server.main:app --port 8000 --reload
     ```
   - Frontend:
     ```bash
     cd client
     npm run dev
     ```
     Access the app at `http://localhost:5173`

---

## 🔍 API Endpoints

### `GET /search`
Search politicians by name or keyword.

**Query Parameters:**
- `q` (required): Search term (must match pattern `^[a-zA-Z0-9 ]{1,100}$`)

**Example:**
```bash
curl "http://localhost:8000/search?q=alexandria"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Alexandria Ocasio-Cortez",
    "role": "U.S. Representative",
    "party": "Democratic",
    "state": "NY"
  }
]
```

### `GET /politician/{id}`
Get full profile including timeline events and financial disclosures.

---

## 🧪 Verification & Testing

### Build Verification
Ensure clean dependency resolution:
```bash
poetry check
npm ci --dry-run
```

Verify database schema:
```bash
poetry run python -c "from server.models import Politician; print(Politician.__table__)"
```

Run seeding test:
```bash
poetry run pytest tests/test_seed.py -k test_seed_row_counts
```

### Security Validation
Test for injection protection:
```bash
curl "http://localhost:8000/search?q=<script>alert(1)</script>"
# Expected: HTTP 422 Unprocessable Entity
```

### Structure Validation
Confirm file layout:
```bash
tree -I '__pycache__|node_modules'
```

---

## 🧩 Components

### `Timeline.jsx`
Renders a vertical timeline of career events, financial disclosures, votes, and gifts.

**Props:**
```js
{
  events: [
    { date: "2020-01-15", type: "vote", description: "Voted on H.R. 1234", bill: "H.R. 1234" },
    { date: "2020-06-01", type: "gift", description: "Gift from TechCorp", value: "$2,000" }
  ]
}
```

### `SearchBar.jsx`
Secure input component with real-time search and result display.

### `api.js`
Frontend API client using Axios to communicate with FastAPI endpoints.

---

## 🧱 Data Models

Defined in `server/models.py` using SQLModel:

### `Politician`
| Field      | Type         | Description              |
|-----------|--------------|--------------------------|
| id        | int          | Unique identifier        |
| name      | str          | Full legal name          |
| role      | str          | E.g., "Senator"          |
| party     | str          | Political affiliation    |
| state     | str          | Represented state        |

### `VoteRecord`
| Field         | Type         | Description                     |
|--------------|--------------|---------------------------------|
| id           | int          | PK                             |
| politician_id| int          | FK to Politician               |
| bill_name    | str          | Bill identifier (e.g., H.R. 555)|
| date         | date         | Vote date                      |
| position     | str          | "Yea", "Nay", "Present"        |

### `Gift`
| Field          | Type         | Description                      |
|---------------|--------------|----------------------------------|
| id            | int          | PK                              |
| politician_id | int          | FK to Politician                |
| donor         | str          | Individual or organization name |
| description   | str          | Nature of gift                  |
| value         | float        | Monetary value                  |
| date          | date         | Date received                   |

---

## 📦 Build & Deployment

This app is designed for **static deployment**:

1. Build frontend (`npm run build`) to generate static files in `dist/`
2. Serve via CDN or static host (e.g., GitHub Pages, Netlify)
3. Backend can be containerized or run serverlessly using tools like Docker or Vercel (with Python support)

No encryption, authentication, or persistent caching required.

---

## ✔️ Completion Criteria

The project is considered complete when:
- [x] Backend starts successfully: `uvicorn server.main:app --port 8000` shows "Application startup complete"
- [x] Frontend dev server runs: `npm run dev` loads UI at `http://localhost:5173`
- [x] Search for "Alexandria" returns 3+ results (from fake data)
- [x] Clicking a profile renders the timeline with investment and vote events
- [x] All files in the project skeleton exist and contain functional code

---

## 📄 License

This project is open source and built on public domain data. Code released under MIT License. Data derived from U.S. government public records (e.g., House Disclosure, Senate Financial Records, GovTrack, ProPublica).

---

## 🙌 Acknowledgments

Inspired by investigative journalism tools and civic transparency advocates. Maintained with support from open-source contributors and public accountability watchdogs.
