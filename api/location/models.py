from sqlalchemy import (Column, String, Integer, Enum, Index, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Sequence
from helpers.database import Base
from api.structure.models import Structure  # noqa: F401
from utilities.utility import Utility, StateType, cascade_soft_delete
import enum


class CountryType(enum.Enum):
    Uganda = "Uganda"
    Kenya = "Kenya"
    Nigeria = "Nigeria"


class TimeZoneType(enum.Enum):
    EAST_AFRICA_TIME = "UTC+3"
    WEST_AFRICA_TIME = "UTC+1"


class Location(Base, Utility):
    __tablename__ = 'locations'
    id = Column(Integer, Sequence('locations_id_seq',
                                  start=1, increment=1), primary_key=True)
    name = Column(String, nullable=False)
    abbreviation = Column(String, nullable=False)
    country = Column(Enum(CountryType))
    time_zone = Column(Enum(TimeZoneType))
    image_url = Column(String)
    state = Column(Enum(StateType), default="active")
    structure_id = Column(
        Integer,
        ForeignKey('structure.id', ondelete="CASCADE"),
        nullable=False
    )
    structure = relationship('OfficeStructure')

    office_structures_id = Column(
        Integer,
        ForeignKey('office_structures.id', ondelete="CASCADE"),
        nullable=False
    )
    office_structures = relationship('Structure')
    rooms = relationship(
        'Room', cascade="all, delete-orphan",
        order_by="func.lower(Room.name)")
    __table_args__ = (
        Index(
            'ix_unique_location_content',
            'name',
            unique=True,
            postgresql_where=(state == 'active')),
    )


cascade_soft_delete(
    Location, 'room', 'location_id'
)
