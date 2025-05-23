# Star Wars GraphQL API

Selamat datang di Star Wars GraphQL API! Aplikasi ini adalah API GraphQL yang memungkinkan Anda untuk mengakses dan memanipulasi data dari universe Star Wars, termasuk karakter, planet, kapal luar angkasa, senjata, kendaraan, dan organisasi Pengguna Force (Force Orders).

## Daftar Isi

- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Struktur Database](#struktur-database)
- [Relasi Antar Tabel](#relasi-antar-tabel)
- [Cara Kerja API](#cara-kerja-api)
- [Contoh Query](#contoh-query)
- [Contoh Mutation](#contoh-mutation)

## Teknologi yang Digunakan

- **Python 3.8+**: Bahasa pemrograman utama
- **FastAPI**: Web framework untuk membuat API
- **Ariadne**: Library GraphQL untuk Python
- **SQLite**: Database ringan berbasis file
- **Uvicorn**: Server ASGI untuk menjalankan aplikasi FastAPI

## Struktur Database

API ini menggunakan SQLite sebagai database. Berikut adalah struktur tabel yang digunakan:

### 1. Tabel `planets`

Menyimpan data planet di universe Star Wars.

```sql
CREATE TABLE planets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    climate TEXT,
    terrain TEXT
)
```

### 2. Tabel `characters`

Menyimpan data karakter Star Wars.

```sql
CREATE TABLE characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    species TEXT,
    home_planet_id INTEGER,
    FOREIGN KEY (home_planet_id) REFERENCES planets (id)
)
```

### 3. Tabel `starships`

Menyimpan data kapal luar angkasa.

```sql
CREATE TABLE starships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    model TEXT,
    manufacturer TEXT
)
```

### 4. Tabel `weapons`

Menyimpan data senjata.

```sql
CREATE TABLE weapons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    type TEXT,
    damage INTEGER,
    range TEXT
)
```

### 5. Tabel `vehicles`

Menyimpan data kendaraan darat.

```sql
CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    model TEXT,
    manufacturer TEXT,
    max_speed INTEGER
)
```

### 6. Tabel `force_orders`

Menyimpan data organisasi Pengguna Force seperti Jedi Order, Sith Order, dll.

```sql
CREATE TABLE force_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    side TEXT,
    description TEXT,
    founding_year INTEGER
)
```

### 7. Tabel Relasi

Tabel-tabel berikut digunakan untuk menyimpan relasi many-to-many:

```sql
-- Relasi karakter-kapal
CREATE TABLE character_starships (
    character_id INTEGER,
    starship_id INTEGER,
    PRIMARY KEY (character_id, starship_id),
    FOREIGN KEY (character_id) REFERENCES characters (id),
    FOREIGN KEY (starship_id) REFERENCES starships (id)
)

-- Relasi karakter-senjata
CREATE TABLE character_weapons (
    character_id INTEGER,
    weapon_id INTEGER,
    PRIMARY KEY (character_id, weapon_id),
    FOREIGN KEY (character_id) REFERENCES characters (id),
    FOREIGN KEY (weapon_id) REFERENCES weapons (id)
)

-- Relasi karakter-kendaraan
CREATE TABLE character_vehicles (
    character_id INTEGER,
    vehicle_id INTEGER,
    PRIMARY KEY (character_id, vehicle_id),
    FOREIGN KEY (character_id) REFERENCES characters (id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
)

-- Relasi karakter-force_orders
CREATE TABLE character_force_orders (
    character_id INTEGER,
    force_order_id INTEGER,
    rank TEXT,
    joined_year INTEGER,
    PRIMARY KEY (character_id, force_order_id),
    FOREIGN KEY (character_id) REFERENCES characters (id),
    FOREIGN KEY (force_order_id) REFERENCES force_orders (id)
)
```

## Relasi Antar Tabel

### Relasi One-to-Many:
- Satu `planet` dapat memiliki banyak `character` (one-to-many)
  - Relasi ini diimplementasikan melalui kolom `home_planet_id` di tabel `characters`

### Relasi Many-to-Many:
- Satu `character` dapat memiliki banyak `starship`, dan satu `starship` dapat dipiloti oleh banyak `character`
  - Diimplementasikan melalui tabel penghubung `character_starships`
- Satu `character` dapat menggunakan banyak `weapon`, dan satu `weapon` dapat digunakan oleh banyak `character`
  - Diimplementasikan melalui tabel penghubung `character_weapons`
- Satu `character` dapat mengemudikan banyak `vehicle`, dan satu `vehicle` dapat dikemudikan oleh banyak `character`
  - Diimplementasikan melalui tabel penghubung `character_vehicles`
- Satu `character` dapat menjadi anggota dari banyak `force_order`, dan satu `force_order` dapat memiliki banyak `character`
  - Diimplementasikan melalui tabel penghubung `character_force_orders`
  - Tabel ini juga menyimpan informasi tambahan: `rank` (pangkat) dan `joined_year` (tahun bergabung)

## Penjelasan Data Force Orders

Pada kode seed.py, kita mendefinisikan data untuk tabel `force_orders` sebagai berikut:

```python
force_orders = [
    ("Jedi Order", "Light", "Ancient order of Force-sensitive peacekeepers", -25000),
    ("Sith Order", "Dark", "Ancient order of Force-users devoted to the dark side", -6900),
    ("Knights of Ren", "Dark", "Dark side Force-users led by Kylo Ren", 28),
    ("Inquisitorius", "Dark", "Dark side Force-sensitive agents of the Galactic Empire", 19),
    ("Gray Jedi", "Neutral", "Force-users who walk the line between light and dark", -4000),
]
```

Setiap baris dalam array `force_orders` merepresentasikan satu record dalam tabel `force_orders` dengan format:
1. **Nama** (`name`): Nama organisasi Force, contoh: "Jedi Order"
2. **Sisi** (`side`): Menunjukkan apakah organisasi ini berafiliasi dengan sisi Terang (Light), Gelap (Dark), atau Netral (Neutral) dari Force
3. **Deskripsi** (`description`): Penjelasan singkat tentang organisasi tersebut
4. **Tahun Pendirian** (`founding_year`): Tahun ketika organisasi didirikan dalam timeline Star Wars

Nilai negatif pada `founding_year` menunjukkan tahun sebelum Battle of Yavin (BBY), yang merupakan sistem penanggalan dalam universe Star Wars. Contoh:
- Jedi Order: -25000 berarti didirikan 25.000 tahun sebelum Battle of Yavin
- Knights of Ren: 28 berarti didirikan 28 tahun setelah Battle of Yavin

Kemudian, kita membuat relasi antara karakter dan Force Order:

```python
character_force_orders = [
    (character_ids["Luke Skywalker"], force_order_ids["Jedi Order"], "Jedi Master", 4),
    (character_ids["Darth Vader"], force_order_ids["Sith Order"], "Sith Lord", 13),
    (character_ids["Yoda"], force_order_ids["Jedi Order"], "Grand Master", -800),
    (character_ids["Obi-Wan Kenobi"], force_order_ids["Jedi Order"], "Jedi Master", -25),
]
```

Format data:
1. **ID Karakter**: Referensi ke tabel `characters`
2. **ID Force Order**: Referensi ke tabel `force_orders`
3. **Rank**: Pangkat karakter dalam organisasi tersebut
4. **Joined Year**: Tahun ketika karakter bergabung dengan organisasi

## Cara Kerja API

API ini dibangun menggunakan arsitektur GraphQL, yang memungkinkan client untuk meminta data yang spesifik yang mereka butuhkan. Berikut adalah komponen utama:

1. **Schema GraphQL** (`schema.graphql`): Mendefinisikan tipe data, query, dan mutation yang tersedia.
2. **Resolvers** (`resolvers.py`): Fungsi Python yang mengambil atau memodifikasi data sesuai dengan permintaan GraphQL.
3. **Database** (`database.py`): Menangani koneksi dan operasi database.
4. **Seed Data** (`seed.py`): Mengisi database dengan data awal untuk testing.
5. **Server** (`main.py`): Menjalankan server FastAPI dan mengintegrasikan GraphQL.

## Contoh Query

Berikut adalah contoh query yang dapat Anda gunakan untuk mengakses data dari API:

### 1. Mendapatkan Semua Karakter

```graphql
query {
  allCharacters {
    id
    name
    species
    homePlanet {
      name
      climate
    }
  }
}
```

### 2. Mendapatkan Detail Karakter Beserta Relasi

```graphql
query {
  character(id: "1") {
    id
    name
    species
    homePlanet {
      name
      terrain
    }
    pilotedStarships {
      name
      model
    }
    weapons {
      name
      type
      damage
    }
    vehicles {
      name
      model
      maxSpeed
    }
    forceOrders {
      forceOrder {
        name
        side
      }
      rank
      joinedYear
    }
  }
}
```

### 3. Mendapatkan Semua Planet dan Penduduknya

```graphql
query {
  allPlanets {
    id
    name
    climate
    terrain
    residents {
      name
      species
    }
  }
}
```

### 4. Mendapatkan Detail Planet Tertentu

```graphql
query {
  planet(id: "1") {
    name
    climate
    terrain
    residents {
      name
    }
  }
}
```

### 5. Mendapatkan Semua Kapal dan Pilotnya

```graphql
query {
  allStarships {
    id
    name
    model
    manufacturer
    pilots {
      name
      species
    }
  }
}
```

### 6. Mendapatkan Detail Kapal Tertentu

```graphql
query {
  starship(id: "1") {
    name
    model
    manufacturer
    pilots {
      name
    }
  }
}
```

### 7. Mendapatkan Semua Senjata dan Penggunanya

```graphql
query {
  allWeapons {
    id
    name
    type
    damage
    range
    wielders {
      name
    }
  }
}
```

### 8. Mendapatkan Detail Senjata Tertentu

```graphql
query {
  weapon(id: "1") {
    name
    type
    damage
    range
    wielders {
      name
      species
    }
  }
}
```

### 9. Mendapatkan Semua Kendaraan dan Pengemudinya

```graphql
query {
  allVehicles {
    id
    name
    model
    manufacturer
    maxSpeed
    drivers {
      name
    }
  }
}
```

### 10. Mendapatkan Detail Kendaraan Tertentu

```graphql
query {
  vehicle(id: "1") {
    name
    model
    manufacturer
    maxSpeed
    drivers {
      name
      species
    }
  }
}
```

### 11. Mendapatkan Semua Force Order dan Anggotanya

```graphql
query {
  allForceOrders {
    id
    name
    side
    description
    foundingYear
    members {
      character {
        name
        species
      }
      rank
      joinedYear
    }
  }
}
```

### 12. Mendapatkan Detail Force Order Tertentu

```graphql
query {
  forceOrder(id: "1") {
    name
    side
    description
    foundingYear
    members {
      character {
        name
        species
      }
      rank
      joinedYear
    }
  }
}
```

## Contoh Mutation

Berikut adalah contoh mutation untuk memodifikasi data:

### 1. Membuat Planet Baru

```graphql
mutation {
  createPlanet(input: {
    name: "Mustafar",
    climate: "Hot",
    terrain: "Volcanic"
  }) {
    id
    name
    climate
    terrain
  }
}
```

### 2. Mengupdate Planet

```graphql
mutation {
  updatePlanet(input: {
    id: "1",
    climate: "Arid, Hot",
    terrain: "Desert, Rocky"
  }) {
    id
    name
    climate
    terrain
  }
}
```

### 3. Menghapus Planet

```graphql
mutation {
  deletePlanet(id: "6")
}
```

### 4. Membuat Karakter Baru

```graphql
mutation {
  createCharacter(input: {
    name: "Ahsoka Tano",
    species: "Togruta",
    homePlanetId: 4
  }) {
    id
    name
    species
    homePlanet {
      name
    }
  }
}
```

### 5. Mengupdate Karakter

```graphql
mutation {
  updateCharacter(input: {
    id: "1",
    species: "Human Jedi"
  }) {
    id
    name
    species
  }
}
```

### 6. Menghapus Karakter

```graphql
mutation {
  deleteCharacter(id: "8")
}
```

### 7. Membuat Kapal Baru

```graphql
mutation {
  createStarship(input: {
    name: "Slave I",
    model: "Firespray-31-class patrol and attack craft",
    manufacturer: "Kuat Systems Engineering"
  }) {
    id
    name
    model
    manufacturer
  }
}
```

### 8. Mengupdate Kapal

```graphql
mutation {
  updateStarship(input: {
    id: "1",
    model: "Modified YT-1300 light freighter"
  }) {
    id
    name
    model
  }
}
```

### 9. Menghapus Kapal

```graphql
mutation {
  deleteStarship(id: "6")
}
```

### 10. Menambahkan Karakter sebagai Pilot Kapal

```graphql
mutation {
  assignStarship(input: {
    characterId: "3",
    starshipId: "1"
  }) {
    id
    name
    pilotedStarships {
      name
    }
  }
}
```

### 11. Membuat Senjata Baru

```graphql
mutation {
  createWeapon(input: {
    name: "Darksaber",
    type: "Lightsaber",
    damage: 120,
    range: "Close"
  }) {
    id
    name
    type
    damage
  }
}
```

### 12. Mengupdate Senjata

```graphql
mutation {
  updateWeapon(input: {
    id: "1",
    damage: 150
  }) {
    id
    name
    damage
  }
}
```

### 13. Menghapus Senjata

```graphql
mutation {
  deleteWeapon(id: "6")
}
```

### 14. Menambahkan Senjata ke Karakter

```graphql
mutation {
  assignWeapon(input: {
    characterId: "7",
    weaponId: "1"
  }) {
    id
    name
    weapons {
      name
      type
    }
  }
}
```

### 15. Membuat Kendaraan Baru

```graphql
mutation {
  createVehicle(input: {
    name: "Sandcrawler",
    model: "Digger Crawler",
    manufacturer: "Corellia Mining Corporation",
    maxSpeed: 30
  }) {
    id
    name
    model
    maxSpeed
  }
}
```

### 16. Mengupdate Kendaraan

```graphql
mutation {
  updateVehicle(input: {
    id: "1",
    maxSpeed: 550
  }) {
    id
    name
    maxSpeed
  }
}
```

### 17. Menghapus Kendaraan

```graphql
mutation {
  deleteVehicle(id: "6")
}
```

### 18. Menambahkan Kendaraan ke Karakter

```graphql
mutation {
  assignVehicle(input: {
    characterId: "2",
    vehicleId: "3"
  }) {
    id
    name
    vehicles {
      name
      model
    }
  }
}
```

### 19. Membuat Force Order Baru

```graphql
mutation {
  createForceOrder(input: {
    name: "Nightsisters",
    side: "Dark",
    description: "Force-wielding witches from Dathomir",
    foundingYear: -5000
  }) {
    id
    name
    side
    description
  }
}
```

### 20. Mengupdate Force Order

```graphql
mutation {
  updateForceOrder(input: {
    id: "3",
    description: "Dark side Force-users led by Supreme Leader Kylo Ren"
  }) {
    id
    name
    description
  }
}
```

### 21. Menghapus Force Order

```graphql
mutation {
  deleteForceOrder(id: "6")
}
```

### 22. Menambahkan Karakter ke Force Order dengan Rank

```graphql
mutation {
  assignForceOrder(input: {
    characterId: "7",
    forceOrderId: "1",
    rank: "Jedi Knight",
    joinedYear: -20
  }) {
    id
    name
    forceOrders {
      forceOrder {
        name
      }
      rank
      joinedYear
    }
  }
}
```

## Menjalankan API

1. Pastikan Python 3.8+ terinstal
2. Buat dan aktifkan virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Instal dependensi:
   ```
   pip install fastapi uvicorn ariadne
   ```
4. Inisialisasi database:
   ```
   python database.py
   python seed.py
   ```
5. Jalankan server:
   ```
   uvicorn main:app --reload
   ```
6. Buka GraphQL Playground di browser:
   ```
   http://localhost:8000/graphql
   ```

Selamat mengeksplorasi Star Wars GraphQL API!
