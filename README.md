# Star Wars GraphQL API

Selamat datang di Star Wars GraphQL API! Aplikasi ini adalah API GraphQL yang memungkinkan Anda untuk mengakses dan memanipulasi data dari universe Star Wars, termasuk karakter, planet, kapal luar angkasa, senjata, kendaraan, dan organisasi Pengguna Force (Force Orders).

## Daftar Isi

- [Pengenalan GraphQL](#pengenalan-graphql)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Struktur Proyek](#struktur-proyek)
- [Struktur Database](#struktur-database)
- [Relasi Antar Tabel](#relasi-antar-tabel)
- [Cara Kerja API](#cara-kerja-api)
- [Contoh Query Terintegrasi](#contoh-query-terintegrasi)
- [Contoh Mutation](#contoh-mutation)
- [Menjalankan API](#menjalankan-api)

## Pengenalan GraphQL

GraphQL adalah bahasa query untuk API dan runtime untuk mengeksekusi query tersebut dengan data yang ada. GraphQL memberikan deskripsi lengkap dan mudah dipahami tentang data dalam API Anda, memberikan klien kekuatan untuk meminta persis apa yang mereka butuhkan dan tidak lebih, memudahkan evolusi API dari waktu ke waktu, dan memungkinkan alat pengembangan yang kuat.

### Perbedaan dengan REST API

1. **Single Endpoint**: GraphQL hanya menggunakan satu endpoint, biasanya `/graphql`, tidak seperti REST yang memiliki banyak endpoint.

2. **Client-Specified Queries**: Client menentukan struktur data yang diinginkan, tidak seperti REST di mana server menentukan struktur respons.

3. **No Over-fetching or Under-fetching**: Client hanya mendapatkan data yang diminta, tidak lebih dan tidak kurang.

4. **Strongly Typed**: GraphQL memiliki sistem tipe yang kuat, memungkinkan validasi query pada waktu kompilasi.

### Komponen Utama GraphQL

1. **Schema**: Mendefinisikan tipe data dan operasi yang tersedia di API.

2. **Query**: Operasi untuk membaca data (mirip dengan GET di REST).

3. **Mutation**: Operasi untuk memodifikasi data (mirip dengan POST, PUT, DELETE di REST).

4. **Resolver**: Fungsi yang menentukan bagaimana data untuk field tertentu diambil atau dimodifikasi.

## Teknologi yang Digunakan

- **Python 3.8+**: Bahasa pemrograman utama yang digunakan untuk mengembangkan backend API.
- **FastAPI**: Web framework modern dan cepat untuk Python yang digunakan untuk membuat API. FastAPI mendukung asynchronous programming dan memiliki performa tinggi.
- **Ariadne**: Library GraphQL untuk Python yang menggunakan pendekatan schema-first. Ariadne memudahkan integrasi GraphQL dengan Python dan FastAPI.
- **SQLite**: Database ringan berbasis file yang digunakan untuk menyimpan data. SQLite ideal untuk aplikasi kecil hingga menengah dan tidak memerlukan server database terpisah.
- **Uvicorn**: Server ASGI (Asynchronous Server Gateway Interface) untuk menjalankan aplikasi FastAPI dengan performa tinggi.

## Struktur Proyek

Proyek ini terdiri dari beberapa file utama:

- **main.py**: File utama yang menjalankan server FastAPI dan mengintegrasikan GraphQL.
- **database.py**: Menangani koneksi database dan mendefinisikan struktur tabel.
- **schema.graphql**: Mendefinisikan tipe data, query, dan mutation yang tersedia di API GraphQL.
- **resolvers.py**: Berisi fungsi resolver yang mengambil atau memodifikasi data sesuai dengan permintaan GraphQL.
- **seed.py**: Mengisi database dengan data awal untuk testing.
- **starwars.db**: File database SQLite yang menyimpan semua data.

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

API ini dibangun menggunakan arsitektur GraphQL, yang memungkinkan client untuk meminta data yang spesifik yang mereka butuhkan. Berikut adalah alur kerja API:

### 1. Definisi Schema (schema.graphql)

Schema GraphQL mendefinisikan struktur data dan operasi yang tersedia. Ini mencakup:
- **Types**: Mendefinisikan struktur objek data (Character, Planet, Starship, dll)
- **Queries**: Mendefinisikan operasi untuk membaca data
- **Mutations**: Mendefinisikan operasi untuk memodifikasi data

Contoh definisi type di schema:
```graphql
type Character {
  id: ID!
  name: String!
  species: String
  homePlanet: Planet
  pilotedStarships: [Starship!]!
  weapons: [Weapon!]!
  vehicles: [Vehicle!]!
  forceOrders: [CharacterForceOrder!]!
}
```

### 2. Implementasi Resolver (resolvers.py)

Resolver adalah fungsi yang menentukan bagaimana data diambil atau dimodifikasi. Setiap field dalam schema memiliki resolver terkait.

Contoh resolver untuk query:
```python
@query.field("character")
def resolve_character(_, info, id):
    conn = get_db_connection()
    try:
        character = conn.execute("SELECT id, name, species, home_planet_id FROM characters WHERE id = ?", (id,)).fetchone()
        return dict(character) if character else None
    finally:
        conn.close()
```

### 3. Alur Eksekusi Query

Ketika client mengirim query GraphQL:
1. Server menerima query dan memvalidasinya terhadap schema
2. Jika valid, server memanggil resolver yang sesuai untuk setiap field yang diminta
3. Resolver mengambil data dari database
4. Server menggabungkan hasil dan mengembalikannya ke client dalam format yang diminta

### 4. Alur Eksekusi Mutation

Untuk mutation, prosesnya serupa:
1. Server menerima mutation dan memvalidasinya
2. Resolver mutation dipanggil dengan input yang diberikan
3. Resolver melakukan perubahan pada database
4. Server mengembalikan hasil sesuai dengan yang diminta dalam mutation

### 5. Integrasi dengan FastAPI (main.py)

FastAPI digunakan sebagai web framework yang mengekspos endpoint GraphQL:
```python
from fastapi import FastAPI
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL

app = FastAPI()
type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(type_defs, resolvers)
graphql_app = GraphQL(schema, debug=True)

app.mount("/graphql", graphql_app)
```

## Contoh Query Terintegrasi

Berikut adalah contoh query terintegrasi yang dapat Anda gunakan untuk mengakses data dari semua tabel dalam satu permintaan. Ini menunjukkan kekuatan GraphQL dalam mengambil data yang saling berhubungan dalam satu query.

### Query Lengkap untuk Eksplorasi Star Wars Universe

```graphql
query StarWarsExplorer {
  # Mendapatkan semua karakter dengan detail lengkap
  allCharacters {
    id
    name
    species
    homePlanet {
      id
      name
      climate
      terrain
    }
    pilotedStarships {
      id
      name
      model
      manufacturer
    }
    weapons {
      id
      name
      type
      damage
      range
    }
    vehicles {
      id
      name
      model
      manufacturer
      maxSpeed
    }
    forceOrders {
      rank
      joinedYear
      forceOrder {
        id
        name
        side
        description
        foundingYear
      }
    }
  }
  
  # Mendapatkan semua planet dan penduduknya
  allPlanets {
    id
    name
    climate
    terrain
    residents {
      id
      name
      species
    }
  }
  
  # Mendapatkan semua kapal dan pilotnya
  allStarships {
    id
    name
    model
    manufacturer
    pilots {
      id
      name
      species
    }
  }
  
  # Mendapatkan semua senjata dan penggunanya
  allWeapons {
    id
    name
    type
    damage
    range
    wielders {
      id
      name
      species
    }
  }
  
  # Mendapatkan semua kendaraan dan pengemudinya
  allVehicles {
    id
    name
    model
    manufacturer
    maxSpeed
    drivers {
      id
      name
      species
    }
  }
  
  # Mendapatkan semua Force Order dan anggotanya
  allForceOrders {
    id
    name
    side
    description
    foundingYear
    members {
      rank
      joinedYear
      character {
        id
        name
        species
      }
    }
  }
}
```

### Query Fokus pada Karakter Tertentu

Jika Anda ingin fokus pada satu karakter dan semua data terkaitnya:

```graphql
query CharacterDetail($characterId: ID!) {
  character(id: $characterId) {
    id
    name
    species
    homePlanet {
      id
      name
      climate
      terrain
      residents {
        id
        name
        species
      }
    }
    pilotedStarships {
      id
      name
      model
      manufacturer
      pilots {
        id
        name
      }
    }
    weapons {
      id
      name
      type
      damage
      range
      wielders {
        id
        name
      }
    }
    vehicles {
      id
      name
      model
      maxSpeed
      drivers {
        id
        name
      }
    }
    forceOrders {
      rank
      joinedYear
      forceOrder {
        id
        name
        side
        description
        foundingYear
        members {
          rank
          character {
            id
            name
          }
        }
      }
    }
  }
}
```

Variables untuk query ini:
```json
{
  "characterId": "1"
}
```

### Query Fokus pada Force Order

Untuk menjelajahi Force Order tertentu dan semua anggotanya dengan detail lengkap:

```graphql
query ForceOrderDetail($forceOrderId: ID!) {
  forceOrder(id: $forceOrderId) {
    id
    name
    side
    description
    foundingYear
    members {
      rank
      joinedYear
      character {
        id
        name
        species
        homePlanet {
          name
          climate
        }
        weapons {
          name
          type
        }
        pilotedStarships {
          name
          model
        }
        vehicles {
          name
          maxSpeed
        }
      }
    }
  }
}
```

Variables untuk query ini:
```json
{
  "forceOrderId": "1"
}
```

## Contoh Mutation

Berikut adalah contoh mutation untuk memodifikasi data. Termasuk contoh mutation terintegrasi yang menunjukkan bagaimana melakukan beberapa operasi sekaligus.

### Mutation Terintegrasi

#### 1. Membuat Karakter Lengkap dengan Relasi

Mutation ini membuat karakter baru, kemudian menambahkan senjata, kapal, kendaraan, dan keanggotaan Force Order dalam satu operasi:

```graphql
mutation CreateCompleteCharacter {
  # Langkah 1: Buat karakter baru
  newCharacter: createCharacter(input: {
    name: "Ahsoka Tano",
    species: "Togruta",
    homePlanetId: 4
  }) {
    id
    name
    species
  }
  
  # Langkah 2: Buat senjata baru untuk karakter
  newWeapon: createWeapon(input: {
    name: "Dual Lightsabers",
    type: "Lightsaber",
    damage: 110,
    range: "Close"
  }) {
    id
    name
  }
  
  # Langkah 3: Buat kendaraan baru untuk karakter
  newVehicle: createVehicle(input: {
    name: "Jedi Starfighter",
    model: "Delta-7B Aethersprite",
    manufacturer: "Kuat Systems Engineering",
    maxSpeed: 1150
  }) {
    id
    name
  }
}
```

Setelah mutation pertama berhasil, gunakan ID yang dihasilkan untuk membuat relasi:

```graphql
mutation AssignRelationsToCharacter($characterId: ID!, $weaponId: ID!, $vehicleId: ID!) {
  # Langkah 4: Hubungkan karakter dengan senjata
  assignWeapon: assignWeapon(input: {
    characterId: $characterId,
    weaponId: $weaponId
  }) {
    id
    name
  }
  
  # Langkah 5: Hubungkan karakter dengan kendaraan
  assignVehicle: assignVehicle(input: {
    characterId: $characterId,
    vehicleId: $vehicleId
  }) {
    id
    name
  }
  
  # Langkah 6: Hubungkan karakter dengan Force Order
  assignForceOrder: assignForceOrder(input: {
    characterId: $characterId,
    forceOrderId: "1", # ID Jedi Order
    rank: "Jedi Padawan",
    joinedYear: -22
  }) {
    id
    name
  }
}
```

Variables untuk mutation kedua:
```json
{
  "characterId": "8", # ID dari karakter yang baru dibuat
  "weaponId": "6", # ID dari senjata yang baru dibuat
  "vehicleId": "6" # ID dari kendaraan yang baru dibuat
}
```

#### 2. Membuat Ekspedisi Star Wars

Mutation ini membuat planet baru, kapal baru, dan karakter baru yang berasal dari planet tersebut dan mengemudikan kapal tersebut:

```graphql
mutation CreateStarWarsExpedition {
  # Langkah 1: Buat planet baru
  newPlanet: createPlanet(input: {
    name: "Ilum",
    climate: "Frigid",
    terrain: "Ice caves, Tundra"
  }) {
    id
    name
  }
  
  # Langkah 2: Buat kapal baru
  newStarship: createStarship(input: {
    name: "The Mantis",
    model: "S-161 XL luxury yacht",
    manufacturer: "Latero Spaceworks"
  }) {
    id
    name
  }
  
  # Langkah 3: Buat Force Order baru
  newForceOrder: createForceOrder(input: {
    name: "Jedi Fallen Order",
    side: "Light",
    description: "Jedi survivors after Order 66",
    foundingYear: 14
  }) {
    id
    name
  }
}
```

Kemudian, buat karakter dan hubungkan semua entitas:

```graphql
mutation CreateExpeditionMembers($planetId: ID!, $starshipId: ID!, $forceOrderId: ID!) {
  # Buat karakter pertama
  character1: createCharacter(input: {
    name: "Cal Kestis",
    species: "Human",
    homePlanetId: $planetId
  }) {
    id
    name
  }
  
  # Buat karakter kedua
  character2: createCharacter(input: {
    name: "Cere Junda",
    species: "Human",
    homePlanetId: $planetId
  }) {
    id
    name
  }
}
```

Terakhir, hubungkan karakter dengan kapal dan Force Order:

```graphql
mutation ConnectExpeditionMembers(
  $char1Id: ID!, 
  $char2Id: ID!, 
  $starshipId: ID!, 
  $forceOrderId: ID!
) {
  # Hubungkan karakter 1 dengan kapal
  assign1: assignStarship(input: {
    characterId: $char1Id,
    starshipId: $starshipId
  }) {
    id
  }
  
  # Hubungkan karakter 2 dengan kapal
  assign2: assignStarship(input: {
    characterId: $char2Id,
    starshipId: $starshipId
  }) {
    id
  }
  
  # Hubungkan karakter 1 dengan Force Order
  force1: assignForceOrder(input: {
    characterId: $char1Id,
    forceOrderId: $forceOrderId,
    rank: "Jedi Padawan",
    joinedYear: 14
  }) {
    id
  }
  
  # Hubungkan karakter 2 dengan Force Order
  force2: assignForceOrder(input: {
    characterId: $char2Id,
    forceOrderId: $forceOrderId,
    rank: "Jedi Knight",
    joinedYear: 14
  }) {
    id
  }
}
```

#### 3. Update Komprehensif Karakter

Mutation ini mengupdate karakter beserta semua relasinya sekaligus:

```graphql
mutation UpdateCharacterComprehensive($characterId: ID!) {
  # Update data karakter
  updateChar: updateCharacter(input: {
    id: $characterId,
    species: "Human Force-sensitive",
    homePlanetId: 1
  }) {
    id
    name
    species
  }
  
  # Tambahkan senjata baru
  newWeapon: createWeapon(input: {
    name: "Crossguard Lightsaber",
    type: "Lightsaber",
    damage: 130,
    range: "Close"
  }) {
    id
  }
  
  # Tambahkan kendaraan baru
  newVehicle: createVehicle(input: {
    name: "TIE Silencer",
    model: "TIE/vn space superiority fighter",
    manufacturer: "Sienar-Jaemus Fleet Systems",
    maxSpeed: 1200
  }) {
    id
  }
}
```

Kemudian, hubungkan entitas baru dan perbarui keanggotaan Force Order:

```graphql
mutation UpdateCharacterRelations(
  $characterId: ID!, 
  $weaponId: ID!, 
  $vehicleId: ID!
) {
  # Hubungkan dengan senjata baru
  assignWeapon: assignWeapon(input: {
    characterId: $characterId,
    weaponId: $weaponId
  }) {
    id
  }
  
  # Hubungkan dengan kendaraan baru
  assignVehicle: assignVehicle(input: {
    characterId: $characterId,
    vehicleId: $vehicleId
  }) {
    id
  }
  
  # Perbarui keanggotaan Force Order
  updateForceOrder: assignForceOrder(input: {
    characterId: $characterId,
    forceOrderId: "3", # Knights of Ren
    rank: "Supreme Leader",
    joinedYear: 34
  }) {
    id
    name
    forceOrders {
      forceOrder {
        name
      }
      rank
    }
  }
}
```

### Contoh Mutation Individual

#### Planet Mutations

##### Membuat Planet Baru

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

##### Mengupdate Planet

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

##### Menghapus Planet

```graphql
mutation {
  deletePlanet(id: "6")
}
```

#### Character Mutations

##### Membuat Karakter Baru

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

##### Mengupdate Karakter

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

##### Menghapus Karakter

```graphql
mutation {
  deleteCharacter(id: "8")
}
```

#### Starship Mutations

##### Membuat Kapal Baru

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

##### Mengupdate Kapal

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

##### Menghapus Kapal

```graphql
mutation {
  deleteStarship(id: "6")
}
```

##### Menambahkan Karakter sebagai Pilot Kapal

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

#### Weapon Mutations

##### Membuat Senjata Baru

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

##### Mengupdate Senjata

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

##### Menghapus Senjata

```graphql
mutation {
  deleteWeapon(id: "6")
}
```

##### Menambahkan Senjata ke Karakter

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

#### Vehicle Mutations

##### Membuat Kendaraan Baru

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

##### Mengupdate Kendaraan

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

##### Menghapus Kendaraan

```graphql
mutation {
  deleteVehicle(id: "6")
}
```

##### Menambahkan Kendaraan ke Karakter

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

#### Force Order Mutations

##### Membuat Force Order Baru

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

##### Mengupdate Force Order

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

##### Menghapus Force Order

```graphql
mutation {
  deleteForceOrder(id: "6")
}
```

##### Menambahkan Karakter ke Force Order dengan Rank

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
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Instal dependensi:
   ```bash
   pip install fastapi uvicorn ariadne
   ```
4. Inisialisasi database:
   ```bash
   python database.py
   python seed.py
   ```
5. Jalankan server:
   ```bash
   uvicorn main:app --reload
   ```
6. Buka GraphQL Playground di browser:
   ```
   http://localhost:8000/graphql
   ```

### Menggunakan GraphQL Playground

GraphQL Playground adalah IDE interaktif untuk menguji query dan mutation GraphQL. Berikut cara menggunakannya:

1. **Menulis Query**: Tulis query di panel kiri
2. **Menjalankan Query**: Klik tombol play di tengah
3. **Melihat Hasil**: Hasil akan ditampilkan di panel kanan
4. **Menggunakan Variables**: Untuk query yang membutuhkan variabel, gunakan tab "Variables" di bawah panel query
5. **Menjelajahi Schema**: Gunakan tab "Schema" di sisi kanan untuk melihat dokumentasi API

Contoh penggunaan dengan variabel:

1. Di panel query, tulis:
   ```graphql
   query CharacterDetail($id: ID!) {
     character(id: $id) {
       name
       species
     }
   }
   ```

2. Di panel variabel, tulis:
   ```json
   {
     "id": "1"
   }
   ```

3. Klik tombol play untuk menjalankan query

Selamat mengeksplorasi Star Wars GraphQL API!
