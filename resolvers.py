from ariadne import QueryType, MutationType, ObjectType
from database import get_db_connection
import sqlite3

query = QueryType()
mutation = MutationType()
character_type = ObjectType("Character")
planet_type = ObjectType("Planet")
starship_type = ObjectType("Starship")
weapon_type = ObjectType("Weapon")
vehicle_type = ObjectType("Vehicle")
force_order_type = ObjectType("ForceOrder")
character_force_order_type = ObjectType("CharacterForceOrder")

# --- Query Resolvers ---
@query.field("allCharacters")
def resolve_all_characters(_, info):
    conn = get_db_connection()
    try:
        characters = conn.execute("SELECT id, name, species, home_planet_id FROM characters").fetchall()
        return [dict(char) for char in characters]
    finally:
        conn.close()

@query.field("character")
def resolve_character(_, info, id):
    conn = get_db_connection()
    try:
        character = conn.execute("SELECT id, name, species, home_planet_id FROM characters WHERE id = ?", (id,)).fetchone()
        return dict(character) if character else None
    finally:
        conn.close()

@query.field("allPlanets")
def resolve_all_planets(_, info):
    conn = get_db_connection()
    try:
        planets = conn.execute("SELECT id, name, climate, terrain FROM planets").fetchall()
        return [dict(p) for p in planets]
    finally:
        conn.close()

@query.field("planet")
def resolve_planet(_, info, id):
    conn = get_db_connection()
    try:
        planet = conn.execute("SELECT id, name, climate, terrain FROM planets WHERE id = ?", (id,)).fetchone()
        return dict(planet) if planet else None
    finally:
        conn.close()

@query.field("allStarships")
def resolve_all_starships(_, info):
    conn = get_db_connection()
    try:
        starships = conn.execute("SELECT id, name, model, manufacturer FROM starships").fetchall()
        return [dict(s) for s in starships]
    finally:
        conn.close()

@query.field("starship")
def resolve_starship(_, info, id):
    conn = get_db_connection()
    try:
        starship = conn.execute("SELECT id, name, model, manufacturer FROM starships WHERE id = ?", (id,)).fetchone()
        return dict(starship) if starship else None
    finally:
        conn.close()

@query.field("allWeapons")
def resolve_all_weapons(_, info):
    conn = get_db_connection()
    try:
        weapons = conn.execute("SELECT id, name, type, damage, range FROM weapons").fetchall()
        return [dict(w) for w in weapons]
    finally:
        conn.close()

@query.field("weapon")
def resolve_weapon(_, info, id):
    conn = get_db_connection()
    try:
        weapon = conn.execute("SELECT id, name, type, damage, range FROM weapons WHERE id = ?", (id,)).fetchone()
        return dict(weapon) if weapon else None
    finally:
        conn.close()

@query.field("allVehicles")
def resolve_all_vehicles(_, info):
    conn = get_db_connection()
    try:
        vehicles = conn.execute("SELECT id, name, model, manufacturer, max_speed FROM vehicles").fetchall()
        return [dict(v) for v in vehicles]
    finally:
        conn.close()

@query.field("vehicle")
def resolve_vehicle(_, info, id):
    conn = get_db_connection()
    try:
        vehicle = conn.execute("SELECT id, name, model, manufacturer, max_speed FROM vehicles WHERE id = ?", (id,)).fetchone()
        return dict(vehicle) if vehicle else None
    finally:
        conn.close()

@query.field("allForceOrders")
def resolve_all_force_orders(_, info):
    conn = get_db_connection()
    try:
        force_orders = conn.execute("SELECT id, name, side, description, founding_year FROM force_orders").fetchall()
        return [dict(fo) for fo in force_orders]
    finally:
        conn.close()

@query.field("forceOrder")
def resolve_force_order(_, info, id):
    conn = get_db_connection()
    try:
        force_order = conn.execute("SELECT id, name, side, description, founding_year FROM force_orders WHERE id = ?", (id,)).fetchone()
        return dict(force_order) if force_order else None
    finally:
        conn.close()

# --- Nested Resolvers ---
@character_type.field("homePlanet")
def resolve_character_home_planet(character_obj, info):
    home_planet_id = character_obj.get("home_planet_id")
    if not home_planet_id:
        return None
    conn = get_db_connection()
    try:
        planet = conn.execute("SELECT id, name, climate, terrain FROM planets WHERE id = ?", (home_planet_id,)).fetchone()
        return dict(planet) if planet else None
    finally:
        conn.close()

