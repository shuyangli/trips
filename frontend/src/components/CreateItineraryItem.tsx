import { useNavigate, useParams } from "react-router";
import { message } from "antd";
import { axiosInstance } from "../api/axiosInstance";
import { ItineraryItemForm, type ItineraryItemFormData } from "./ItineraryItemForm";

export const CreateItineraryItem = () => {
  const navigate = useNavigate();
  const { tripId } = useParams();

  const handleSubmit = async (data: ItineraryItemFormData) => {
    try {
      // Convert Dayjs objects to ISO strings
      const formattedData = {
        ...data,
        trip_id: tripId, // Add the trip ID from the URL
        itinerary_datetime: data.itinerary_datetime?.toISOString(),
        departure_datetime: data.departure_datetime?.toISOString(),
        arrival_datetime: data.arrival_datetime?.toISOString(),
        pickup_datetime: data.pickup_datetime?.toISOString(),
        dropoff_datetime: data.dropoff_datetime?.toISOString(),
        check_in_datetime: data.check_in_datetime?.toISOString(),
        check_out_datetime: data.check_out_datetime?.toISOString(),
        start_datetime: data.start_datetime?.toISOString(),
        end_datetime: data.end_datetime?.toISOString(),
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