# import requests
# from fastapi import FastAPI
#
#
# # def request_url():
# #     # API URL
# #     url = "https://dattebayo-api.onrender.com/characters/?page=1&limit=10"
# #
# #     # Fetching data from the API
# #     response = requests.get(url)
# #
# #     # Check if the request was successful
# #     if response.status_code == 200:
# #         # Parse the JSON response
# #         data = response.json()
# #         print("Data fetched successfully!")
# #         return data
# #     else:
# #         print(f"Failed to fetch data. Status code: {response.status_code}")
# #         return None
#
#
# app = FastAPI()
#
#
# # @app.get("/")
# # async def root():
# #     return {"message": "Hello World", "data": request_url()}
# #
# #
# # @app.get("/hello/{name}")
# # async def say_hello(name: str):
# #     return {"message": f"Hello {name}"}
#
#
# @app.get("/characters/")
# async def characters():
#     try:
#         data = request_url()
#         characters = data["characters"]  # `characters` is likely a list
#         character_data = []
#
#         # Loop through each character in the list and extract relevant information
#         for character in characters:
#             character_data.append({
#                 "id": character["id"],
#                 "name": character["name"]
#             })
#
#         response = {
#             "message": "success",
#             "total": len(characters),
#             "characters": character_data
#         }
#         return response
#
#     except Exception as e:
#         return {"message": str(e)}
#
#
# @app.get("/character/{id}/")
# async def character_by_id(id: int):
#     try:
#         url = f"https://dattebayo-api.onrender.com/characters/{id}"
#         data = requests.get(url)
#         json_data = data.json()
#         response = {
#             "message": "success",
#             "id": json_data["id"],
#             "name": json_data["name"],
#             "images": json_data["images"],
#         }
#         if json_data["personal"]["birthdate"]:
#             response["birthdate"] = json_data["personal"]["birthdate"]
#         if json_data["personal"]["sex"]:
#             response["sex"] = json_data["personal"]["sex"]
#         if json_data["personal"]["kekkeiGenkai"]:
#             response["kekkeiGenkai"] = json_data["personal"]["kekkeiGenkai"]
#         else:
#             response["kekkeiGenkai"] = []
#         return response
#     except Exception as e:
#         return {"message": str(e)}


import requests
from fastapi import FastAPI

app = FastAPI()


def request_url(endpoint: str):
    url = f"https://dattebayo-api.onrender.com/{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


@app.get("/characters/")
async def characters():
    try:
        data = request_url("characters/?page=1&limit=10")
        characters = data.get("characters", [])
        character_data = [
            {
                "id": character["id"],
                "name": character["name"],
                "images": character["images"][0] if len(character["images"]) > 0 else None
            }
            for character in characters
        ]

        character_data.append({"id": None, "name": None, "images": None})

        return {
            "message": "success",
            "total": len(characters),
            "characters": character_data
        }

    except requests.exceptions.RequestException as e:
        return {"message": f"API request failed: {str(e)}"}
    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}


@app.get("/character/{id}/")
async def character_by_id(id: int):
    try:
        json_data = request_url(f"characters/{id}")
        personal_data = json_data.get("personal", {})

        return {
            "message": "success",
            "id": json_data["id"],
            "name": json_data["name"],
            "images": json_data.get("images", []),
            "birthdate": personal_data.get("birthdate"),
            "sex": personal_data.get("sex"),
            "kekkeiGenkai": personal_data.get("kekkeiGenkai", None)
        }

    except requests.exceptions.RequestException as e:
        return {"message": f"API request failed: {str(e)}"}
    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}
