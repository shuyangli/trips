import { useNavigate, useParams } from "react-router";
import { message } from "antd";
import { axiosInstance } from "../api/axiosInstance";
import { ItineraryItemForm, type ItineraryItemFormData } from "./ItineraryItemForm";

export const CreateItineraryItem = () => {
  const navigate = useNavigate();
  const { tripId } = useParams();

  const handleSubmit = async (data: ItineraryItemFormData) => {
    try {
      // Convert Dayjs objects to ISO strings in details
      const details = data.details ? {
        ...data.details,
        departure_datetime: data.details.departure_datetime?.toISOString(),
        arrival_datetime: data.details.arrival_datetime?.toISOString(),
        pickup_datetime: data.details.pickup_datetime?.toISOString(),
        dropoff_datetime: data.details.dropoff_datetime?.toISOString(),
        check_in_datetime: data.details.check_in_datetime?.toISOString(),
        check_out_datetime: data.details.check_out_datetime?.toISOString(),
        start_datetime: data.details.start_datetime?.toISOString(),
        end_datetime: data.details.end_datetime?.toISOString(),
      } : undefined;

      const formattedData = {
        ...data,
        trip_id: tripId, // Add the trip ID from the URL
        itinerary_datetime: data.itinerary_datetime?.toISOString(),
        details,
      };

      await axiosInstance.post("/api/v1/itinerary-items", formattedData);
      message.success("Itinerary item created successfully!");
      navigate(`/trip/${tripId}`); // Navigate back to trip details
    } catch (error) {
      console.error(error);
      message.error("Failed to create itinerary item. Please try again.");
      throw error; // Re-throw to prevent form reset
    }
  };

  return <ItineraryItemForm onSubmit={handleSubmit} />;
};