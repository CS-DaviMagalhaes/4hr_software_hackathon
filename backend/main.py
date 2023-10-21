from fastapi import FastAPI, Request, Body
import httpx
import pandas as pd
import json
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
#mount frontend
# Serve static files (HTML)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="frontend")

#apis
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/pokemon/{name}")
async def get_pokemon(name: str):
    pokeapi_url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    

    async with httpx.AsyncClient() as client:
        response = await client.get(pokeapi_url)
        if response.status_code == 200:
            pokemon_data = response.json()

            #Obtener solamente los nombres de las habilidades
            ability_names = [ability["ability"]["name"] for ability in pokemon_data["abilities"]]
            types = [type["type"]["name"] for type in pokemon_data["types"]]
            return {
                "name": pokemon_data["name"],
                "height": pokemon_data["height"],
                "weight": pokemon_data["weight"],
                "types": types,
                "abilities": ability_names,
            }
        else:
            return {"error": "Pokemon not found"}
    return templates.TemplateResponse("index.html", {"request": request, "name": name})


@app.get("/pokemon/{number}")
async def get_pokemon(number: int):
    pokeapi_url = f"https://pokeapi.co/api/v2/pokemon/{number}"
    

    async with httpx.AsyncClient() as client:
        response = await client.get(pokeapi_url)
        if response.status_code == 200:
            pokemon_data = response.json()

            #Obtener solamente los nombres de las habilidades
            ability_names = [ability["ability"]["name"] for ability in pokemon_data["abilities"]]
            types = [type["type"]["name"] for type in pokemon_data["types"]]
            return {
                "name": pokemon_data["name"],
                "height": pokemon_data["height"],
                "weight": pokemon_data["weight"],
                "types": types,
                "abilities": ability_names,
            }
        else:
            return {"error": "Pokemon not found"}
        
#get data to json
async def fetch_all_pokemon_data():
    result_df = pd.DataFrame()
    for i in range(1, 301):
        data = await get_pokemon(i)
        df = pd.DataFrame([data])
        result_df = pd.concat([result_df, df], ignore_index=True)

    # Convert the DataFrame to a list of dictionaries
    data_list = result_df.to_dict(orient='records')

    # Append the data to a JSON file
    with open('pokemon_data.json', 'a') as json_file:
        json_file.write('[')
        for item in data_list:
            json.dump(item, json_file)
            json_file.write(',')
            json_file.write('\n')
        json_file.write(']')
if __name__ == "__main__":
    import uvicorn

    # Create an event loop and run the asynchronous function
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    loop.run_until_complete(fetch_all_pokemon_data())
