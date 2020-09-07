
# Python Standard Libraries
import sqlite3

def get_review_years():
    try:
        conn = sqlite3.connect("./db/results.db")
        cursor = conn.cursor()
        cursor.execute(f"""
                SELECT article_publish_year FROM articles;
                """)
        
        results = cursor.fetchall()
        years=[]
        for result in results:
            years.append(result[0])
        
        return years
    except Exception as e:
        print(e)
        
def get_review_cites():
    try:
        conn = sqlite3.connect("./db/results.db")
        cursor = conn.cursor()
        cursor.execute(f"""
                SELECT article_cites FROM articles;
                """)
        
        results = cursor.fetchall()
        print(results)
        cites=[]
        for result in results:
            cites.append(result[0])
        
        return cites
    except Exception as e:
        print(e)
    