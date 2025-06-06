from datetime import datetime
from typing import Any, TypedDict, Union
import uuid
from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.database.models import ItineraryItemType


class ItineraryItem(BaseModel):
    """Base class for all itinerary items with common fields."""

    itinerary_item_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    trip_id: str | None = None
    created_by_user_id: str
    type: ItineraryItemType
    itinerary_datetime: datetime | None = None
    booking_reference: str | None = None
    booking_url: str | None = None
    notes: str | None = None
    details: dict[str, Any] | None = None
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


# Type-specific detail schemas for validation
class FlightDetails(TypedDict):
    origin_airport_code: str | None
    destination_airport_code: str | None
    departure_datetime: datetime | None
    arrival_datetime: datetime | None
    airline_name: str | None
    flight_number: str | None
    seat: str | None


class BusDetails(TypedDict):
    origin_station: str | None
    destination_station: str | None
    departure_datetime: datetime | None
    arrival_datetime: datetime | None
    bus_company: str | None
    bus_number: str | None
    seat: str | None


class TrainDetails(TypedDict):
    origin_station: str | None
    destination_station: str | None
    departure_datetime: datetime | None
    arrival_datetime: datetime | None
    train_company: str | None
    train_number: str | None
    seat: str | None


class CarRentalDetails(TypedDict):
    pickup_location: str | None
    dropoff_location: str | None
    pickup_datetime: datetime | None
    dropoff_datetime: datetime | None


class AccommodationDetails(TypedDict):
    address: str | None
    check_in_datetime: datetime | None
    check_out_datetime: datetime | None


class ActivityDetails(TypedDict):
    description: str | None
    location_name: str | None
    start_datetime: datetime | None
    end_datetime: datetime | None


# Create/Update schemas
class CreateItineraryItemRequest(BaseModel):
    """Schema for creating itinerary items."""

    trip_id: str | None = None
    type: ItineraryItemType
    itinerary_datetime: datetime | None = None
    booking_reference: str | None = None
    booking_url: str | None = None
    notes: str | None = None
    details: dict[str, Any] | None = None

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


class ItineraryItemUpdate(BaseModel):
    """Schema for updating itinerary items."""

    trip_id: str | None = None
    type: ItineraryItemType | None = None
    itinerary_datetime: datetime | None = None
    booking_reference: str | None = None
    booking_url: str | None = None
    notes: str | None = None
    details: dict[str, Any] | None = None

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
