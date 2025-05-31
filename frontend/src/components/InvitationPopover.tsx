import { useContext, useEffect, useState } from "react";
import { Badge, Button, Empty, List, Popover, message } from "antd";
import { BellOutlined, CheckOutlined, CloseOutlined } from "@ant-design/icons";
import dayjs from "dayjs";
import { axiosInstance } from "../api/axiosInstance";
import { AuthStatusContext } from "../contexts/AuthStatusContext";

interface TripInvitation {
  trip_id: string;
  user_id: string;
  status: string;
  created_at: string;
  updated_at: string;
  trip_name: string;
  trip_description?: string;
  start_date?: string;
  end_date?: string;
  inviter_given_name: string;
  inviter_family_name: string;
}

export const InvitationPopover = () => {
  const [invitations, setInvitations] = useState<TripInvitation[]>([]);
  const [loading, setLoading] = useState(false);
  const [popoverVisible, setPopoverVisible] = useState(false);
  const authStatus = useContext(AuthStatusContext);

  const fetchInvitations = async () => {
    if (!authStatus.user) return;

    setLoading(true);
    try {
      const response = await axiosInstance.get<TripInvitation[]>("/api/v1/invitations");
      setInvitations(response.data);
    } catch (error) {
      console.error("Error fetching invitations:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (authStatus.user && !authStatus.loading) {
      fetchInvitations();
    }
  }, [authStatus.user, authStatus.loading]);

  const handleResponse = async (tripId: string, response: "joined" | "declined") => {
    try {
      await axiosInstance.post(`/api/v1/trips/${tripId}/respond`, {
        response: response
      });

      message.success(`Invitation ${response === "joined" ? "accepted" : "declined"} successfully!`);

      // Remove the invitation from the list
      setInvitations(prev => prev.filter(inv => inv.trip_id !== tripId));
    } catch (error) {
      console.error("Error responding to invitation:", error);
      message.error("Failed to respond to invitation");
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return "TBD";
    return dayjs(dateString).format("MMM D, YYYY");
  };

  const formatDateRange = (invitation: TripInvitation) => {
    if (!invitation.start_date && !invitation.end_date) return "Dates TBD";
    if (invitation.start_date && invitation.end_date) {
      return `${formatDate(invitation.start_date)} - ${formatDate(invitation.end_date)}`;
    }
    if (invitation.start_date) return `Starting ${formatDate(invitation.start_date)}`;
    if (invitation.end_date) return `Ending ${formatDate(invitation.end_date)}`;
    return "Dates TBD";
  };

  const popoverContent = (
    <div className="w-80">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-lg font-semibold">Trip Invitations</h3>
        <Button
          type="text"
          size="small"
          onClick={fetchInvitations}
          loading={loading}
        >
          Refresh
        </Button>
      </div>

      {invitations.length === 0 ? (
        <Empty
          image={Empty.PRESENTED_IMAGE_SIMPLE}
          description="No pending invitations"
        />
      ) : (
        <List
          dataSource={invitations}
          renderItem={(invitation) => (
            <List.Item className="border-b border-gray-100 last:border-b-0 py-3">
              <div className="w-full">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="font-semibold text-gray-900">{invitation.trip_name}</h4>
                    <p className="text-sm text-gray-600">
                      Invited by {invitation.inviter_given_name} {invitation.inviter_family_name}
                    </p>
                  </div>
                </div>

                <p className="text-sm text-gray-500 mb-2">{formatDateRange(invitation)}</p>

                {invitation.trip_description && (
                  <p className="text-sm text-gray-600 mb-3">{invitation.trip_description}</p>
                )}

                <div className="flex space-x-2">
                  <Button
                    type="primary"
                    size="small"
                    icon={<CheckOutlined />}
                    onClick={() => handleResponse(invitation.trip_id, "joined")}
                  >
                    Accept
                  </Button>
                  <Button
                    size="small"
                    icon={<CloseOutlined />}
                    onClick={() => handleResponse(invitation.trip_id, "declined")}
                  >
                    Decline
                  </Button>
                </div>
              </div>
            </List.Item>
          )}
        />
      )}
    </div>
  );

  if (!authStatus.user) {
    return null;
  }

  return (
    <Popover
      content={popoverContent}
      title={null}
      trigger="click"
      placement="bottomRight"
      open={popoverVisible}
      onOpenChange={setPopoverVisible}
    >
      <Badge count={invitations.length} size="small">
        <Button
          type="text"
          icon={<BellOutlined />}
          className="flex items-center"
        />
      </Badge>
    </Popover>
  );
};