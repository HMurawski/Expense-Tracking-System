import os
from dotenv import load_dotenv
from contextlib import contextmanager
import mysql.connector
from logging_setup import setup_logger

logger = setup_logger("db_helper")

# Load environment variables
load_dotenv()

def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Missing required environment variable: {var_name}")
    return value

# Retrieve and validate environment variables
try:
    host = get_env_variable("DB_HOST")
    port = int(get_env_variable("DB_PORT"))
    user = get_env_variable("DB_USER")
    password = get_env_variable("DB_PASSWORD")
    database = get_env_variable("DB_NAME")
except ValueError as e:
    logger.error(str(e))
    raise

@contextmanager
def get_db_cursor(commit=False):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor(dictionary=True)
        yield cursor
        if commit:
            connection.commit()
    except mysql.connector.Error as err:
        logger.error(f"Database connection error: {err}")
        if commit:
            connection.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def fetch_all_records():
    """Fetch all records from the expenses table."""
    query = "SELECT * FROM expenses"
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error fetching records: {e}")
        return []

def fetch_expenses_for_date(expense_date):
    """Fetch expenses for a specific date."""
    logger.info(f"Fetching expenses for {expense_date}")
    query = "SELECT * FROM expenses WHERE expense_date = %s"
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query, (expense_date,))
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error fetching expenses for date {expense_date}: {e}")
        return []

def insert_expense(expense_date, amount, category, notes):
    """Insert a new expense."""
    logger.info(f"Inserting expense: {expense_date}, {amount}, {category}, {notes}")
    query = """
        INSERT INTO expenses (expense_date, amount, category, notes)
        VALUES (%s, %s, %s, %s)
    """
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(query, (expense_date, amount, category, notes))
    except Exception as e:
        logger.error(f"Error inserting expense: {e}")

def delete_expenses_for_date(expense_date):
    """Delete all expenses for a specific date."""
    logger.info(f"Deleting expenses for {expense_date}")
    query = "DELETE FROM expenses WHERE expense_date = %s"
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(query, (expense_date,))
    except Exception as e:
        logger.error(f"Error deleting expenses for date {expense_date}: {e}")

def fetch_expense_summary(start_date, end_date):
    """Fetch summary of expenses between two dates."""
    logger.info(f"Fetching expense summary for {start_date} to {end_date}")
    query = """
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE expense_date BETWEEN %s AND %s
        GROUP BY category
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query, (start_date, end_date))
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error fetching expense summary: {e}")
        return []


if __name__ == "__main__":
    # Example function calls:
    #fetch_all_records()
    fetch_expenses_for_date("2024-08-02")
    # insert_expense("2024-08-24", 30, "Food", "Pizza")
    # delete_expenses_for_date("2024-08-20")
    # fetch_expenses_for_date("2024-08-24")
    # summary = fetch_expense_summary("2024-08-01", "2024-08-03")
    # for record in summary:
    #     print(record)
