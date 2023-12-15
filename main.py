from fastapi import FastAPI
import strawberry
from strawberry.asgi import GraphQL
from typing import List, Optional
import requests

@strawberry.type
class BookClub:
    title: str
    organizer: str

@strawberry.type
class Query:
    @strawberry.field
    def bookclubs(self, title: Optional[str] = None, organizer: Optional[str] = None) -> List[BookClub]:
        bookclubs_data = [
            BookClub(title="Harry Potter", organizer="Lance Wong"),
            BookClub(title="Divergent", organizer="Sahil Mahendrakar"),
            BookClub(title="The Secret Garden", organizer="Rachel Chung"),
            BookClub(title="Magic Treehouse", organizer="Preethi Prakash"),
            BookClub(title="Diary of a Wimpy Kid", organizer="Sana Choudhary"),
            BookClub(title="Hunger Games", organizer="Josh Zhou"),
            BookClub(title="Percy Jackson", organizer="Nicole Lin"),
        ]
                
        filtered_bookclubs = bookclubs_data

        if title:
            filtered_bookclubs = [club for club in filtered_bookclubs if club.title == title]

        if organizer:
            filtered_bookclubs = [club for club in filtered_bookclubs if club.organizer == organizer]

        return filtered_bookclubs

schema = strawberry.Schema(query=Query)

app = FastAPI()

query = '''query getBookClubs {
    bookclubs {
        title
        organizer
    }
}'''

graphql_endpoint = 'http://localhost:8000/graphql'
app.add_route("/graphql", GraphQL(schema, debug=True))

headers = {
    'Content-Type': 'application/json',
}

request_data = {
    'query': query,
}

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI server!"}

@app.get("/show")
def show():
    response = requests.post(graphql_endpoint, json=request_data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return {"error": f"Could not execute GraphQL query. Status code: {response.status_code}"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
