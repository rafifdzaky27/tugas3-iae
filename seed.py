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
        (1, "Tatooine", "Arid", "Desert"),
        (2, "Alderaan", "Temperate", "Grasslands, Mountains"),
        (3, "Yavin IV", "Temperate, Humid", "Jungle, Rainforests"),
        (4, "Naboo", "Temperate", "Grassy Hills, Swamps"),
        (5, "Coruscant", "Temperate", "Cityscape"),
        (6, "Hoth", "Frozen", "Ice Caves, Mountain Ranges"),
        (7, "Dagobah", "Murky", "Swamp, Jungles"),
        (8, "Bespin", "Temperate", "Gas Giant"),
        (9, "Endor", "Temperate", "Forests"),
        (10, "Mustafar", "Hot", "Volcanoes, Lava Rivers")
    ]
    c.executemany("INSERT INTO planets (id, name, climate, terrain) VALUES (?, ?, ?, ?)", planets)
    planet_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM planets").fetchall()}

    # Data karakter
    characters = [
        (1, "Luke Skywalker", "Human", planet_ids["Tatooine"]),
        (2, "Leia Organa", "Human", planet_ids["Alderaan"]),
        (3, "Han Solo", "Human", planet_ids["Corellia"] if "Corellia" in planet_ids else None),
        (4, "C-3PO", "Droid", planet_ids["Tatooine"]),
        (5, "Yoda", "Unknown", planet_ids["Dagobah"]),
        (6, "Darth Vader", "Human", planet_ids["Tatooine"]),
        (7, "Obi-Wan Kenobi", "Human", planet_ids["Stewjon"] if "Stewjon" in planet_ids else None),
        (8, "Chewbacca", "Wookiee", planet_ids["Kashyyyk"] if "Kashyyyk" in planet_ids else None),
        (9, "Rey", "Human", planet_ids["Jakku"] if "Jakku" in planet_ids else None),
        (10, "Kylo Ren", "Human", planet_ids["Chandrila"] if "Chandrila" in planet_ids else None),
        (11, "Finn", "Human", None),
        (12, "Poe Dameron", "Human", planet_ids["Yavin IV"]),
        (13, "Mace Windu", "Human", planet_ids["Haruun Kal"] if "Haruun Kal" in planet_ids else None),
        (14, "Qui-Gon Jinn", "Human", None),
        (15, "Padmé Amidala", "Human", planet_ids["Naboo"])
    ]
    c.executemany("INSERT INTO characters (id, name, species, home_planet_id) VALUES (?, ?, ?, ?)", characters)
    character_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM characters").fetchall()}

    # Data kapal
    starships = [
        (1, "Millennium Falcon", "YT-1300 light freighter", "Corellian Engineering"),
        (2, "X-wing", "T-65 X-wing starfighter", "Incom Corporation"),
        (3, "TIE Fighter", "TIE/LN starfighter", "Sienar Fleet Systems"),
        (4, "Star Destroyer", "Imperial-class Star Destroyer", "Kuat Drive Yards"),
        (5, "Death Star", "DS-1 Orbital Battle Station", "Galactic Empire"),
        (6, "Slave I", "Firespray-31-class patrol craft", "Kuat Systems Engineering"),
        (7, "Tantive IV", "CR90 corvette", "Corellian Engineering"),
        (8, "A-wing", "RZ-1 A-wing interceptor", "Alliance Underground Engineering"),
        (9, "Y-wing", "BTL Y-wing starfighter", "Koensayr Manufacturing"),
        (10, "Executor", "Executor-class star dreadnought", "Kuat Drive Yards")
    ]
    c.executemany("INSERT INTO starships (id, name, model, manufacturer) VALUES (?, ?, ?, ?)", starships)
    starship_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM starships").fetchall()}

    # Relasi karakter-kapal
    character_starships = [
        (character_ids["Han Solo"], starship_ids["Millennium Falcon"]),
        (character_ids["Luke Skywalker"], starship_ids["X-wing"]),
        (character_ids["Darth Vader"], starship_ids["TIE Fighter"]),
        (character_ids["Leia Organa"], starship_ids["Tantive IV"]),
        (character_ids["Poe Dameron"], starship_ids["X-wing"]),
        (character_ids["Luke Skywalker"], starship_ids["Millennium Falcon"]),
        (character_ids["Darth Vader"], starship_ids["Star Destroyer"]),
        (character_ids["Chewbacca"], starship_ids["Millennium Falcon"]),
        (character_ids["Han Solo"], starship_ids["Tantive IV"]),
        (character_ids["Leia Organa"], starship_ids["Millennium Falcon"])
    ]
    c.executemany("INSERT INTO character_starships (character_id, starship_id) VALUES (?, ?)", character_starships)
    
    # Data senjata
    weapons = [
        (1, "Lightsaber", "Melee", 100, "Close"),
        (2, "Blaster", "Ranged", 50, "Medium"),
        (3, "Bowcaster", "Ranged", 70, "Long"),
        (4, "Thermal Detonator", "Explosive", 150, "Area"),
        (5, "Force Lightning", "Force", 120, "Medium"),
        (6, "DL-44 Heavy Blaster", "Ranged", 65, "Medium"),
        (7, "Lightsaber Pike", "Melee", 90, "Medium"),
        (8, "Vibroblade", "Melee", 60, "Close"),
        (9, "E-11 Blaster Rifle", "Ranged", 55, "Long"),
        (10, "Wookiee Bowcaster", "Ranged", 75, "Long")
    ]
    c.executemany("INSERT INTO weapons (id, name, type, damage, range) VALUES (?, ?, ?, ?, ?)", weapons)
    weapon_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM weapons").fetchall()}
    
    # Relasi karakter-senjata
    character_weapons = [
        (character_ids["Luke Skywalker"], weapon_ids["Lightsaber"]),
        (character_ids["Han Solo"], weapon_ids["Blaster"]),
        (character_ids["Darth Vader"], weapon_ids["Lightsaber"]),
        (character_ids["Yoda"], weapon_ids["Lightsaber"]),
        (character_ids["Darth Vader"], weapon_ids["Force Lightning"]),
        (character_ids["Chewbacca"], weapon_ids["Bowcaster"]),
        (character_ids["Leia Organa"], weapon_ids["Blaster"]),
        (character_ids["Obi-Wan Kenobi"], weapon_ids["Lightsaber"]),
        (character_ids["Rey"], weapon_ids["Lightsaber"]),
        (character_ids["Kylo Ren"], weapon_ids["Lightsaber"]),
        (character_ids["Mace Windu"], weapon_ids["Lightsaber"]),
        (character_ids["Qui-Gon Jinn"], weapon_ids["Lightsaber"]),
        (character_ids["Han Solo"], weapon_ids["DL-44 Heavy Blaster"]),
        (character_ids["Finn"], weapon_ids["Lightsaber"]),
        (character_ids["Finn"], weapon_ids["Blaster"])
    ]
    c.executemany("INSERT INTO character_weapons (character_id, weapon_id) VALUES (?, ?)", character_weapons)
    
    # Data kendaraan
    vehicles = [
        (1, "Speeder Bike", "74-Z speeder bike", "Aratech Repulsor Company", 500),
        (2, "AT-AT", "All Terrain Armored Transport", "Kuat Drive Yards", 60),
        (3, "Snowspeeder", "T-47 airspeeder", "Incom Corporation", 650),
        (4, "Landspeeder", "X-34 landspeeder", "SoroSuub Corporation", 250),
        (5, "Podracer", "BT410 podracer", "Custom", 900),
        (6, "AT-ST", "All Terrain Scout Transport", "Kuat Drive Yards", 90),
        (7, "Sail Barge", "Luxury sail barge", "Ubrikkian Industries", 100),
        (8, "Sand Crawler", "Digger Crawler", "Corellia Mining Corporation", 30),
        (9, "Tribubble Bongo", "Submarine", "Otoh Gunga", 85),
        (10, "BARC Speeder", "BARC speeder", "Aratech Repulsor Company", 520)
    ]
    c.executemany("INSERT INTO vehicles (id, name, model, manufacturer, max_speed) VALUES (?, ?, ?, ?, ?)", vehicles)
    vehicle_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM vehicles").fetchall()}
    
    # Relasi karakter-kendaraan
    character_vehicles = [
        (character_ids["Luke Skywalker"], vehicle_ids["Landspeeder"]),
        (character_ids["Luke Skywalker"], vehicle_ids["Snowspeeder"]),
        (character_ids["Darth Vader"], vehicle_ids["AT-AT"]),
        (character_ids["Han Solo"], vehicle_ids["Speeder Bike"]),
        (character_ids["Leia Organa"], vehicle_ids["Speeder Bike"]),
        (character_ids["Chewbacca"], vehicle_ids["AT-ST"]),
        (character_ids["Rey"], vehicle_ids["Speeder Bike"]),
        (character_ids["Finn"], vehicle_ids["Snowspeeder"]),
        (character_ids["Poe Dameron"], vehicle_ids["Speeder Bike"]),
        (character_ids["Obi-Wan Kenobi"], vehicle_ids["BARC Speeder"]),
        (character_ids["Qui-Gon Jinn"], vehicle_ids["Tribubble Bongo"]),
        (character_ids["Padmé Amidala"], vehicle_ids["Tribubble Bongo"]),
        (character_ids["Padmé Amidala"], vehicle_ids["Speeder Bike"]),
        (character_ids["Kylo Ren"], vehicle_ids["AT-AT"]),
        (character_ids["C-3PO"], vehicle_ids["Sand Crawler"])
    ]
    c.executemany("INSERT INTO character_vehicles (character_id, vehicle_id) VALUES (?, ?)", character_vehicles)
    
    # Data force orders (Jedi, Sith, dll)
    force_orders = [
        (1, "Jedi Order", "Light", "Ancient order of Force-sensitive peacekeepers", -25000),
        (2, "Sith Order", "Dark", "Ancient order of Force-users devoted to the dark side", -6900),
        (3, "Knights of Ren", "Dark", "Dark side Force-users led by Kylo Ren", 28),
        (4, "Inquisitorius", "Dark", "Dark side Force-sensitive agents of the Galactic Empire", 19),
        (5, "Gray Jedi", "Neutral", "Force-users who walk the line between light and dark", -4000),
        (6, "Jedi Praxeum", "Light", "Luke Skywalker's Jedi academy", 11),
        (7, "Nightsisters", "Dark", "Force-wielding witches from Dathomir", -5000),
        (8, "Guardians of the Whills", "Light", "Spiritual order connected to the Force", -8000),
        (9, "New Jedi Order", "Light", "Luke Skywalker's reformed Jedi Order", 11),
        (10, "Rule of Two", "Dark", "Sith philosophy limiting their numbers to two", -1000)
    ]
    c.executemany("INSERT INTO force_orders (id, name, side, description, founding_year) VALUES (?, ?, ?, ?, ?)", force_orders)
    force_order_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM force_orders").fetchall()}
    
    # Relasi karakter-force_orders
    character_force_orders = [
        (character_ids["Luke Skywalker"], force_order_ids["Jedi Order"], "Jedi Master", 4),
        (character_ids["Darth Vader"], force_order_ids["Sith Order"], "Sith Lord", 13),
        (character_ids["Yoda"], force_order_ids["Jedi Order"], "Grand Master", -800),
        (character_ids["Obi-Wan Kenobi"], force_order_ids["Jedi Order"], "Jedi Master", -25),
        (character_ids["Kylo Ren"], force_order_ids["Knights of Ren"], "Master of the Knights of Ren", 28),
        (character_ids["Rey"], force_order_ids["Jedi Order"], "Jedi Knight", 35),
        (character_ids["Luke Skywalker"], force_order_ids["New Jedi Order"], "Founder", 11),
        (character_ids["Mace Windu"], force_order_ids["Jedi Order"], "Jedi Master", -40),
        (character_ids["Qui-Gon Jinn"], force_order_ids["Jedi Order"], "Jedi Master", -60),
        (character_ids["Darth Vader"], force_order_ids["Jedi Order"], "Jedi Knight", -22)
    ]
    c.executemany("INSERT INTO character_force_orders (character_id, force_order_id, rank, joined_year) VALUES (?, ?, ?, ?)", character_force_orders)

    conn.commit()
    conn.close()
    print("Database berhasil diisi dengan data Star Wars!")

if __name__ == "__main__":
    init_db()  # Pastikan tabel ada
    seed_data()