import { Card, Tag } from "antd";
import { CalendarOutlined, EnvironmentOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router";
import dayjs from "dayjs";

interface Trip {
  trip_id: string;
  name: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  created_at: string;
  updated_at: string;
}

interface TripCardProps {
  trip: Trip;
}

export const TripCard = ({ trip }: TripCardProps) => {
  const navigate = useNavigate();
  
  const handleCardClick = () => {
    navigate(`/trip/${trip.trip_id}`);
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return "TBD";
    return dayjs(dateString).format("MMM D, YYYY");
  };

  const formatDateRange = () => {
    if (!trip.start_date && !trip.end_date) return "Dates TBD";
    if (trip.start_date && trip.end_date) {
      return `${formatDate(trip.start_date)} - ${formatDate(trip.end_date)}`;
    }
    if (trip.start_date) return `Starting ${formatDate(trip.start_date)}`;
    if (trip.end_date) return `Ending ${formatDate(trip.end_date)}`;
    return "Dates TBD";
  };

  const getDaysUntilTrip = () => {
    if (!trip.start_date) return null;
    const days = dayjs(trip.start_date).diff(dayjs(), 'day');
    if (days < 0) return null;
    if (days === 0) return "Today";
    if (days === 1) return "Tomorrow";
    return `${days} days away`;
  };

  const daysUntil = getDaysUntilTrip();

  return (
    <Card 
      className="w-full mb-4 hover:shadow-xl transition-all duration-200 cursor-pointer border-0 shadow-md"
      hoverable
      style={{ borderRadius: '12px' }}
      onClick={handleCardClick}
    >
      <div className="flex flex-col space-y-3">
        <div className="flex justify-between items-start">
          <h3 className="text-2xl font-bold text-gray-900 mb-1">{trip.name}</h3>
          {daysUntil && (
            <Tag color={daysUntil === "Today" ? "red" : daysUntil === "Tomorrow" ? "orange" : "blue"}>
              {daysUntil}
            </Tag>
          )}
        </div>
        
        <div className="flex items-center text-gray-600 mb-2">
          <CalendarOutlined className="mr-2 text-blue-500" />
          <span className="font-medium">{formatDateRange()}</span>
        </div>
        
        {trip.description && (
          <div className="flex items-start text-gray-600">
            <EnvironmentOutlined className="mr-2 mt-1 text-green-500 flex-shrink-0" />
            <span className="text-gray-700">{trip.description}</span>
          </div>
        )}
      </div>
    </Card>
  );
};