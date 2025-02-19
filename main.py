import os
import logging
import asyncio
import requests
import csv
import sqlite3
import datetime

from dotenv import load_dotenv
load_dotenv()

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig
from langchain_openai import ChatOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
CSV_URL = "https://www.nseindia.com/companies-listing/corporate-filings-actions"
DB_NAME = "nse_corporate_actions.db"
TABLE_NAME = "corporate_actions"
DATA_DIR = "data"  # Directory to store CSV files


#Fetch keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")



def create_table(db_name, table_name):
    """Creates the database table if it doesn't exist."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                Symbol TEXT,
                Company_Name TEXT,
                Security_Type TEXT,
                Ex_Date TEXT,
                Purpose TEXT,
                Record_Date TEXT,
                BC_Start_Date TEXT,
                BC_End_Date TEXT,
                ND_Start_Date TEXT,
                ND_End_Date TEXT,
                Actual_Payment_Date TEXT,
                Remarks TEXT,
                DateTime_Downloaded TEXT
            )
        """)
        conn.commit()
        logging.info(f"Table '{table_name}' created (if it didn't exist) in database '{db_name}'.")
    except sqlite3.Error as e:
        logging.error(f"Error creating table: {e}")
    finally:
        if conn:
            conn.close()


def insert_data(db_name, table_name, csv_file):
    """Inserts data from the CSV file into the database table."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Skip the header row

            # Prepare the SQL query for inserting data
            placeholders = ', '.join(['?'] * len(header))
            sql = f"INSERT INTO {table_name} VALUES ({placeholders}, ?)"  # Add DateTime_Downloaded

            for row in csv_reader:
                # Add the current timestamp to each row
                row_with_timestamp = row + [datetime.datetime.now().isoformat()]
                cursor.execute(sql, row_with_timestamp)

        conn.commit()
        logging.info(f"Data inserted successfully from '{csv_file}' into table '{table_name}'.")
    except sqlite3.Error as e:
        logging.error(f"Error inserting data: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during data insertion: {e}")
    finally:
        if conn:
            conn.close()

async def main():
    """Main function to orchestrate the download and database insertion."""

    # Create the data directory if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        logging.info(f"Created directory: {DATA_DIR}")

    # Generate filename based on current date
    today = datetime.date.today()
    csv_filename = os.path.join(DATA_DIR, f"nse_corporate_actions_{today.strftime('%Y%m%d')}.csv")

    # Configure Browser
    browser_config = BrowserConfig(headless=True,
                                   disable_security=True,
                                   new_context_config=BrowserContextConfig(
                        save_downloads_path="data/",
                    ),)  # Keep headful for debugging
    browser = Browser(config=browser_config)

    # Configure Agent
    llm = ChatOpenAI(model='gpt-4o-mini', api_key=OPENAI_API_KEY)
    
    agent = Agent(
        task=f"""
        1. Go to the NSE corporate actions page (https://www.nseindia.com/companies-listing/corporate-filings-actions).
        2. Download the CSV file
        3. Select the 'SME' tab and download the CSV file
        4. Select the 'Debt' tab and download the CSV file
        5. Select the 'MF' tab and download the CSV file
        """,
        llm=llm,
        browser=browser,
    )

    try:
        # Run the agent
        history = await agent.run(max_steps=20)

        # Check if the CSV file was downloaded
        if os.path.exists(csv_filename):
            logging.info(f"CSV downloaded successfully to {csv_filename}")

            # Create the database table
            create_table(DB_NAME, TABLE_NAME)

            # Insert data into the database
            insert_data(DB_NAME, TABLE_NAME, csv_filename)
        else:
            logging.error(f"CSV file not found after agent execution.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        await browser.close()  # Ensure browser is closed

if __name__ == "__main__":
    asyncio.run(main())