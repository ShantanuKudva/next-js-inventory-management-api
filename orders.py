from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
import models
from db import engine, SessionLocal
from sqlalchemy.orm import Session

from datetime import datetime
from sqlalchemy import func

app = FastAPI()


# Add CORS middleware with appropriate configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin (you can restrict it to specific origins)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allow specific HTTP methods
    allow_headers=["*"],  # Allow all headers
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

class ProductPartAssociations(BaseModel):
    id:int
    product_id:int
    part_id:int
    quantity:int 

    class Config:
        orm_mode = True


class Parts(BaseModel):
    part_id:int
    part_name:str = Field(min_length=1, max_length=1000)
    inventory_quantity: int
    class Config:
        orm_mode = True

class Products(BaseModel):
    product_id: int
    name:str = Field(min_length=1)
    description:str = Field(min_length=1, max_length=1000)
    class Config:
        orm_mode = True

class Order(BaseModel):
    order_id:int
    product_id:int
    quantity: int = Field(gt=0)
    order_date:datetime = None
    status:str = Field(min_length=1)
    class Config:
        orm_mode = True



# Orders' APIS

@app.get('/api/orders/')
def read_orders(db:Session=Depends(get_db)):
    return db.query(models.Orders).all()

@app.post("/api/orders/")
def post_orders(order:Order, db:Session=Depends(get_db)):
    orders_model = models.Orders()
    orders_model.order_id =  order.order_id
    orders_model.product_id =  order.product_id
    orders_model.quantity =  order.quantity
    orders_model.status =  order.status
    orders_model.order_date = order.order_date
    db.add(orders_model)
    db.commit()

    return order


@app.put('/api/orders/{order_id}')
def update_orders(order_id:int, order:Order, db: Session=Depends(get_db)):
    order_model = db.query(models.Orders).filter(models.Orders.order_id == order_id).first()
    if order_model is None:
        raise HTTPException(
            status_code=404,
            detail = f"order of {order_id} not found"
        )
            
    order_model.order_id =  order.order_id
    order_model.product_id =  order.product_id
    order_model.quantity =  order.quantity
    order_model.status =  order.status
    order_model.order_date = order.order_date
    db.add(order_model)
    db.commit()

    return order


@app.delete('/api/orders/{order_id}')
def delete_orders(order_id: int, db:Session = Depends(get_db)):
    order_model = db.query(models.Orders).filter(models.Orders.order_id == order_id).first()
    if order_model is None:
        raise HTTPException(
            status_code=404,
            detail = f"order of {order_id} not found"
        )
    order_model = db.query(models.Orders).filter(models.Orders.order_id == order_id).delete()
    db.commit()

    return {"message": f"order of id {order_id} deleted successfully"}





#Parts' API's

@app.get('/api/parts/')
def read_parts(db:Session=Depends(get_db)):
    return db.query(models.Parts).all()

@app.post("/api/parts/")
def post_parts(parts:Parts, db:Session=Depends(get_db)):
    parts_model = models.Parts()
    parts_model.part_id =  parts.part_id
    parts_model.part_name =  parts.part_name
    db.add(parts_model)
    db.commit()

    return parts


@app.put('/api/parts/{part_id}')
def update_parts(part_id:int, parts:Parts, db: Session=Depends(get_db)):
    parts_model = db.query(models.Parts).filter(models.Parts.part_id == part_id).first()
    if parts_model is None:
        raise HTTPException(
            status_code=404,
            detail = f"part of {part_id} not found"
        )
            
    parts_model.part_id =  parts.part_id
    parts_model.part_name =  parts.part_name
    db.add(parts_model)
    db.commit()

    return parts


@app.delete('/api/parts/{part_id}')
def delete_parts(part_id: int, db:Session = Depends(get_db)):
    parts_model = db.query(models.Parts).filter(models.Parts.part_id == part_id).first()
    if parts_model is None:
        raise HTTPException(
            status_code=404,
            detail = f"part of {part_id} not found"
        )
    parts_model = db.query(models.Parts).filter(models.Parts.part_id == part_id).delete()
    db.commit()

    return {"message": f"part of id {part_id} deleted successfully"}




#Products' API's

@app.get('/api/products/')
def read_products(db:Session=Depends(get_db)):
    return db.query(models.Products).all()

@app.post("/api/products/")
def post_parts(products:Products, db:Session=Depends(get_db)):
    products_model = models.Products()
    products_model.product_id =  products.product_id
    products_model.name =  products.name
    products_model.description  = products.description
    db.add(products_model)
    db.commit()

    return products


@app.put('/api/products/{product_id}')
def update_products(product_id:int, products:Products, db: Session=Depends(get_db)):
    products_model = db.query(models.Products).filter(models.Products.product_id == product_id).first()
    if products_model is None:
        raise HTTPException(
            status_code=404,
            detail = f"product of {product_id} not found"
        )
            
    products_model.product_id =  products.product_id
    products_model.name =  products.name
    products_model.description  = products.description
    db.add(products_model)
    db.commit()

    return products


