from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_products():
    return {"message": "List of products"}

@router.post("/")
async def create_product():
    return {"message": "Product created"}
