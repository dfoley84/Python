from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class vCenter(Base):
    __tablename__ = "vCenter"
    id = Column(Integer, primary_key=True)
    vCenterName = Column(String(50), unique=False, nullable=False)
    MachineName = Column(String(50), unique=False, nullable=False)
    MachineOperatingSystem = Column(String(50), unique=False, nullable=False)
    ToolStatus = Column(String(50), unique=False, nullable=False)
    UserName = Column(String(50), unique=False, nullable=False)

   
class Horizon(Base):
    __tablename__ = "Horizon"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ConnectionBroker = Column(String(120), unique=False)
    vPool = Column(String(120), unique=False)
    vCenter = Column(String(120), unique=False)
    MachineName = Column(String(120), unique=False)
    MachineDisplayName = Column(String(120), unique=False)
    MachineStatus = Column(String(120), unique=False)
    MachineOpt = Column(String(120), unique=False)
    ToolStatus = Column(String(120), unique=False)
    UserName = Column(String(120), unique=False)
