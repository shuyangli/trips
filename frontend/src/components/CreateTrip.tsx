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

  const handleSubmit = async (data: TripFormData) => {
    const { tripName, destination, dateRange, participants } = data;
    const [startDate, endDate] = dateRange ?? [];

    try {
      const tripResponse = await axiosInstance.post("/api/v1/trips", {
        name: tripName,
        description: destination,
        start_date: startDate?.toISOString(),
        end_date: endDate?.toISOString(),
      });

      const createdTrip = tripResponse.data;

      // Send invitations to participants
      if (participants && participants.length > 0) {
        const invitationPromises = participants.map(email =>
          axiosInstance.post(`/api/v1/trips/${createdTrip.trip_id}/invite`, {
            email: email.trim()
          }).catch(error => {
            console.error(`Failed to invite ${email}:`, error);
            message.warning(`Failed to invite ${email}`);
          })
        );

        await Promise.allSettled(invitationPromises);

        const successfulInvites = participants.length;
        if (successfulInvites > 0) {
          message.success(`Trip created! Invitations sent to ${successfulInvites} participant${successfulInvites > 1 ? 's' : ''}.`);
        }
      } else {
        message.success("Trip created successfully!");
      }
      navigate("/"); // Navigate back to trip list
    } catch (error) {
      console.error(error);
      message.error("Failed to create trip. Please try again.");
      throw error; // Re-throw to prevent form reset
    }
  };

  return (
    <TripForm
      mode="create"
      onSubmit={handleSubmit}
    />
  );
};
