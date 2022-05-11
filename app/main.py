# TODO: create delete request for devices and redis words
# TODO: create tests for devices

import os
import json

from fastapi import FastAPI, Body, Response, Depends, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette import status
import redis
from sqlalchemy.orm import Session

from database.db import Base, engine, get_db
from database import models, schemas


load_dotenv()

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

r = redis.Redis(
    host=os.environ["HOST"],
    port=os.environ["PORT"],
    password=os.environ["PASSWORD"]
)


@app.get("/")
async def home_test():
    return "Hello World"


@app.post("/words", status_code=201)
async def annograms(words: dict = Body(...)):
    """
    Take 2 words
    and check annogram
    if annogram redis count +1
    return count
    """

    if sorted(list(words["word_1"])) == sorted(list(words["word_2"])):
        check = r.get("annogram")
        if not check:
            r.set("annogram", 1)
        else:
            r.set("annogram", int(check) + 1)
        value = r.get("annogram").decode("utf-8")
        return Response(f"Two words are annograms, count: {value}")
    else:
        return Response("Two words are not annograms")
 

@app.delete("/redis", status_code=200)
async def test_redis(word: dict = Body(...)):
    """
    Delete from redis by key
    """

    try:
        r.delete(word["word"])
        return f"word was deleted."
    except:
        return "Something wrong"


@app.post("/devices", status_code=201)
async def create_device(device: schemas.DeviseBase, db: Session = Depends(get_db)):
    """
    Create device
    with optional endpoint
    """

    if device.endpoint:
        new_device = models.Device(dev_type=device.dev_type, dev_id=device.dev_id)
        db.add(new_device)
        db.commit()
        new_endpoint = models.Endpoints(device_id=new_device.id)
        db.add(new_endpoint)
        db.commit()
    else:
        new_device = models.Device(dev_type=device.dev_type, dev_id=device.dev_id)
        db.add(new_device)
        db.commit()
    return device


@app.get("/devices", status_code=200)
async def no_endpoint_devices(db: Session = Depends(get_db)):
    """
    Get all devices without endpoints
    """
    subquery = db.query(models.Device).join(models.Endpoints).filter(models.Endpoints.device_id != None).with_entities(models.Endpoints.device_id).all()
    except_list = [i.device_id for i in subquery]
    devices = db.query(models.Device).filter(models.Device.id.not_in(except_list)).all()
    return devices


@app.delete("/devices/{id}", status_code=200)
async def delete_device(id: str, db: Session = Depends(get_db)):
    """
    Delete device by id
    """

    device_delete = db.query(models.Device).filter(models.Device.dev_id == id).first()
    if device_delete:
        endpoint_delete = db.query(models.Endpoints).filter(models.Endpoints.device_id == device_delete.id).delete()
        db.delete(device_delete)  
        db.commit()
        return f"Device with id: {id} was deleted."
    else:
        raise HTTPException(status_code=404, detail=f"Device with id: {id} not found.")
    
    # value = r.get("annogram")
    # if not value:
    #     value = "Check"
    # return value

    # r.set("foo", "bar".encode("utf-8"))
    # value = r.get("foo").decode("utf-8")
    # return value



# redis-18506.c299.asia-northeast1-1.gce.cloud.redislabs.com:18506
# database name: Ivan-free-db
# password: bsIwj0mAE3zODIm3irCJjn4KVAfWDfBp