@app.delete('/api/products/{product_id}')
def delete_products(product_id: int, db:Session = Depends(get_db)):
    products_model = db.query(models.Product).filter(models.func.lower(models.func.replace(models.Product.name, ' ', '')) == product_name.lower().replace(' ', '')).first()

    if products_model is None:
        raise HTTPException(
            status_code=404,
            detail = f"product of {product_id} not found"
        )
  
    products_model = db.query(models.Products).filter(models.Products.product_id == product_id).delete()
    db.commit()

    return {"message": f"product of id {product_id} deleted successfully"}





#PPA's API's

@app.get('/api/ppa/')
def read_ppa(db:Session=Depends(get_db)):
    return db.query(models.ProductPartAssociation).all()

@app.post("/api/ppa/")
def post_ppa(ppa:ProductPartAssociations, db:Session=Depends(get_db)):
    ppa_model = models.ProductPartAssociation()

    ppa_model.id = ppa.id
    ppa_model.product_id =  ppa.product_id
    ppa_model.part_id =  ppa.part_id
    ppa_model.quantity  = ppa.quantity
    db.add(ppa_model)
    db.commit()

    return ppa


@app.put('/api/ppa/{id}')
def update_ppa(id:int, ppa:ProductPartAssociations, db: Session=Depends(get_db)):
    ppa_model = db.query(models.ProductPartAssociation).filter(models.ProductPartAssociation.id == id).first()
    if ppa_model is None:
        raise HTTPException(
            status_code=404,
            detail = f"PPA of {id} not found"
        )
            
    ppa_model.id = ppa.id
    ppa_model.product_id =  ppa.product_id
    ppa_model.part_id =  ppa.part_id
    ppa_model.quantity  = ppa.quantity
    db.add(ppa_model)
    db.commit()

    return ppa



@app.delete('/api/ppa/{id}')
def delete_ppa(id: int, db:Session = Depends(get_db)):
    ppa_model = db.query(models.ProductPartAssociation).filter(models.ProductPartAssociation.id == id).first()
    if ppa_model is None:
        raise HTTPException(
            status_code=404,
            detail = f"PPA of {id} not found"
        )
            
    ppa_model = db.query(models.ProductPartAssociation).filter(models.ProductPartAssociation.id == id).delete()
    db.commit()

    return {"message": f"PPA of id {id} deleted successfully"}


@app.get("/api/product/{product_name}/{number}/parts")
def get_parts_for_product_with_factor(number: int, product_name: str, db: Session = Depends(get_db)):
    try:
        # Convert product_name to lowercase and remove spaces
        product_name_cleaned = product_name.replace(" ", "").lower()

        # Query the database to find the product by name
        product = db.query(models.Products).filter(func.lower(models.Products.name) == product_name_cleaned).first()
        if product:
            product_id = product.product_id

            # Query the product part associations to get the parts required for the product
            product_parts = (
                db.query(models.ProductPartAssociation)
                .filter(models.ProductPartAssociation.product_id == product_id)
                .all()
            )

            # Retrieve the details of each part
            parts_info = []
            for product_part in product_parts:
                part = (
                    db.query(models.Parts)
                    .filter(models.Parts.part_id == product_part.part_id)
                    .first()
                )
                if part:
                    # Calculate the required quantity for each part
                    required_quantity = product_part.quantity * number

                    # Check if there are enough parts available in the inventory
                    if part.inventory_quantity >= required_quantity:
                        parts_info.append(
                            {"part_name": part.part_name, "quantity": required_quantity, "part_id": product_part.part_id}
                        )
                    else:
                        # If parts are not sufficient, return a message without crashing
                        return {"message": f"Not enough {part.part_name} available"}
            
            # If all parts are available, return the parts info
            return {"product_name": product_name, "parts_required": parts_info}
        else:
            # If product is not found, return a message without crashing
            return {"message": "Product not found"}
    except Exception as e:
        # If any other unexpected error occurs, return a standardized message
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Internal Server Error"})
    





@app.get("/api/product/{product_name}/parts")
def get_parts_for_product(product_name: str, db: Session = Depends(get_db)):
    try:
        # Convert product_name to lowercase and remove spaces
        product_name_cleaned = product_name.replace(" ", "").lower()

        # Query the database to find the product by name
        product = db.query(models.Products).filter(func.lower(models.Products.name) == product_name_cleaned).first()
        if product:
            product_id = product.product_id

            # Query the product part associations to get the parts required for the product
            product_parts = (
                db.query(models.ProductPartAssociation)
                .filter(models.ProductPartAssociation.product_id == product_id)
                .all()
            )

            # Retrieve the details of each part
            parts_info = []
            for product_part in product_parts:
                part = (
                    db.query(models.Parts)
                    .filter(models.Parts.part_id == product_part.part_id)
                    .first()
                )
                if part:
                  parts_info.append(
                            {"part_name": part.part_name, "inventory_quantity": part.inventory_quantity, "part_id": product_part.part_id}
                        )
                else:
               # If parts are not sufficient, return a message without crashing
                   return {"message": f"Not available"}
            
            # If all parts are available, return the parts info
            return {"product_name": product_name, "parts_required": parts_info}
        else:
            # If product is not found, return a message without crashing
            return {"message": "Product not found"}
    except Exception as e:
        # If any other unexpected error occurs, return a standardized message
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Internal Server Error"})
    

    