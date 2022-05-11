from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship

from .db import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    dev_type = Column(String)
    dev_id = Column(String, unique=True)

    endpoints = relationship("Endpoints", back_populates="devices")

class Endpoints(Base):
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))

    devices = relationship("Device", back_populates="endpoints")