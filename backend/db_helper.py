import os
from dotenv import load_dotenv
from contextlib import contextmanager
import mysql.connector


load_dotenv()

# Retrieve and validate environment variables
try:
    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT"))  
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")

    if None in [host, port, user, password, database]:
        raise ValueError(
            "Missing required environment variables! Ensure that your .env file contains: "
            "DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME."
        )
except Exception as e:
    print(f"Error loading environment variables: {e}")
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
        try:
            yield cursor
            if commit:
                connection.commit()
        except Exception as e:
            if commit:
                connection.rollback()
            print(f"Error during database operation: {e}")
            raise
        finally:
            print("Closing cursor")
            cursor.close()
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise
    finally:
        if connection:
            connection.close()

def fetch_all_records():
    query = "SELECT * FROM expenses"
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query)
            expenses = cursor.fetchall()
            for expense in expenses:
                print(expense)
    except Exception as e:
        print(f"Error fetching records: {e}")

def fetch_expenses_for_date(expense_date):
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
            expenses = cursor.fetchall()
            for expense in expenses:
                print(expense)
    except Exception as e:
        print(f"Error fetching expenses for date {expense_date}: {e}")

def insert_expense(expense_date, amount, category, notes):
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
                (expense_date, amount, category, notes)
            )
    except Exception as e:
        print(f"Error inserting expense: {e}")

def delete_expenses_for_date(expense_date):
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))
    except Exception as e:
        print(f"Error deleting expenses for date {expense_date}: {e}")

if __name__ == "__main__":
    # Example function calls:
    fetch_all_records()
    # fetch_expenses_for_date("2024-08-01")
    # insert_expense("2024-08-20", 300, "Food", "Panipuri")
    # delete_expenses_for_date("2024-08-20")
    # fetch_expenses_for_date("2024-08-20")
