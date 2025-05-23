import sqlite3

DATABASE_NAME = "starwars.db"

def get_db_connection():
    """Membuka koneksi ke database dengan row factory untuk akses kolom berdasarkan nama."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Membuat tabel jika belum ada."""
    conn = get_db_connection()
    c = conn.cursor()

    # Tabel planets
    c.execute("""
        CREATE TABLE IF NOT EXISTS planets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            climate TEXT,
            terrain TEXT
        )
    """)

    # Tabel characters
    c.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            species TEXT,
            home_planet_id INTEGER,
            FOREIGN KEY (home_planet_id) REFERENCES planets (id)
        )
    """)

    # Tabel starships
    c.execute("""
        CREATE TABLE IF NOT EXISTS starships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            model TEXT,
            manufacturer TEXT
        )
    """)

    # Tabel penghubung characters-starships (many-to-many)
    c.execute("""
        CREATE TABLE IF NOT EXISTS character_starships (
            character_id INTEGER,
            starship_id INTEGER,
            PRIMARY KEY (character_id, starship_id),
            FOREIGN KEY (character_id) REFERENCES characters (id),
            FOREIGN KEY (starship_id) REFERENCES starships (id)
        )
    """)
    
    # Tabel weapons (senjata)
    c.execute("""
        CREATE TABLE IF NOT EXISTS weapons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            type TEXT,
            damage INTEGER,
            range TEXT
        )
    """)
    
    # Tabel penghubung characters-weapons (many-to-many)
    c.execute("""
        CREATE TABLE IF NOT EXISTS character_weapons (
            character_id INTEGER,
            weapon_id INTEGER,
            PRIMARY KEY (character_id, weapon_id),
            FOREIGN KEY (character_id) REFERENCES characters (id),
            FOREIGN KEY (weapon_id) REFERENCES weapons (id)
        )
    """)
    
    # Tabel vehicles (kendaraan)
    c.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            model TEXT,
            manufacturer TEXT,
            max_speed INTEGER
        )
    """)
    
    # Tabel penghubung characters-vehicles (many-to-many)
    c.execute("""
        CREATE TABLE IF NOT EXISTS character_vehicles (
            character_id INTEGER,
            vehicle_id INTEGER,
            PRIMARY KEY (character_id, vehicle_id),
            FOREIGN KEY (character_id) REFERENCES characters (id),
            FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
        )
    """)
    
    # Tabel force_orders (Jedi, Sith, dll)
    c.execute("""
        CREATE TABLE IF NOT EXISTS force_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            side TEXT,
            description TEXT,
            founding_year INTEGER
        )
    """)
    
    # Tabel penghubung characters-force_orders (many-to-many)
    c.execute("""
        CREATE TABLE IF NOT EXISTS character_force_orders (
            character_id INTEGER,
            force_order_id INTEGER,
            rank TEXT,
            joined_year INTEGER,
            PRIMARY KEY (character_id, force_order_id),
            FOREIGN KEY (character_id) REFERENCES characters (id),
            FOREIGN KEY (force_order_id) REFERENCES force_orders (id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tabel berhasil dibuat.")

if __name__ == "__main__":
    init_db()