from database import get_db_connection, init_db

def seed_data():
    """Mengisi database dengan data awal Star Wars."""
    conn = get_db_connection()
    c = conn.cursor()

    # Bersihkan data lama
    c.execute("DELETE FROM character_force_orders")
    c.execute("DELETE FROM character_vehicles")
    c.execute("DELETE FROM character_weapons")
    c.execute("DELETE FROM character_starships")
    c.execute("DELETE FROM characters")
    c.execute("DELETE FROM starships")
    c.execute("DELETE FROM weapons")
    c.execute("DELETE FROM vehicles")
    c.execute("DELETE FROM force_orders")
    c.execute("DELETE FROM planets")
    conn.commit()

    # Data planet
    planets = [
        ("Tatooine", "Arid", "Desert"),
        ("Alderaan", "Temperate", "Grasslands, Mountains"),
        ("Yavin IV", "Temperate, Humid", "Jungle, Rainforests"),
        ("Naboo", "Temperate", "Grassy Hills, Swamps"),
        ("Coruscant", "Temperate", "Cityscape"),
    ]
    c.executemany("INSERT INTO planets (name, climate, terrain) VALUES (?, ?, ?)", planets)
    planet_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM planets").fetchall()}

    # Data karakter
    characters = [
        ("Luke Skywalker", "Human", planet_ids["Tatooine"]),
        ("Leia Organa", "Human", planet_ids["Alderaan"]),
        ("Han Solo", "Human", None),
        ("C-3PO", "Droid", None),
        ("Yoda", "Unknown", None),
        ("Darth Vader", "Human", planet_ids["Tatooine"]),
        ("Obi-Wan Kenobi", "Human", None),
    ]
    c.executemany("INSERT INTO characters (name, species, home_planet_id) VALUES (?, ?, ?)", characters)
    character_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM characters").fetchall()}

    # Data kapal
    starships = [
        ("Millennium Falcon", "YT-1300 light freighter", "Corellian Engineering"),
        ("X-wing", "T-65 X-wing starfighter", "Incom Corporation"),
        ("TIE Fighter", "TIE/LN starfighter", "Sienar Fleet Systems"),
        ("Star Destroyer", "Imperial-class Star Destroyer", "Kuat Drive Yards"),
        ("Death Star", "DS-1 Orbital Battle Station", "Galactic Empire"),
    ]
    c.executemany("INSERT INTO starships (name, model, manufacturer) VALUES (?, ?, ?)", starships)
    starship_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM starships").fetchall()}

    # Relasi karakter-kapal
    character_starships = [
        (character_ids["Han Solo"], starship_ids["Millennium Falcon"]),
        (character_ids["Luke Skywalker"], starship_ids["X-wing"]),
        (character_ids["Darth Vader"], starship_ids["TIE Fighter"]),
    ]
    c.executemany("INSERT INTO character_starships (character_id, starship_id) VALUES (?, ?)", character_starships)
    
    # Data senjata
    weapons = [
        ("Lightsaber", "Melee", 100, "Close"),
        ("Blaster", "Ranged", 50, "Medium"),
        ("Bowcaster", "Ranged", 70, "Long"),
        ("Thermal Detonator", "Explosive", 150, "Area"),
        ("Force Lightning", "Force", 120, "Medium"),
    ]
    c.executemany("INSERT INTO weapons (name, type, damage, range) VALUES (?, ?, ?, ?)", weapons)
    weapon_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM weapons").fetchall()}
    
    # Relasi karakter-senjata
    character_weapons = [
        (character_ids["Luke Skywalker"], weapon_ids["Lightsaber"]),
        (character_ids["Han Solo"], weapon_ids["Blaster"]),
        (character_ids["Darth Vader"], weapon_ids["Lightsaber"]),
        (character_ids["Yoda"], weapon_ids["Lightsaber"]),
        (character_ids["Darth Vader"], weapon_ids["Force Lightning"]),
    ]
    c.executemany("INSERT INTO character_weapons (character_id, weapon_id) VALUES (?, ?)", character_weapons)
    
    # Data kendaraan
    vehicles = [
        ("Speeder Bike", "74-Z speeder bike", "Aratech Repulsor Company", 500),
        ("AT-AT", "All Terrain Armored Transport", "Kuat Drive Yards", 60),
        ("Snowspeeder", "T-47 airspeeder", "Incom Corporation", 650),
        ("Landspeeder", "X-34 landspeeder", "SoroSuub Corporation", 250),
        ("Podracer", "BT410 podracer", "Custom", 900),
    ]
    c.executemany("INSERT INTO vehicles (name, model, manufacturer, max_speed) VALUES (?, ?, ?, ?)", vehicles)
    vehicle_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM vehicles").fetchall()}
    
    # Relasi karakter-kendaraan
    character_vehicles = [
        (character_ids["Luke Skywalker"], vehicle_ids["Landspeeder"]),
        (character_ids["Luke Skywalker"], vehicle_ids["Snowspeeder"]),
        (character_ids["Darth Vader"], vehicle_ids["AT-AT"]),
        (character_ids["Han Solo"], vehicle_ids["Speeder Bike"]),
    ]
    c.executemany("INSERT INTO character_vehicles (character_id, vehicle_id) VALUES (?, ?)", character_vehicles)
    
    # Data force orders (Jedi, Sith, dll)
    force_orders = [
        ("Jedi Order", "Light", "Ancient order of Force-sensitive peacekeepers", -25000),
        ("Sith Order", "Dark", "Ancient order of Force-users devoted to the dark side", -6900),
        ("Knights of Ren", "Dark", "Dark side Force-users led by Kylo Ren", 28),
        ("Inquisitorius", "Dark", "Dark side Force-sensitive agents of the Galactic Empire", 19),
        ("Gray Jedi", "Neutral", "Force-users who walk the line between light and dark", -4000),
    ]
    c.executemany("INSERT INTO force_orders (name, side, description, founding_year) VALUES (?, ?, ?, ?)", force_orders)
    force_order_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM force_orders").fetchall()}
    
    # Relasi karakter-force_orders
    character_force_orders = [
        (character_ids["Luke Skywalker"], force_order_ids["Jedi Order"], "Jedi Master", 4),
        (character_ids["Darth Vader"], force_order_ids["Sith Order"], "Sith Lord", 13),
        (character_ids["Yoda"], force_order_ids["Jedi Order"], "Grand Master", -800),
        (character_ids["Obi-Wan Kenobi"], force_order_ids["Jedi Order"], "Jedi Master", -25),
    ]
    c.executemany("INSERT INTO character_force_orders (character_id, force_order_id, rank, joined_year) VALUES (?, ?, ?, ?)", character_force_orders)

    conn.commit()
    conn.close()
    print("Database berhasil diisi dengan data Star Wars!")

if __name__ == "__main__":
    init_db()  # Pastikan tabel ada
    seed_data()