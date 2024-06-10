from fastapi import APIRouter

router = APIRouter(
    prefix="/products", 
    tags=["products"], 
    responses={404: {"message": "No encontrado"}}
    )

@router.get("/")
async def products():
    return ["producto1","producto2","producto3"]