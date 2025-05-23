# Star Wars GraphQL API - Contoh Mutation dan Query

Dokumen ini berisi contoh mutation dan query untuk menguji API GraphQL Star Wars, dengan fokus pada operasi update/delete untuk karakter dan kapal, serta operasi pada tabel Force Order.

## 1. Mutation untuk Karakter

### 1.1 Membuat Karakter Baru

```graphql
mutation CreateCharacter {
  createCharacter(input: {
    name: "Ahsoka Tano",
    species: "Togruta",
    homePlanetId: 4  # ID planet Naboo
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

### 1.2 Mengupdate Karakter

```graphql
mutation UpdateCharacter {
  updateCharacter(input: {
    id: "1",  # ID Luke Skywalker
    species: "Human Jedi",
    homePlanetId: 1  # ID planet Tatooine
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

### 1.3 Menghapus Karakter

```graphql
mutation DeleteCharacter {
  deleteCharacter(id: "15")  # ID karakter yang ingin dihapus
}
```

## 2. Mutation untuk Kapal (Starship)

### 2.1 Membuat Kapal Baru

```graphql
mutation CreateStarship {
  createStarship(input: {
    name: "Razor Crest",
    model: "ST-70 Assault Ship",
    manufacturer: "Nevarro Shipyards"
  }) {
    id
    name
    model
    manufacturer
  }
}
```

### 2.2 Mengupdate Kapal

```graphql
mutation UpdateStarship {
  updateStarship(input: {
    id: "2",  # ID X-wing
    model: "T-70 X-wing starfighter",
    manufacturer: "Incom-FreiTek Corporation"
  }) {
    id
    name
    model
    manufacturer
  }
}
```

### 2.3 Menghapus Kapal

```graphql
mutation DeleteStarship {
  deleteStarship(id: "10")  # ID kapal yang ingin dihapus
}
```

### 2.4 Menghubungkan Karakter dengan Kapal

```graphql
mutation AssignStarship {
  assignStarship(input: {
    characterId: "9",  # ID Rey
    starshipId: "2"    # ID X-wing
  }) {
    id
    name
    pilotedStarships {
      id
      name
      model
    }
  }
}
```

## 3. Mutation untuk Force Order

### 3.1 Membuat Force Order Baru

```graphql
mutation CreateForceOrder {
  createForceOrder(input: {
    name: "Jedi Fallen Order",
    side: "Light",
    description: "Survivors of Order 66 led by Cal Kestis",
    foundingYear: 14
  }) {
    id
    name
    side
    description
    foundingYear
  }
}
```

### 3.2 Mengupdate Force Order

```graphql
mutation UpdateForceOrder {
  updateForceOrder(input: {
    id: "3",  # ID Knights of Ren
    description: "Dark side Force-users loyal to Supreme Leader Snoke and later Kylo Ren",
    side: "Dark"
  }) {
    id
    name
    side
    description
    foundingYear
  }
}
```

### 3.3 Menghapus Force Order

```graphql
mutation DeleteForceOrder {
  deleteForceOrder(id: "10")  # ID Force Order yang ingin dihapus
}
```

### 3.4 Menghubungkan Karakter dengan Force Order

```graphql
mutation AssignForceOrder {
  assignForceOrder(input: {
    characterId: "12",  # ID Poe Dameron
    forceOrderId: "6",  # ID Jedi Praxeum
    rank: "Initiate",
    joinedYear: 34
  }) {
    id
    name
    forceOrders {
      rank
      joinedYear
      forceOrder {
        name
        side
      }
    }
  }
}
```

### 3.5 Menghapus Hubungan Karakter dengan Force Order

```graphql
mutation RemoveForceOrder {
  removeForceOrder(input: {
    characterId: "6",  # ID Darth Vader
    forceOrderId: "1"  # ID Jedi Order
  }) {
    id
    name
    forceOrders {
      forceOrder {
        name
      }
    }
  }
}
```

## 4. Mutation untuk Senjata (Weapon)

### 4.1 Membuat Senjata Baru

```graphql
mutation CreateWeapon {
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
    range
  }
}
```

### 4.2 Mengupdate Senjata

```graphql
mutation UpdateWeapon {
  updateWeapon(input: {
    id: "1",  # ID Lightsaber
    damage: 130,
    range: "Medium"
  }) {
    id
    name
    type
    damage
    range
  }
}
```

### 4.3 Menghapus Senjata

```graphql
mutation DeleteWeapon {
  deleteWeapon(id: "8")  # ID senjata yang ingin dihapus
}
```

### 4.4 Menghubungkan Karakter dengan Senjata

```graphql
mutation AssignWeapon {
  assignWeapon(input: {
    characterId: "11",  # ID Finn
    weaponId: "1"       # ID Lightsaber
  }) {
    id
    name
    weapons {
      id
      name
      type
      damage
    }
  }
}
```

### 4.5 Menghapus Hubungan Karakter dengan Senjata

```graphql
mutation RemoveWeapon {
  removeWeapon(input: {
    characterId: "11",  # ID Finn
    weaponId: "1"       # ID Lightsaber
  }) {
    id
    name
    weapons {
      name
    }
  }
}
```

## 5. Mutation untuk Kendaraan (Vehicle)

### 5.1 Membuat Kendaraan Baru

```graphql
mutation CreateVehicle {
  createVehicle(input: {
    name: "Sandcrawler",
    model: "Digger Crawler",
    manufacturer: "Corellia Mining Corporation",
    maxSpeed: 30
  }) {
    id
    name
    model
    manufacturer
    maxSpeed
  }
}
```

### 5.2 Mengupdate Kendaraan

```graphql
mutation UpdateVehicle {
  updateVehicle(input: {
    id: "3",  # ID Snowspeeder
    model: "T-48 airspeeder",
    maxSpeed: 700
  }) {
    id
    name
    model
    manufacturer
    maxSpeed
  }
}
```

### 5.3 Menghapus Kendaraan

```graphql
mutation DeleteVehicle {
  deleteVehicle(id: "7")  # ID kendaraan yang ingin dihapus
}
```

### 5.4 Menghubungkan Karakter dengan Kendaraan

```graphql
mutation AssignVehicle {
  assignVehicle(input: {
    characterId: "10",  # ID Kylo Ren
    vehicleId: "6"      # ID AT-ST
  }) {
    id
    name
    vehicles {
      id
      name
      model
      maxSpeed
    }
  }
}
```

### 5.5 Menghapus Hubungan Karakter dengan Kendaraan

```graphql
mutation RemoveVehicle {
  removeVehicle(input: {
    characterId: "10",  # ID Kylo Ren
    vehicleId: "6"      # ID AT-ST
  }) {
    id
    name
    vehicles {
      name
    }
  }
}
```

## 6. Query untuk Melihat Hasil Mutation

### 6.1 Query untuk Mendapatkan Semua Senjata dan Penggunanya

```graphql
query GetAllWeapons {
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
}
```

### 6.2 Query untuk Mendapatkan Detail Senjata Tertentu

```graphql
query GetWeaponDetails {
  weapon(id: "1") {  # ID Lightsaber
    id
    name
    type
    damage
    range
    wielders {
      id
      name
      species
      homePlanet {
        name
      }
    }
  }
}
```

### 6.3 Query untuk Mendapatkan Semua Kendaraan dan Pengemudinya

```graphql
query GetAllVehicles {
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
}
```

### 6.4 Query untuk Mendapatkan Detail Kendaraan Tertentu

```graphql
query GetVehicleDetails {
  vehicle(id: "2") {  # ID AT-AT
    id
    name
    model
    manufacturer
    maxSpeed
    drivers {
      id
      name
      species
      homePlanet {
        name
      }
    }
  }
}
```

### 6.5 Query Karakter dengan Force Orders

```graphql
query GetCharacterWithForceOrders {
  character(id: "1") {  # ID Luke Skywalker
    id
    name
    species
    forceOrders {
      rank
      joinedYear
      forceOrder {
        id
        name
        side
        description
      }
    }
  }
}
```

### 6.6 Query Semua Force Orders dengan Anggota

```graphql
query GetAllForceOrders {
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

### 6.7 Query Karakter dengan Semua Relasi

```graphql
query GetCharacterWithAllRelations {
  character(id: "6") {  # ID Darth Vader
    id
    name
    species
    homePlanet {
      name
    }
    pilotedStarships {
      name
      model
    }
    weapons {
      name
      type
    }
    vehicles {
      name
      model
    }
    forceOrders {
      rank
      joinedYear
      forceOrder {
        name
        side
      }
    }
  }
}
```

## 7. Contoh Penggunaan dengan Variabel di Postman

Untuk menggunakan variabel di Postman:

1. Pilih metode POST
2. Masukkan URL: `http://localhost:8000/graphql`
3. Di tab "Body", pilih "GraphQL"
4. Di kolom "QUERY", masukkan query atau mutation
5. Di kolom "GRAPHQL VARIABLES", masukkan variabel dalam format JSON

### 7.1 Contoh Update Karakter dengan Variabel

Query:
```graphql
mutation UpdateCharacter($input: CharacterInput!) {
  updateCharacter(input: $input) {
    id
    name
    species
  }
}
```

Variables:
```json
{
  "input": {
    "id": "9",
    "name": "Rey Skywalker",
    "species": "Human Force-sensitive"
  }
}
```

### 7.2 Contoh Assign Force Order dengan Variabel

Query:
```graphql
mutation AssignForceOrder($input: CharacterForceOrderInput!) {
  assignForceOrder(input: $input) {
    id
    name
    forceOrders {
      rank
      forceOrder {
        name
      }
    }
  }
}
```

Variables:
```json
{
  "input": {
    "characterId": "10",
    "forceOrderId": "3",
    "rank": "Master of the Knights of Ren",
    "joinedYear": 28
  }
}
```

## 8. Contoh Mutation Terintegrasi

Berikut adalah contoh mutation terintegrasi yang menunjukkan alur lengkap untuk membuat dan mengupdate entitas:

```graphql
# Langkah 1: Buat Force Order baru
mutation CreateNewForceOrder {
  newForceOrder: createForceOrder(input: {
    name: "Jedi Fallen Order",
    side: "Light",
    description: "Survivors of Order 66",
    foundingYear: 14
  }) {
    id
    name
  }
}

# Langkah 2: Buat karakter baru
mutation CreateNewCharacter {
  newCharacter: createCharacter(input: {
    name: "Cal Kestis",
    species: "Human",
    homePlanetId: 5  # ID Coruscant
  }) {
    id
    name
  }
}

# Langkah 3: Hubungkan karakter dengan Force Order
# Gunakan ID yang didapat dari langkah 1 dan 2
mutation AssignForceOrderToCharacter {
  assignForceOrder(input: {
    characterId: "16",  # ID Cal Kestis (hasil dari langkah 2)
    forceOrderId: "11", # ID Jedi Fallen Order (hasil dari langkah 1)
    rank: "Jedi Knight",
    joinedYear: 14
  }) {
    id
    name
    forceOrders {
      rank
      joinedYear
      forceOrder {
        name
        side
      }
    }
  }
}

# Langkah 4: Update karakter
mutation UpdateNewCharacter {
  updateCharacter(input: {
    id: "16",  # ID Cal Kestis
    species: "Human Force-sensitive"
  }) {
    id
    name
    species
    forceOrders {
      rank
      forceOrder {
        name
      }
    }
  }
}
