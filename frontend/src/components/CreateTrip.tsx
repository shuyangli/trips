import { useState } from "react";
import { useNavigate } from "react-router";
import { message } from "antd";
import { axiosInstance } from "../api/axiosInstance";
import { TripForm } from "./TripForm";

interface TripFormData {
  tripName?: string;
  destination?: string;
  dateRange?: [import("dayjs").Dayjs, import("dayjs").Dayjs];
  participants?: string[];
}

export const CreateTrip = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (data: TripFormData) => {
    const { tripName, destination, dateRange, participants } = data;
    const [startDate, endDate] = dateRange ?? [];
    
    setLoading(true);
    try {
      await axiosInstance.post("/api/v1/trips", {
        name: tripName,
        description: destination,
        start_date: startDate?.toISOString(),
        end_date: endDate?.toISOString(),
      });

      // TODO: Add participant invitations here when backend is ready
      if (participants && participants.length > 0) {
        console.log("Participants to invite:", participants);
        // Future: Call API to invite participants
      }

      message.success("Trip created successfully!");
      navigate("/"); // Navigate back to trip list
    } catch (error) {
      console.error(error);
      message.error("Failed to create trip. Please try again.");
      throw error; // Re-throw to prevent form reset
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white">
      <TripForm 
        mode="create" 
        onSubmit={handleSubmit}
        loading={loading}
      />
    </div>
  );
};
