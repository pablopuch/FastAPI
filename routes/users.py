from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


#Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int



users_fake = [
    User(id=1, name="Pepe", surname="Santana", url="https://pepe.com", age=33),
    User(id=2, name="Juan", surname="hoki", url="https://juan.com", age=16),
    User(id=3, name="Ana", surname="Armas", url="https://ana.com", age=22),
]



@router.get("/users")
async def all_users():
    return users_fake


# Path

@router.get("/user/{id}")
async def user(id: int):
    user = filter(lambda user: user.id == id, users_fake)
    try:
        
        return list(user)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    
  
  
# Query   

@router.get("/userquery/")
async def user(id: int):
    return search_user(id)




@router.post("/user/", response_model=User, status_code=201)
async def new_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
        
    users_fake.append(user)
    return user
    
    

@router.put("/user/")
async def update_user(user: User):
    
    found = False
    
    for index, saved_user in enumerate(users_fake):
        if saved_user.id == user.id:
            users_fake[index] = user
            found = True
            
    if not found:
        return {"error": "No se ha actualizado el usuario"}

    return user
    
 
 
@router.delete("/user/{id}")
async def update_user(id: int):
    
    found = False
    
    for index, saved_user in enumerate(users_fake):
        if saved_user.id == id:
            del users_fake[index]
            found = True
                
                
    if not found:
        return {"error": "No se ha eliminado el usuario"}

    return users_fake
    
    
    
    
    
    
    
    

def search_user(id: int):
    user = filter(lambda user: user.id == id, users_fake)
    try:  
         
        return list(user)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}