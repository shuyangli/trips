from datetime import datetime
from enum import StrEnum
from typing import Any
import uuid
from pydantic import BaseModel, Field


class ItineraryItemType(StrEnum):
    UNKNOWN = "unknown"
    FLIGHT = "flight"
    # Trains and buses
    GROUND_TRANSPORTATION = "ground"
    CAR_RENTAL = "car_rental"
    ACCOMMODATION = "accommodation"
    ACTIVITY = "activity"


class FlightItineraryItem(BaseModel):
    type: ItineraryItemType = ItineraryItemType.FLIGHT

    # Ideally these are displayed with timezone in mind.
    origin_airport_code: str
    destination_airport_code: str

    departure_datetime: datetime
    arrival_datetime: datetime

    transport_carrier: str | None = None
    transport_number: str | None = None


class GroundTransportationItineraryItem(BaseModel):
    type: ItineraryItemType = ItineraryItemType.GROUND_TRANSPORTATION

    # Ideally these are displayed with timezone in mind.
    origin_detail: str
    destination_detail: str

    departure_datetime: datetime
    arrival_datetime: datetime

    transport_carrier: str | None = None
    transport_number: str | None = None


class CarRentalItineraryItem(BaseModel):
    type: ItineraryItemType = ItineraryItemType.CAR_RENTAL

    # Ideally these are displayed with timezone in mind.
    pickup_location: str
    dropoff_location: str | None = None

    pickup_datetime: datetime
    dropoff_datetime: datetime


class AccommodationItineraryItem(BaseModel):
    type: ItineraryItemType = ItineraryItemType.ACCOMMODATION

    address: str

    check_in_datetime: datetime
    check_out_datetime: datetime


class ActivityItineraryItem(BaseModel):
    type: ItineraryItemType = ItineraryItemType.ACTIVITY

    description: str | None = None
    location_name: str | None = None

    start_datetime: datetime
    end_datetime: datetime | None


class ItineraryItem(BaseModel):
    """An item in an itinerary, representing a single travel booking (e.g. flight or train),
    accommodation (e.g. hotel or airbnb), or activity (e.g. dining reservation, museum visit).
    """

    itinerary_item_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    # FK to Trip.trip_id
    trip_id: str | None = None

    # FK to User.user_id
    created_by_user_id: str

    # Used for sorting and filtering only
    itinerary_datetime: datetime | None = None

    # Reference for the booking: PNR, hotel confirmation number, etc.
    booking_reference: str | None = None
    # Link to the booking, especially for activities or dining reservations.
    booking_url: str | None = None

    # Other notes about the item
    notes: str | None = None

    # Other semi-structured or unstructured data
    raw_details_json: dict[str, Any] | None = None

    # Perhaps this should support attachments too for things like receipts or tickets.

    created_at: int
    updated_at: int

    # Maybe keep track of price too?
