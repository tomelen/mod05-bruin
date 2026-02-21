import duckdb
import os

db_path = 'duckdb.db' 

full_path = os.path.abspath(db_path)
print(f"🔍 Looking for database at: {full_path}")

if os.path.exists(db_path):
    size = os.path.getsize(db_path)
    print(f"⚖️ File size: {size / 1024:.2f} KB")
    
    # Using read_only=True is a good habit for local inspection
    with duckdb.connect(db_path, read_only=True) as con:
        # We concatenate schema and table name, and filter out system schemas
        query = """
            SELECT table_schema || '.' || table_name 
            FROM information_schema.tables 
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
        """
        tables = [row[0] for row in con.execute(query).fetchall()]
        
        if tables:
            print(f"✅ Found tables: {tables}")
        else:
            print("❌ No user tables found.")
        
        # Previews
        print("\n--- Top 10 Players ---")
        con.sql("SELECT * FROM dataset.players LIMIT 10").show()

        print("\n--- Top 10 Player Stats ---")
        con.sql("SELECT * FROM dataset.player_stats LIMIT 10").show()
        
else:
    print(f"🚫 File not found at {full_path}")