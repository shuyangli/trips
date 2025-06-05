from datetime import datetime
from typing import Any, Union
import uuid
from pydantic import BaseModel, ConfigDict, Field, field_validator, computed_field

from src.database.models import ItineraryItemType


class ItineraryItemBase(BaseModel):
    """Base class for all itinerary items with common fields."""

    itinerary_item_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    trip_id: str | None = None
    created_by_user_id: str
    type: ItineraryItemType
    itinerary_datetime: datetime | None = None
    booking_reference: str | None = None
    booking_url: str | None = None
    notes: str | None = None
    raw_details_json: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    @field_validator(
        "itinerary_item_id", "trip_id", "created_by_user_id", mode="before"
    )
    @classmethod
    def uuid_to_string(cls, v: Any) -> str:
        if isinstance(v, uuid.UUID):
            return str(v)
        if not isinstance(v, str):
            raise ValueError(f"Invalid value {v} for str-like field.")
        return v


class FlightItineraryItem(ItineraryItemBase):
    type: ItineraryItemType = ItineraryItemType.FLIGHT

    # Ideally these are displayed with timezone in mind.
    origin_airport_code: str
    destination_airport_code: str

    departure_datetime: datetime
    arrival_datetime: datetime

    transport_carrier: str | None = None
    transport_number: str | None = None

    @computed_field
    @property
    def computed_itinerary_datetime(self) -> datetime:
        return self.departure_datetime


class GroundTransportationItineraryItem(ItineraryItemBase):
    type: ItineraryItemType = ItineraryItemType.GROUND_TRANSPORTATION

    # Ideally these are displayed with timezone in mind.
    origin_detail: str
    destination_detail: str

    departure_datetime: datetime
    arrival_datetime: datetime

    transport_carrier: str | None = None
    transport_number: str | None = None

    @computed_field
    @property
    def computed_itinerary_datetime(self) -> datetime:
        return self.departure_datetime


class CarRentalItineraryItem(ItineraryItemBase):
    type: ItineraryItemType = ItineraryItemType.CAR_RENTAL

    # Ideally these are displayed with timezone in mind.
    pickup_location: str
    dropoff_location: str | None = None

    pickup_datetime: datetime
    dropoff_datetime: datetime

    @computed_field
    @property
    def computed_itinerary_datetime(self) -> datetime:
        return self.pickup_datetime


class AccommodationItineraryItem(ItineraryItemBase):
    type: ItineraryItemType = ItineraryItemType.ACCOMMODATION

    address: str

    check_in_datetime: datetime
    check_out_datetime: datetime

    @computed_field
    @property
    def computed_itinerary_datetime(self) -> datetime:
        return self.check_in_datetime


class ActivityItineraryItem(ItineraryItemBase):
    type: ItineraryItemType = ItineraryItemType.ACTIVITY

    description: str | None = None
    location_name: str | None = None

    start_datetime: datetime
    end_datetime: datetime | None = None

    @computed_field
    @property
    def computed_itinerary_datetime(self) -> datetime:
        return self.start_datetime


# Create/Update schemas (without auto-generated fields)
class CreateItineraryItemRequestBase(BaseModel):
    """Base schema for creating itinerary items."""

    trip_id: str | None = None
    type: ItineraryItemType
    itinerary_datetime: datetime | None = None
    booking_reference: str | None = None
    booking_url: str | None = None
    notes: str | None = None
    raw_details_json: dict[str, Any] | None = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("trip_id", mode="before")
    @classmethod
    def uuid_to_string(cls, v: Any) -> str | None:
        if v is None:
            return None
        if isinstance(v, uuid.UUID):
            return str(v)
        if not isinstance(v, str):
            raise ValueError(f"Invalid value {v} for str-like field.")
        return v


class CreateFlightItineraryItemRequest(CreateItineraryItemRequestBase):
    type: ItineraryItemType = ItineraryItemType.FLIGHT
    origin_airport_code: str
    destination_airport_code: str
    departure_datetime: datetime
    arrival_datetime: datetime
    transport_carrier: str | None = None
    transport_number: str | None = None


class CreateGroundTransportationItineraryItemRequest(CreateItineraryItemRequestBase):
    type: ItineraryItemType = ItineraryItemType.GROUND_TRANSPORTATION
    origin_detail: str
    destination_detail: str
    departure_datetime: datetime
    arrival_datetime: datetime
    transport_carrier: str | None = None
    transport_number: str | None = None


class CreateCarRentalItineraryItemRequest(CreateItineraryItemRequestBase):
    type: ItineraryItemType = ItineraryItemType.CAR_RENTAL
    pickup_location: str
    dropoff_location: str | None = None
    pickup_datetime: datetime
    dropoff_datetime: datetime


class CreateAccommodationItineraryItemRequest(CreateItineraryItemRequestBase):
    type: ItineraryItemType = ItineraryItemType.ACCOMMODATION
    address: str
    check_in_datetime: datetime
    check_out_datetime: datetime


class CreateActivityItineraryItemRequest(CreateItineraryItemRequestBase):
    type: ItineraryItemType = ItineraryItemType.ACTIVITY
    description: str | None = None
    location_name: str | None = None
    start_datetime: datetime
    end_datetime: datetime | None = None


# Union type for create request discriminated union based on type field
CreateItineraryItemRequest = Union[
    CreateFlightItineraryItemRequest,
    CreateGroundTransportationItineraryItemRequest,
    CreateCarRentalItineraryItemRequest,
    CreateAccommodationItineraryItemRequest,
    CreateActivityItineraryItemRequest,
]


class ItineraryItemUpdate(BaseModel):
    """Schema for updating itinerary items."""

    trip_id: str | None = None
    type: ItineraryItemType | None = None
    itinerary_datetime: datetime | None = None
    booking_reference: str | None = None
    booking_url: str | None = None
    notes: str | None = None
    raw_details_json: dict[str, Any] | None = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("trip_id", mode="before")
    @classmethod
    def uuid_to_string(cls, v: Any) -> str | None:
        if v is None:
            return None
        if isinstance(v, uuid.UUID):
            return str(v)
        if not isinstance(v, str):
            raise ValueError(f"Invalid value {v} for str-like field.")
        return v


# Union type for discriminated union based on type field
ItineraryItem = Union[
    FlightItineraryItem,
    GroundTransportationItineraryItem,
    CarRentalItineraryItem,
    AccommodationItineraryItem,
    ActivityItineraryItem,
]