@character_type.field("pilotedStarships")
def resolve_character_piloted_starships(character_obj, info):
    character_id = character_obj.get("id")
    conn = get_db_connection()
    try:
        starships = conn.execute(
            """
            SELECT s.id, s.name, s.model, s.manufacturer
            FROM starships s
            JOIN character_starships cs ON s.id = cs.starship_id
            WHERE cs.character_id = ?
            """,
            (character_id,),
        ).fetchall()
        return [dict(s) for s in starships]
    finally:
        conn.close()

@character_type.field("weapons")
def resolve_character_weapons(character_obj, info):
    character_id = character_obj.get("id")
    conn = get_db_connection()
    try:
        weapons = conn.execute(
            """
            SELECT w.id, w.name, w.type, w.damage, w.range
            FROM weapons w
            JOIN character_weapons cw ON w.id = cw.weapon_id
            WHERE cw.character_id = ?
            """,
            (character_id,),
        ).fetchall()
        return [dict(w) for w in weapons]
    finally:
        conn.close()

@character_type.field("vehicles")
def resolve_character_vehicles(character_obj, info):
    character_id = character_obj.get("id")
    conn = get_db_connection()
    try:
        vehicles = conn.execute(
            """
            SELECT v.id, v.name, v.model, v.manufacturer, v.max_speed
            FROM vehicles v
            JOIN character_vehicles cv ON v.id = cv.vehicle_id
            WHERE cv.character_id = ?
            """,
            (character_id,),
        ).fetchall()
        return [dict(v) for v in vehicles]
    finally:
        conn.close()

@character_type.field("forceOrders")
def resolve_character_force_orders(character_obj, info):
    character_id = character_obj.get("id")
    conn = get_db_connection()
    try:
        force_orders = conn.execute(
            """
            SELECT fo.id as force_order_id, fo.name, fo.side, fo.description, fo.founding_year,
                   cfo.rank, cfo.joined_year, c.id as character_id
            FROM force_orders fo
            JOIN character_force_orders cfo ON fo.id = cfo.force_order_id
            JOIN characters c ON c.id = cfo.character_id
            WHERE c.id = ?
            """,
            (character_id,),
        ).fetchall()
        
        result = []
        for fo in force_orders:
            result.append({
                "character": {"id": fo["character_id"]},
                "forceOrder": {
                    "id": fo["force_order_id"],
                    "name": fo["name"],
                    "side": fo["side"],
                    "description": fo["description"],
                    "founding_year": fo["founding_year"]
                },
                "rank": fo["rank"],
                "joinedYear": fo["joined_year"]
            })
        return result
    finally:
        conn.close()

@planet_type.field("residents")
def resolve_planet_residents(planet_obj, info):
    planet_id = planet_obj.get("id")
    conn = get_db_connection()
    try:
        characters = conn.execute(
            "SELECT id, name, species, home_planet_id FROM characters WHERE home_planet_id = ?",
            (planet_id,),
        ).fetchall()
        return [dict(char) for char in characters]
    finally:
        conn.close()

@starship_type.field("pilots")
def resolve_starship_pilots(starship_obj, info):
    starship_id = starship_obj.get("id")
    conn = get_db_connection()
    try:
        characters = conn.execute(
            """
            SELECT c.id, c.name, c.species, c.home_planet_id
            FROM characters c
            JOIN character_starships cs ON c.id = cs.character_id
            WHERE cs.starship_id = ?
            """,
            (starship_id,),
        ).fetchall()
        return [dict(char) for char in characters]
    finally:
        conn.close()

@weapon_type.field("wielders")
def resolve_weapon_wielders(weapon_obj, info):
    weapon_id = weapon_obj.get("id")
    conn = get_db_connection()
    try:
        characters = conn.execute(
            """
            SELECT c.id, c.name, c.species, c.home_planet_id
            FROM characters c
            JOIN character_weapons cw ON c.id = cw.character_id
            WHERE cw.weapon_id = ?
            """,
            (weapon_id,),
        ).fetchall()
        return [dict(char) for char in characters]
    finally:
        conn.close()

@vehicle_type.field("drivers")
def resolve_vehicle_drivers(vehicle_obj, info):
    vehicle_id = vehicle_obj.get("id")
    conn = get_db_connection()
    try:
        characters = conn.execute(
            """
            SELECT c.id, c.name, c.species, c.home_planet_id
            FROM characters c
            JOIN character_vehicles cv ON c.id = cv.character_id
            WHERE cv.vehicle_id = ?
            """,
            (vehicle_id,),
        ).fetchall()
        return [dict(char) for char in characters]
    finally:
        conn.close()

