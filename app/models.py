from sqlalchemy import (CheckConstraint, Column, DateTime, ForeignKey,
                        Identity, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class M3UUser(Base):
    __tablename__ = "m3u_users"
    id = Column(Integer, Identity(always=True), primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=True)
    password = Column(String(80))
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    disabled = Column(String(1), CheckConstraint("disabled in ('Y','N')"),
                      nullable=False, default="N")


class Channel(Base):
    __tablename__ = "channel"
    ch_id = Column(String(10), primary_key=True)
    disp_name = Column(String(80), unique=True, nullable=False)
    icon = Column(String(80))
    programmes = relationship("Programme", back_populates="channel_rel")


class Programme(Base):
    __tablename__ = "programme"
    id = Column(Integer, Identity(always=True), primary_key=True)
    channel = Column(String(10), ForeignKey('channel.ch_id'))
    pstart = Column(DateTime(timezone=True), nullable=False)
    pstop = Column(DateTime(timezone=True), nullable=False)
    title = Column(String(400))
    pdesc = Column(String(1500))
    cat = Column(String(50))
    channel_rel = relationship("Channel", back_populates="programmes")
