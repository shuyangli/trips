import { useContext, useEffect, useState } from "react";
import { message, Spin, Button } from "antd";
import { Link, useNavigate } from "react-router";
import { PlusOutlined } from "@ant-design/icons";
import { axiosInstance } from "../api/axiosInstance";
import { TripCard } from "./TripCard";
import { AuthStatusContext } from "../contexts/AuthStatusContext";
import { ErrorView } from "./ErrorView";
import { LoadingView } from "./LoadingView";

interface Trip {
  trip_id: string;
  name: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  created_at: string;
  updated_at: string;
}

export const TripList = () => {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [loading, setLoading] = useState(true);
  const authStatus = useContext(AuthStatusContext);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTrips = async () => {
      try {
        const response = await axiosInstance.get<Trip[]>("/api/v1/trips");
        setTrips(response.data);
      } catch (error) {
        console.error("Error fetching trips:", error);
        message.error("Failed to load trips");
      } finally {
        setLoading(false);
      }
    };

    // Only fetch trips if user is authenticated and not loading
    if (authStatus.user && !authStatus.loading) {
      void fetchTrips();
    } else if (!authStatus.loading && !authStatus.user) {
      // User is not authenticated
      setLoading(false);
    }
  }, [authStatus.user, authStatus.loading]);

  if (loading || authStatus.loading) {
    return (<LoadingView details="Loading your trips..." />);
  }

  if (!authStatus.user) {
    return (
      <ErrorView
        icon="🔐"
        title="Sign in required"
        details="Please sign in to view your trips and start planning your adventures."
       />);
  }

  return (
    <div className="w-full max-w-5xl mx-auto p-6">
      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Your Upcoming Trips</h1>
            <p className="text-gray-600 text-lg">Plan and manage your future adventures</p>
          </div>
          <Button
            type="primary"
            size="large"
            icon={<PlusOutlined />}
            onClick={() => navigate("/create")}
          >
            Create Trip
          </Button>
        </div>
      </div>

      {trips.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl shadow-sm border border-gray-100">
          <div className="max-w-md mx-auto">
            <div className="text-6xl mb-6">✈️</div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">No upcoming trips yet</h3>
            <p className="text-gray-500 mb-6">Ready to plan your next adventure?</p>
            <Link
              to="/create"
              className="inline-block bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors no-underline"
            >
              Create Your First Trip
            </Link>
          </div>
        </div>
      ) : (
        <div className="grid gap-6">
          {trips.map((trip) => (
            <TripCard key={trip.trip_id} trip={trip} />
          ))}
        </div>
      )}
    </div>
  );
};