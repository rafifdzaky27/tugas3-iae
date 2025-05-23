# Star Wars GraphQL API - Contoh Query dan Mutation

Dokumen ini berisi contoh query dan mutation untuk menguji API GraphQL Star Wars. Contoh-contoh ini mencakup semua tabel dan operasi yang tersedia dalam API.

## Query Examples

### 1. Query untuk Mendapatkan Semua Data Karakter dengan Relasi

Query ini menunjukkan kemampuan GraphQL untuk mengambil data karakter beserta semua relasinya dalam satu request.

```graphql
query GetCharacterWithRelations {
  character(id: "1") {
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
    }
    vehicles {
      id
      name
      model
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
      }
    }
  }
}
```

### 2. Query untuk Mendapatkan Semua Planet dan Penduduknya

Query ini menunjukkan relasi one-to-many antara planet dan karakter.

```graphql
query GetPlanetsWithResidents {
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
}
```

### 3. Query untuk Mendapatkan Semua Force Order dan Anggotanya

Query ini menunjukkan relasi many-to-many dengan data tambahan (rank dan joinedYear).

```graphql
query GetForceOrdersWithMembers {
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

### 4. Query untuk Mendapatkan Semua Senjata dan Penggunanya

Query ini menunjukkan relasi many-to-many antara senjata dan karakter.

```graphql
query GetWeaponsWithWielders {
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

### 5. Query untuk Mendapatkan Semua Kapal dan Pilotnya

Query ini menunjukkan relasi many-to-many antara kapal dan karakter.

```graphql
query GetStarshipsWithPilots {
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
}
```

### 6. Query untuk Mendapatkan Semua Kendaraan dan Pengemudinya

Query ini menunjukkan relasi many-to-many antara kendaraan dan karakter.

```graphql
query GetVehiclesWithDrivers {
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

## Mutation Examples

### 1. Membuat Planet Baru

Mutation ini menunjukkan cara membuat entitas baru.

```graphql
mutation CreateNewPlanet {
  createPlanet(input: {
    name: "Exegol",
    climate: "Dry, Stormy",
    terrain: "Desert, Rocky"
  }) {
    id
    name
    climate
    terrain
  }
}
```

### 2. Membuat Karakter Baru dan Menghubungkannya dengan Planet

Mutation ini menunjukkan cara membuat karakter dan mengaitkannya dengan planet yang sudah ada.

```graphql
mutation CreateCharacterWithPlanet {
  createCharacter(input: {
    name: "Rey Skywalker",
    species: "Human",
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

### 3. Membuat Force Order Baru

Mutation ini menunjukkan cara membuat Force Order baru.

```graphql
mutation CreateNewForceOrder {
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
    foundingYear
  }
}
```

### 4. Menghubungkan Karakter dengan Force Order

Mutation ini menunjukkan cara menghubungkan karakter dengan Force Order, termasuk data tambahan.

```graphql
mutation AssignCharacterToForceOrder {
  assignForceOrder(input: {
    characterId: "1",  # ID Luke Skywalker
    forceOrderId: "1", # ID Jedi Order
    rank: "Jedi Master",
    joinedYear: 4
  }) {
    id
    name
    forceOrders {
      rank
      joinedYear
      forceOrder {
        name
      }
    }
  }
}
```

### 5. Membuat Senjata Baru dan Menghubungkannya dengan Karakter

Mutation ini menunjukkan cara membuat senjata baru dan mengaitkannya dengan karakter.

```graphql
mutation CreateAndAssignWeapon {
  # Membuat senjata baru
  newWeapon: createWeapon(input: {
    name: "Darksaber",
    type: "Lightsaber",
    damage: 120,
    range: "Close"
  }) {
    id
    name
  }
  
  # Mengaitkan senjata dengan karakter
  # Catatan: Dalam penggunaan nyata, gunakan ID dari hasil mutation pertama
  assignWeapon: assignWeapon(input: {
    characterId: "1",  # ID Luke Skywalker
    weaponId: "6"      # Ganti dengan ID senjata yang baru dibuat
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

### 6. Mengupdate Data Karakter

Mutation ini menunjukkan cara mengupdate data yang sudah ada.

```graphql
mutation UpdateCharacterData {
  updateCharacter(input: {
    id: "1",  # ID Luke Skywalker
    species: "Human Jedi"
  }) {
    id
    name
    species
  }
}
```

### 7. Membuat Kendaraan Baru

Mutation ini menunjukkan cara membuat kendaraan baru.

```graphql
mutation CreateNewVehicle {
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

### 8. Menghapus Entitas

Mutation ini menunjukkan cara menghapus data.

```graphql
mutation DeleteEntity {
  # Menghapus senjata
  deleteWeapon(id: "6")
  
  # Menghapus kendaraan
  deleteVehicle(id: "6")
  
  # Menghapus Force Order
  deleteForceOrder(id: "6")
}
```

## Contoh Penggunaan dengan Variabel di Postman

Untuk menggunakan variabel di Postman:

1. Pilih metode POST
2. Masukkan URL: `http://localhost:8000/graphql`
3. Di tab "Body", pilih "GraphQL"
4. Di kolom "QUERY", masukkan query atau mutation
5. Di kolom "GRAPHQL VARIABLES", masukkan variabel dalam format JSON

Contoh:

Query:
```graphql
query GetCharacter($id: ID!) {
  character(id: $id) {
    name
    species
  }
}
```

Variables:
```json
{
  "id": "1"
}
```

## Contoh Mutation Terintegrasi

Berikut adalah contoh mutation terintegrasi yang membuat karakter lengkap dengan semua relasinya:

```graphql
mutation CreateCompleteCharacter {
  # Buat karakter baru
  newCharacter: createCharacter(input: {
    name: "Ahsoka Tano",
    species: "Togruta",
    homePlanetId: 4
  }) {
    id
    name
  }
  
  # Buat senjata baru
  newWeapon: createWeapon(input: {
    name: "Dual Lightsabers",
    type: "Lightsaber",
    damage: 110,
    range: "Close"
  }) {
    id
    name
  }
  
  # Buat kendaraan baru
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

Setelah mutation di atas berhasil, gunakan ID yang dihasilkan untuk mutation berikutnya:

```graphql
mutation AssignRelations($characterId: ID!, $weaponId: ID!, $vehicleId: ID!) {
  # Hubungkan karakter dengan senjata
  assignWeapon: assignWeapon(input: {
    characterId: $characterId,
    weaponId: $weaponId
  }) {
    id
  }
  
  # Hubungkan karakter dengan kendaraan
  assignVehicle: assignVehicle(input: {
    characterId: $characterId,
    vehicleId: $vehicleId
  }) {
    id
  }
  
  # Hubungkan karakter dengan Force Order
  assignForceOrder: assignForceOrder(input: {
    characterId: $characterId,
    forceOrderId: "1",
    rank: "Jedi Padawan",
    joinedYear: -22
  }) {
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
  "characterId": "8",
  "weaponId": "6",
  "vehicleId": "6"
}
```
