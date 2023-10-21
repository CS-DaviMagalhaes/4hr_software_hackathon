import psycopg2
import json

def uploadToDb():
    db_config = {
        'dbname': 'Pokemon',
        'user': 'postgres',
        'password': 'coconut',
        'host': 'localhost',
        'port': 5432
    }

    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    with open(r'C:\Users\HP\Desktop\UTEC\Ciclo_VI\Ingenieria_de_software\Hackaton\pokemon_data.json') as pokemon_file:
        data = json.load(pokemon_file)
        cursor.execute("CREATE TABLE if not exists pokemon (id SERIAL PRIMARY KEY, name VARCHAR(255), height INTEGER, weight INTEGER, types TEXT[], abilities TEXT[], sprite VARCHAR(255), held_items JSON);")

    for entry in data:
        name = entry['name']
        height = entry['height']
        weight = entry['weight']
        types = entry['types']
        abilities = entry['abilities']
        sprite = entry['sprite']
        held_items = json.dumps(entry['held_items'])  # Convertir a JSON si es necesario

        # Inserta la fila en la base de datos
        cursor.execute("INSERT INTO pokemon (name, height, weight, types, abilities, sprite, held_items) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, height, weight, types, abilities, sprite, held_items))
    
    connection.commit()

    cursor.close()
    connection.close()

