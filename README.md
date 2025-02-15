# NSE Corporate Filings Actions Bot

A Python-based bot that automatically downloads corporate filing action data from the [NSE (National Stock Exchange of India)](https://www.nseindia.com/companies-listing/corporate-filings-actions), stores it locally in CSV files, and inserts it into a SQLite database. This project demonstrates an **agent-based approach** to browser automation and data ingestion, which can be scheduled to run daily using GitHub Actions or another scheduler.

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
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


## Scheduling with GitHub Actions

I'm using GitHub Actions to run this script daily. You can edit the YAML file to suit your needs.

Note: I've actually not been able to get Github actions to get this to run successfully. Some issue with browser-use and pypi. YMMV.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements, bug fixes, or feature ideas.

---

## License

This project is licensed under the [MIT License](LICENSE) — feel free to modify and reuse it in your own projects.

---

### Disclaimer

This project is not affiliated with the National Stock Exchange of India. Use at your own risk. Ensure you comply with NSE’s website terms of service and local regulations when automating data downloads.