@force_order_type.field("members")
def resolve_force_order_members(force_order_obj, info):
    force_order_id = force_order_obj.get("id")
    conn = get_db_connection()
    try:
        members = conn.execute(
            """
            SELECT c.id as character_id, c.name, c.species, c.home_planet_id,
                   fo.id as force_order_id, fo.name as force_order_name, fo.side, fo.description, fo.founding_year,
                   cfo.rank, cfo.joined_year
            FROM characters c
            JOIN character_force_orders cfo ON c.id = cfo.character_id
            JOIN force_orders fo ON fo.id = cfo.force_order_id
            WHERE fo.id = ?
            """,
            (force_order_id,),
        ).fetchall()
        
        result = []
        for member in members:
            result.append({
                "character": {
                    "id": member["character_id"],
                    "name": member["name"],
                    "species": member["species"],
                    "home_planet_id": member["home_planet_id"]
                },
                "forceOrder": {"id": member["force_order_id"]},
                "rank": member["rank"],
                "joinedYear": member["joined_year"]
            })
        return result
    finally:
        conn.close()

@character_force_order_type.field("character")
def resolve_character_force_order_character(character_force_order_obj, info):
    character_id = character_force_order_obj.get("character", {}).get("id")
    if not character_id:
        return None
    conn = get_db_connection()
    try:
        character = conn.execute(
            "SELECT id, name, species, home_planet_id FROM characters WHERE id = ?",
            (character_id,),
        ).fetchone()
        return dict(character) if character else None
    finally:
        conn.close()

@character_force_order_type.field("forceOrder")
def resolve_character_force_order_force_order(character_force_order_obj, info):
    force_order_id = character_force_order_obj.get("forceOrder", {}).get("id")
    if not force_order_id:
        return None
    conn = get_db_connection()
    try:
        force_order = conn.execute(
            "SELECT id, name, side, description, founding_year FROM force_orders WHERE id = ?",
            (force_order_id,),
        ).fetchone()
        return dict(force_order) if force_order else None
    finally:
        conn.close()

# --- Mutation Resolvers ---
@mutation.field("createPlanet")
def resolve_create_planet(_, info, input):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO planets (name, climate, terrain) VALUES (?, ?, ?)",
            (input["name"], input.get("climate"), input.get("terrain")),
        )
        conn.commit()
        planet_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        planet = conn.execute("SELECT id, name, climate, terrain FROM planets WHERE id = ?", (planet_id,)).fetchone()
        return dict(planet)
    except sqlite3.IntegrityError:
        conn.rollback()
        raise Exception(f"Planet '{input['name']}' sudah ada.")
    finally:
        conn.close()

@mutation.field("updatePlanet")
def resolve_update_planet(_, info, input):
    conn = get_db_connection()
    try:
        planet = conn.execute("SELECT id, name, climate, terrain FROM planets WHERE id = ?", (input["id"],)).fetchone()
        if not planet:
            raise Exception(f"Planet dengan ID {input['id']} tidak ditemukan.")
        conn.execute(
            "UPDATE planets SET name = ?, climate = ?, terrain = ? WHERE id = ?",
            (
                input.get("name", planet["name"]),
                input.get("climate", planet["climate"]),
                input.get("terrain", planet["terrain"]),
                input["id"],
            ),
        )
        conn.commit()
        updated_planet = conn.execute("SELECT id, name, climate, terrain FROM planets WHERE id = ?", (input["id"],)).fetchone()
        return dict(updated_planet)
    except sqlite3.IntegrityError:
        conn.rollback()
        raise Exception("Nama planet sudah digunakan.")
    finally:
        conn.close()

@mutation.field("deletePlanet")
def resolve_delete_planet(_, info, id):
    conn = get_db_connection()
    try:
        planet = conn.execute("SELECT id FROM planets WHERE id = ?", (id,)).fetchone()
        if not planet:
            raise Exception(f"Planet dengan ID {id} tidak ditemukan.")
        residents = conn.execute("SELECT COUNT(*) FROM characters WHERE home_planet_id = ?", (id,)).fetchone()[0]
        if residents > 0:
            raise Exception(f"Tidak dapat menghapus planet dengan {residents} penduduk.")
        conn.execute("DELETE FROM planets WHERE id = ?", (id,))
        conn.commit()
        return True
    finally:
        conn.close()

