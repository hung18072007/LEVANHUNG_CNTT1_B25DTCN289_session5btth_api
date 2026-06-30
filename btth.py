from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

products = [
    {"id": 1, "name": "Keyboard", "price": 500000},
    {"id": 2, "name": "Mouse", "price": 300000}
]

class CreateProducts(BaseModel):
    id : int
    name : str
    price : int

@app.get("/products")
async def show_product():
    return {
        "message": "Lấy dữ liệu công việc thành công" , "data": products, "status_code": 200
    }

@app.post("/products", status_code=201)
async def create_produuct(new_product : CreateProducts):
    if new_product.name == "":
        raise HTTPException(status_code=400, detail="Tên không được rỗng")
    if new_product.price <= 0:
        raise HTTPException(status_code=400, detail="Giá phải lớn hơn 0")

    product_dict = {
        "id": new_product.id,
        "name": new_product.name,
        "price": new_product.price
    }

    products.append(product_dict)
    
    return {
        "message" : "Thêm sản phẩm thành công" , "data" : product_dict
    }
    
@app.delete("/products/{product_id}")
async def del_product(product_id : int ):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {
                "message" : f"Xóa thành công sản phẩm có id : {product_id}"
            }
            
    raise HTTPException(status_code=404, detail="Product not found")