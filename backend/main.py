from fastapi import FastAPI, Request, Body
import httpx

app = FastAPI()
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
            return {
                "name": pokemon_data["name"],
                "height": pokemon_data["height"],
            }
        else:
            return {"error": "Pokemon not found"}