@mutation.field("createCharacter")
def resolve_create_character(_, info, input):
    conn = get_db_connection()
    try:
        if input.get("homePlanetId"):
            planet = conn.execute("SELECT id FROM planets WHERE id = ?", (input["homePlanetId"],)).fetchone()
            if not planet:
                raise Exception(f"Planet dengan ID {input['homePlanetId']} tidak ditemukan.")
        conn.execute(
            "INSERT INTO characters (name, species, home_planet_id) VALUES (?, ?, ?)",
            (input["name"], input.get("species"), input.get("homePlanetId")),
        )
        conn.commit()
        char_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        character = conn.execute(
            "SELECT id, name, species, home_planet_id FROM characters WHERE id = ?", (char_id,)
        ).fetchone()
        return dict(character)
    except sqlite3.IntegrityError:
        conn.rollback()
        raise Exception(f"Karakter '{input['name']}' sudah ada.")
    finally:
        conn.close()

@mutation.field("assignStarship")
def resolve_assign_starship(_, info, input):
    conn = get_db_connection()
    try:
        character = conn.execute("SELECT id FROM characters WHERE id = ?", (input["characterId"],)).fetchone()
        starship = conn.execute("SELECT id FROM starships WHERE id = ?", (input["starshipId"],)).fetchone()
        if not character:
            raise Exception(f"Karakter dengan ID {input['characterId']} tidak ditemukan.")
        if not starship:
            raise Exception(f"Kapal dengan ID {input['starshipId']} tidak ditemukan.")
        conn.execute(
            "INSERT OR IGNORE INTO character_starships (character_id, starship_id) VALUES (?, ?)",
            (input["characterId"], input["starshipId"]),
        )
        conn.commit()
        character = conn.execute(
            "SELECT id, name, species, home_planet_id FROM characters WHERE id = ?",
            (input["characterId"],),
        ).fetchone()
        return dict(character)
    finally:
        conn.close()

@mutation.field("updateCharacter")
def resolve_update_character(_, info, input):
    conn = get_db_connection()
    try:
        char = conn.execute("SELECT * FROM characters WHERE id = ?", (input["id"],)).fetchone()
        if not char:
            raise Exception(f"Karakter dengan ID {input['id']} tidak ditemukan.")

        conn.execute(
            "UPDATE characters SET name = ?, species = ?, home_planet_id = ? WHERE id = ?",
            (
                input.get("name", char["name"]),
                input.get("species", char["species"]),
                input.get("homePlanetId", char["home_planet_id"]),
                input["id"],
            ),
        )
        conn.commit()
        updated = conn.execute("SELECT * FROM characters WHERE id = ?", (input["id"],)).fetchone()
        return dict(updated)
    finally:
        conn.close()

@mutation.field("deleteCharacter")
def resolve_delete_character(_, info, id):
    conn = get_db_connection()
    try:
        char = conn.execute("SELECT id FROM characters WHERE id = ?", (id,)).fetchone()
        if not char:
            raise Exception(f"Karakter dengan ID {id} tidak ditemukan.")
        conn.execute("DELETE FROM character_starships WHERE character_id = ?", (id,))
        conn.execute("DELETE FROM characters WHERE id = ?", (id,))
        conn.commit()
        return True
    finally:
        conn.close()

@mutation.field("updateStarship")
def resolve_update_starship(_, info, input):
    conn = get_db_connection()
    try:
        ship = conn.execute("SELECT * FROM starships WHERE id = ?", (input["id"],)).fetchone()
        if not ship:
            raise Exception(f"Kapal dengan ID {input['id']} tidak ditemukan.")
        conn.execute(
            "UPDATE starships SET name = ?, model = ?, manufacturer = ? WHERE id = ?",
            (
                input.get("name", ship["name"]),
                input.get("model", ship["model"]),
                input.get("manufacturer", ship["manufacturer"]),
                input["id"],
            ),
        )
        conn.commit()
        updated = conn.execute("SELECT * FROM starships WHERE id = ?", (input["id"],)).fetchone()
        return dict(updated)
    finally:
        conn.close()

@mutation.field("deleteStarship")
def resolve_delete_starship(_, info, id):
    conn = get_db_connection()
    try:
        ship = conn.execute("SELECT id FROM starships WHERE id = ?", (id,)).fetchone()
        if not ship:
            raise Exception(f"Kapal dengan ID {id} tidak ditemukan.")
        conn.execute("DELETE FROM character_starships WHERE starship_id = ?", (id,))
        conn.execute("DELETE FROM starships WHERE id = ?", (id,))
        conn.commit()
        return True
    finally:
        conn.close()


resolvers = [query, mutation, character_type, planet_type, starship_type, weapon_type, vehicle_type, force_order_type, character_force_order_type]