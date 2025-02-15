# NSE Corporate Filings Actions Bot

A Python-based bot that automatically downloads corporate filing action data from the [NSE (National Stock Exchange of India)](https://www.nseindia.com/companies-listing/corporate-filings-actions), stores it locally in CSV files, and inserts it into a SQLite database. This project demonstrates an **agent-based approach** to browser automation and data ingestion, which can be scheduled to run daily using GitHub Actions or another scheduler.

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Scheduling with GitHub Actions](#scheduling-with-github-actions)
- [Contributing](#contributing)
- [License](#license)

---

## Features

1. **Automated Browser Agent**  
   Uses the [`browser_use`](https://pypi.org/project/browser-use/) library to programmatically navigate to NSE’s Corporate Filings page and download CSVs.
2. **Data Storage**  
   - CSV files are saved in a local `data/` directory.
   - Data is also inserted into a local SQLite database (`nse_corporate_actions.db`).
3. **Asynchronous Execution**  
   Uses `asyncio` to run the browser automation efficiently.
4. **Logging**  
   Provides logs at various levels to track the status of downloads and database inserts.
5. **Easy Scheduling**  
   Can be set up to run automatically via GitHub Actions (or Windows Task Scheduler, cron jobs, etc.).

---

## How It Works

1. **Agent Initialization**  
   The script spins up a headless (or headful) browser session using `browser_use`.
2. **Navigation and Download**  
   The agent visits [NSE’s Corporate Filings Actions page](https://www.nseindia.com/companies-listing/corporate-filings-actions) and downloads multiple CSVs (Equities, SME, Debt, MF).
3. **Database Insertion**  
   Once downloaded, the CSV files are read, and each row is inserted into a local SQLite database. A timestamp is added to each record.
4. **Scheduling**  
   You can schedule this script to run daily (e.g., at 5 PM) so you always have the latest corporate filings data.

---

## Project Structure

```
NSE_Corp_Filing_Actions_bot/
├─ .github/
│   └─ workflows/
│       └─ daily.yml            # (Optional) GitHub Actions workflow file
├─ data/
│   └─ ...                      # CSV files downloaded here
├─ main.py                      # Main script (async agent, downloads + DB insertion)
├─ requirements.txt             # Python dependencies
├─ .gitignore                   # Ignores sensitive files, logs, etc.
└─ README.md                    # This file
```

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/BharatBheesetti/NSE_Corp_Filing_Actions_bot.git
   cd NSE_Corp_Filing_Actions_bot
   ```

2. **Create a virtual environment (optional but recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install the required packages**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## Usage

1. **Set Up Environment Variables**  
   See [Environment Variables](#environment-variables) below to configure your OpenAI or other API keys.

2. **Run the Script**:

   ```bash
   python main.py
   ```

3. **Check Logs**  
   The script uses Python’s `logging` module. You can see logs in the console or redirect them to a file if desired.

4. **Check Downloaded Data**  
   - CSV files are saved to the `data/` directory by default.
   - The SQLite database (`nse_corporate_actions.db`) is created in the project root directory.

---

## Environment Variables

To avoid committing secrets to version control, the script references these keys via `os.getenv(...)`:

- `OPENAI_API_KEY`
- `DEEPSEEK_API_KEY`
- `GOOGLE_API_KEY`

### Option A: Set them directly in your environment

On Windows:
```powershell
$env:OPENAI_API_KEY="sk-..."
$env:DEEPSEEK_API_KEY="sk-..."
$env:GOOGLE_API_KEY="AIza..."
```

On Linux/macOS:
```bash
export OPENAI_API_KEY="sk-..."
export DEEPSEEK_API_KEY="sk-..."
export GOOGLE_API_KEY="AIza..."
```

### Option B: Use a `.env` file (for local development)

1. Install [`python-dotenv`](https://pypi.org/project/python-dotenv/) if not already:

   ```bash
   pip install python-dotenv
   ```

2. Create a `.env` file (excluded from Git) in the project root:

   ```bash
   OPENAI_API_KEY=sk-...
   DEEPSEEK_API_KEY=sk-...
   GOOGLE_API_KEY=AIza...
   ```

3. In `main.py`, uncomment the relevant lines:

   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

---

## Scheduling with GitHub Actions

To schedule the script to run daily on GitHub Actions:

1. Create a file at `.github/workflows/daily.yml`:

   ```yaml
   name: Daily NSE Corporate Actions

   on:
     schedule:
       - cron: '0 17 * * *'   # 17:00 UTC daily
     workflow_dispatch:       # allows manual triggers

   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3

         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.10'

         - name: Install dependencies
           run: |
             pip install --upgrade pip
             pip install -r requirements.txt

         - name: Run script
           env:
             OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
             DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
             GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
           run: |
             python main.py
   ```

2. Add your secrets (API keys) under **Settings → Secrets and variables → Actions** in your GitHub repository.  
3. GitHub will run this workflow daily at 17:00 UTC (adjust the cron as needed).

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements, bug fixes, or feature ideas.

---

## License

This project is licensed under the [MIT License](LICENSE) — feel free to modify and reuse it in your own projects.

---

### Disclaimer

This project is not affiliated with the National Stock Exchange of India. Use at your own risk. Ensure you comply with NSE’s website terms of service and local regulations when automating data downloads.