from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from models import User, Gender, Role, UserUpdateRequest
######################### To start the server type: uvicorn main:app --reload  in the VSCode terminal #########################
app = FastAPI()

db: List[User] = [
    User(id= UUID("56b77659-6c54-4c06-8152-55724b4d442b"), first_name = "David", last_name = "Zvonaruv", gender = Gender.male, roles = [Role.student]),
    User(id= UUID("e8d4b6f8-332d-404d-94ef-9747a016554d"),first_name = "Shelly", last_name = "Shoval", gender = Gender.female, roles = [Role.admin,Role.user]) 
]

@app.get("/")
async def root():
    return {"Hello" : "World"}

#get all the users
@app.get("/api/v1/users")
async def fetch_users():
    return db

#add a new user to the DB
@app.post("/api/v1/users")
async def register_user(user: User):
    user.id = uuid4() #give the new user a new user id
    db.append(user)
    return {"id": user.id}

#delete a user via its UUID
@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code= 404,
        detail=f"user with id: {user_id} does not exists"
    )
#update user details
@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )
