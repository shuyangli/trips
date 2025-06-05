import { useContext, useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router";
import { Card, message, Tag, Button, Empty } from "antd";
import { ArrowLeftOutlined, CalendarOutlined, EnvironmentOutlined, ClockCircleOutlined, EditOutlined } from "@ant-design/icons";
import dayjs from "dayjs";
import { axiosInstance } from "../api/axiosInstance";
import { AuthStatusContext } from "../contexts/AuthStatusContext";
import { ErrorView } from "./ErrorView";
import { LoadingView } from "./LoadingView";

interface TripDetails {
  trip_id: string;
  name: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  created_at: string;
  updated_at: string;
  itinerary_items: ItineraryItem[];
}

interface ItineraryItem {
  itinerary_item_id: string;
  trip_id: string;
  created_by_user_id: string;
  type: string;
  itinerary_datetime?: string;
  booking_reference?: string;
  booking_url?: string;
  notes?: string;
  raw_details_json?: any;
  created_at: string;
  updated_at: string;
}

export const TripDetailPage = () => {
  const { tripId } = useParams<{ tripId: string }>();
  const navigate = useNavigate();
  const authStatus = useContext(AuthStatusContext);
  const [trip, setTrip] = useState<TripDetails | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTripDetails = async () => {
      if (!tripId) return;

      try {
        const response = await axiosInstance.get<TripDetails>(`/api/v1/trips/${tripId}`);
        setTrip(response.data);
      } catch (error) {
        console.error("Error fetching trip details:", error);
        message.error("Failed to load trip details");
        navigate("/"); // Redirect to home if trip not found
      } finally {
        setLoading(false);
      }
    };

    if (authStatus.user && !authStatus.loading) {
      fetchTripDetails();
    } else if (!authStatus.loading && !authStatus.user) {
      setLoading(false);
    }
  }, [tripId, authStatus.user, authStatus.loading, navigate]);

  const formatDate = (dateString?: string) => {
    if (!dateString) return "TBD";
    return dayjs(dateString).format("MMM D, YYYY");
  };

  const formatDateTime = (dateString?: string) => {
    if (!dateString) return "TBD";
    return dayjs(dateString).format("MMM D, YYYY h:mm A");
  };

  const formatDateRange = () => {
    if (!trip?.start_date && !trip?.end_date) return "Dates TBD";
    if (trip?.start_date && trip?.end_date) {
      return `${formatDate(trip.start_date)} - ${formatDate(trip.end_date)}`;
    }
    if (trip?.start_date) return `Starting ${formatDate(trip.start_date)}`;
    if (trip?.end_date) return `Ending ${formatDate(trip.end_date)}`;
    return "Dates TBD";
  };

  const getItemTypeColor = (type: string) => {
    switch (type) {
      case "FLIGHT": return "blue";
      case "ACCOMMODATION": return "green";
      case "ACTIVITY": return "orange";
      case "GROUND_TRANSPORTATION": return "purple";
      case "CAR_RENTAL": return "cyan";
      default: return "default";
    }
  };

  const getItemTypeIcon = (type: string) => {
    switch (type) {
      case "FLIGHT": return "✈️";
      case "ACCOMMODATION": return "🏨";
      case "ACTIVITY": return "🎯";
      case "GROUND_TRANSPORTATION": return "🚊";
      case "CAR_RENTAL": return "🚗";
      default: return "📋";
    }
  };

  if (loading || authStatus.loading) {
    return (<LoadingView details="Loading trip details..." />);
  }

  if (!authStatus.user) {
    return (
      <ErrorView
        icon="🔐"
        title="Sign in required"
        details="Please sign in to view trip details."
       />);
  }

  if (!trip) {
    return (
      <ErrorView
        icon="❌"
        title="Trip not found."
        details="This trip doesn't exist or you don't have access to it.">
          <Button type="primary" onClick={() => navigate("/")} className="mt-4">
            Back to Trips
          </Button>
      </ErrorView>
    );
  }

  return (
    <div className="w-full max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate("/")}
          className="mb-4"
        >
          Back to Trips
        </Button>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
          <div className="flex justify-between items-start mb-4">
            <h1 className="text-4xl font-bold text-gray-900">{trip.name}</h1>
            <Button
              type="primary"
              icon={<EditOutlined />}
              onClick={() => navigate(`/trip/${trip.trip_id}/edit`)}
            >
              Edit Trip
            </Button>
          </div>

          <div className="flex items-center text-gray-600 mb-4">
            <CalendarOutlined className="mr-2 text-blue-500" />
            <span className="font-medium text-lg">{formatDateRange()}</span>
          </div>

          {trip.description && (
            <div className="flex items-start text-gray-600 mb-4">
              <EnvironmentOutlined className="mr-2 mt-1 text-green-500 flex-shrink-0" />
              <span className="text-gray-700 text-lg">{trip.description}</span>
            </div>
          )}
        </div>
      </div>

      {/* Itinerary Section */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Itinerary</h2>
          <Button
            type="primary"
            onClick={() => navigate(`/trip/${trip.trip_id}/createItinerary`)}
          >
            Add Itinerary Item
          </Button>
        </div>

        {trip.itinerary_items.length === 0 ? (
          <Empty
            image={Empty.PRESENTED_IMAGE_SIMPLE}
            description={
              <span className="text-gray-500">
                No itinerary items yet. Start adding flights, hotels, and activities to your trip!
              </span>
            }
          />
        ) : (
          <div className="space-y-4">
            {trip.itinerary_items.map((item) => (
              <Card
                key={item.itinerary_item_id}
                className="border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
                style={{ borderRadius: '8px' }}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-4">
                    <div className="text-2xl">{getItemTypeIcon(item.type)}</div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <Tag color={getItemTypeColor(item.type)}>
                          {item.type.replace('_', ' ')}
                        </Tag>
                        {item.itinerary_datetime && (
                          <div className="flex items-center text-gray-600">
                            <ClockCircleOutlined className="mr-1" />
                            <span className="text-sm">{formatDateTime(item.itinerary_datetime)}</span>
                          </div>
                        )}
                      </div>

                      {item.notes && (
                        <p className="text-gray-700 mb-2">{item.notes}</p>
                      )}

                      {item.booking_reference && (
                        <p className="text-sm text-gray-500">
                          <strong>Reference:</strong> {item.booking_reference}
                        </p>
                      )}

                      {item.booking_url && (
                        <a
                          href={item.booking_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-500 hover:text-blue-700 text-sm"
                        >
                          View Booking
                        </a>
                      )}
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
