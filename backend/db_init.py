import psycopg2
import json

db_config = {
    'dbname': 'Pokemon',
    'user': 'postgres',
    'password': 'coconut',
    'host': 'localhost',
    'port': 5432
}

connection = psycopg2.connect(**db_config)
cursor = connection.cursor()

with open(r'C:\Users\HP\Desktop\UTEC\Ciclo_VI\Ingenieria_de_software\Hackaton\backend\pokemon_data.json') as pokemon_file:
    data = json.load(pokemon_file)
    cursor.execute("CREATE TABLE if not exists pokemon (name VARCHAR(255), height INTEGER, weight INTEGER, types TEXT[], abilities TEXT[]);")

for entry in data:
    name = entry['name']
    height = entry['height']
    weight = entry['weight']
    types = entry['types']
    abilities = entry['abilities']

    # Inserta la fila en la base de datos
    cursor.execute("INSERT INTO pokemon (name, height, weight, types, abilities) VALUES (%s, %s, %s, %s, %s)", (name, height, weight, types, abilities))
connection.commit()

cursor.close()
connection.close()