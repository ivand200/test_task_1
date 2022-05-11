from fastapi.testclient import TestClient
import pytest
import json
from app.main import r, app
from sqlalchemy.orm import Session
from database import models, schemas

client = TestClient(app)


def test_models():
    device = models.Device(dev_type="47AXZ", dev_id="XR400")
    assert device.dev_id == "XR400"
    assert device.dev_type == "47AXZ"


def test_devices():
    """
    Create and delete device
    """
    devices = [
        {
            "dev_type": "47AXZ",
            "dev_id": "XR58",
            "endpoint": 1
        },
        {
            "dev_type": "47AXZ",
            "dev_id": "XR56"
        },
        {
            "dev_type": "47AXZ",
            "dev_id": "XR59" 
        }
    ]
    for i in devices:
        response = client.post("/devices", data=json.dumps(i))
        response_body = response.json()
        response_delete = client.delete(f"/devices/{i['dev_id']}")
        response_delete_body = response_delete.json()

        assert response.status_code == 201
        assert response_body["dev_id"] == i["dev_id"]
        assert response_delete.status_code == 200
        assert response_delete_body == f"Device with id: {i['dev_id']} was deleted."


def test_positive_words_redis():
    payload = {
        "word_1": "car",
        "word_2": "rac"
    }
    to_delete = {
        "word": "annogram"
    }

    response = client.post("/words", data=json.dumps(payload))
    response_second = client.post("/words", data=json.dumps(payload))
    response_delete = client.delete("/redis", data=json.dumps(to_delete))

    assert response.status_code == 200
    assert response.text == f"Two words are annograms, count: 1"
    assert response_second.status_code == 200
    assert response_second.text == f"Two words are annograms, count: 2"
    assert response_delete.status_code == 200


def test_negative_words():
    payload = {
        "word_1": "donut",
        "word_2": "donud"
    }

    response = client.post("/words", data=json.dumps(payload))

    assert response.status_code == 200
    assert response.text == "Two words are not annograms"


