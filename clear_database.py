import sqlite3

def connect_db():
    return sqlite3.connect('tv_reviews.db')

def delete_all_data_from_table(table_name):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute(f'DELETE FROM {table_name}')
        conn.commit()
        conn.close()
        print(f"All data from {table_name} has been deleted.")
    except Exception as e:
        print(f"Error deleting data from {table_name}: {e}")

def delete_all_data():
    tables = ['reviews', 'favorites', 'programs', 'users']
    for table in tables:
        delete_all_data_from_table(table)

if __name__ == "__main__":
    delete_all_data()
