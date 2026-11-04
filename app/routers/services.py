from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
import models
from  database import get_db
from redis_client import get_redis
from elasticsearch_client import get_elastic  
import schemas
from auth import get_current_user_id
from typing import List
import json

router = APIRouter()

@router.post("/add/services", response_model=schemas.ServiceResponse, status_code=status.HTTP_201_CREATED)
async def add_services(payload: schemas.ServiceCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if user is None: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "provider":
        raise HTTPException(status_code=403, detail="You cant add the services")
    
    new_service =models.Services(
        title = payload.title,
        description= payload.description,
        service= payload.service,
        charge_rs= payload.charge_rs,
        city= payload.city,
        is_active= payload.is_active
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    es = get_elastic()

    await es.index(index="services", id=str(new_service.id), document={
        "id": new_service.id,
        "service": new_service.service,
        "charge_rs": new_service.charge_rs,
        "city": new_service.city
    })
    r = get_redis()
    await r.delete("catalog:Services")
    return new_service

@router.get("/see/all/services", response_model=List[schemas.ServiceResponse])
async def show_all_services(db:Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cant access the services without being user")

    r = get_redis()
    cache_key = "catalog:Services"
    cached_data = await r.get(cache_key)
    if cached_data:
        products = json.loads(str(cached_data))
        return products
    data_from_db = db.query(models.Services).all()
    product_list = []
    for p in data_from_db:
        product_list.append({
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "service": p.service,
            "charge_rs": p.charge_rs,
            "city": p.city,
            "provider_id": p.provider_id,
            "provider_name": p.provider_name,
            "is_active": p.is_active
        })

    await r.setex(cache_key, 300, json.dumps(product_list))
    return product_list

@router.get("/services/search?q=")
async def search_services(q: str):
    if not q or not q.strip():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User must enter the query to get desired results")
    
    es = get_elastic()
    query_body = {
        "query_body":{
            "multi-match":{
                "query": q,
                "field": ["name"],
                "fuzziness": "AUTO"
            }
        }
    }
    response = await es.search(index="services", body=query_body)
    result = []
    for hit in response["hits"]["hits"]:
        result.append(hit["_source"])

    return {
        "query": q,
        "total": response["hits"]["total"]["Value"],
        "result":result 
    }

@router.get("/service/{id}", response_model=schemas.ServiceResponse)
def get_service(id: int, db : Session = Depends(get_db), current_user_id:int = Depends(get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    services = db.query(models.Services).filter(models.Services.id == id).first()
    if services is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The service is not found")
    return services

@router.put("/services/update/{id}", response_model=schemas.ServiceResponse)
async def update_services(payload: schemas.ServiceCreate ,id: int, db: Session = Depends(get_db), current_id: int = Depends(get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == current_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "provider":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Provider is required to update the services") 
    service_id = db.query(models.Services).filter(models.Services.id == id).first()
    
    if service_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The id doesn't matches the service's id")
    
    service_id.title = payload.title,
    service_id.description =  payload.description,
    service_id.charge_rs =  payload.charge_rs,
    service_id.city =  payload.city,
    service_id.is_active = payload.is_active
    
    
    db.commit()
    db.refresh(service_id)

    es = get_elastic()
    await es.index(index="products", id= str(service_id.id), document={
        "id": service_id.id,
        "service": service_id.service,
        "charge_rs": service_id.charge_rs,
        "city": service_id.city
    })    

    r = get_redis()
    await r.delete("catalog:Services")
    return service_id

@router.delete("/services/delete/{id}")
async def delete_service(service_delete_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if str(user.role) != "provider":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the provider can delete the service")
    service = db.query(models.Services).filter(models.Services.id == service_delete_id).first()
    if service is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Service is not found")
    if service.provider_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the provider of the service can delete the service")
    db.delete(service)
    db.commit()
    es = get_elastic()
    await es.options(ignore_status=404).delete(index="services", id = str(service_delete_id))
    r = get_redis()
    await r.delete("catalog:Services")
