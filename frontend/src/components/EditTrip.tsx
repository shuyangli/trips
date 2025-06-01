import { useState, useEffect, useContext } from "react";
import { useParams, useNavigate } from "react-router";
import { message, Spin } from "antd";
import { axiosInstance } from "../api/axiosInstance";
import { TripForm } from "./TripForm";
import { AuthStatusContext } from "../contexts/AuthStatusContext";
import { LoadingView } from "./LoadingView";

interface TripFormData {
  tripName?: string;
  destination?: string;
  dateRange?: [import("dayjs").Dayjs, import("dayjs").Dayjs];
  participants?: string[];
}

interface TripDetails {
  trip_id: string;
  name: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  created_at: string;
  updated_at: string;
}

export const EditTrip = () => {
  const { tripId } = useParams<{ tripId: string }>();
  const navigate = useNavigate();
  const authStatus = useContext(AuthStatusContext);
  const [trip, setTrip] = useState<TripDetails | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTripDetails = async () => {
      if (!tripId) {
        navigate("/");
        return;
      }

      try {
        const response = await axiosInstance.get<TripDetails>(`/api/v1/trips/${tripId}`);
        setTrip(response.data);
      } catch (error) {
        console.error("Error fetching trip details:", error);
        message.error("Failed to load trip details");
        navigate("/");
      } finally {
        setLoading(false);
      }
    };

    if (authStatus.user && !authStatus.loading) {
      fetchTripDetails();
    } else if (!authStatus.loading && !authStatus.user) {
      setLoading(false);
      navigate("/");
    }
  }, [tripId, authStatus.user, authStatus.loading, navigate]);

  const handleSubmit = async (data: TripFormData) => {
    if (!tripId) return;

    const { tripName, destination, dateRange, participants } = data;
    const [startDate, endDate] = dateRange ?? [];

    try {
      // Update trip details
      await axiosInstance.put(`/api/v1/trips/${tripId}`, {
        name: tripName,
        description: destination,
        start_date: startDate?.toISOString(),
        end_date: endDate?.toISOString(),
      });

      // Send invitations to new participants
      if (participants && participants.length > 0) {
        const invitationPromises = participants.map(email =>
          axiosInstance.post(`/api/v1/trips/${tripId}/invite`, {
            email: email.trim()
          }).catch(error => {
            console.error(`Failed to invite ${email}:`, error);
            message.warning(`Failed to invite ${email}`);
          })
        );

        await Promise.allSettled(invitationPromises);

        const successfulInvites = participants.length;
        if (successfulInvites > 0) {
          message.success(`Trip updated! Invitations sent to ${successfulInvites} additional participant${successfulInvites > 1 ? 's' : ''}.`);
        } else {
          message.success("Trip updated successfully!");
        }
      } else {
        message.success("Trip updated successfully!");
      }

      navigate(`/trip/${tripId}`);
    } catch (error) {
      console.error(error);
      message.error("Failed to update trip. Please try again.");
      throw error;
    }
  };

  if (loading || authStatus.loading) {
    return (<LoadingView details="Loading trip details..." />);
  }

  if (!authStatus.user) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-white">
        <p className="text-gray-500 text-lg">Please sign in to edit trips.</p>
      </div>
    );
  }

  if (!trip) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-white">
        <p className="text-gray-500 text-lg">Trip not found.</p>
      </div>
    );
  }

  return (
    <TripForm
      mode="edit"
      initialValues={trip}
      onSubmit={handleSubmit}
    />
  );
};