import { useEffect, useState } from "react";
import { Dayjs } from "dayjs";
import dayjs from "dayjs";
import { Button, DatePicker, Form, Input, Select, TimePicker } from "antd";
import { ItineraryItemType } from "../types/itinerary";

export interface ItineraryItemFormData {
  type: ItineraryItemType;
  trip_id?: string;
  itinerary_datetime?: Dayjs;
  booking_reference?: string;
  booking_url?: string;
  notes?: string;
  // Flight specific
  origin_airport_code?: string;
  destination_airport_code?: string;
  departure_datetime?: Dayjs;
  arrival_datetime?: Dayjs;
  transport_carrier?: string;
  transport_number?: string;
  // Ground Transportation specific
  origin_detail?: string;
  destination_detail?: string;
  // Car Rental specific
  pickup_location?: string;
  dropoff_location?: string;
  pickup_datetime?: Dayjs;
  dropoff_datetime?: Dayjs;
  // Accommodation specific
  address?: string;
  check_in_datetime?: Dayjs;
  check_out_datetime?: Dayjs;
  // Activity specific
  description?: string;
  location_name?: string;
  start_datetime?: Dayjs;
  end_datetime?: Dayjs;
}

export interface ItineraryItemFormProps {
  initialValues?: {
    type?: ItineraryItemType;
    trip_id?: string;
    itinerary_datetime?: string;
    booking_reference?: string;
    booking_url?: string;
    notes?: string;
    // Add other fields as needed
  };
  onSubmit: (data: ItineraryItemFormData) => Promise<void>;
}

export const ItineraryItemForm = ({ initialValues, onSubmit }: ItineraryItemFormProps) => {
  const [form] = Form.useForm();
  const [submitting, setSubmitting] = useState(false);
  const [selectedType, setSelectedType] = useState<ItineraryItemType | undefined>(initialValues?.type);
  const isCreateMode = initialValues === undefined;

  useEffect(() => {
    if (initialValues) {
      const itinerary_datetime = initialValues.itinerary_datetime
        ? dayjs(initialValues.itinerary_datetime)
        : undefined;

      form.setFieldsValue({
        type: initialValues.type,
        trip_id: initialValues.trip_id,
        itinerary_datetime,
        booking_reference: initialValues.booking_reference,
        booking_url: initialValues.booking_url,
        notes: initialValues.notes,
      });
      setSelectedType(initialValues.type);
    }
  }, [form, initialValues]);

  const handleSubmit = async (values: ItineraryItemFormData) => {
    try {
      setSubmitting(true);
      await onSubmit(values);
    } catch (error) {
      // Error handling is done in the parent component
    } finally {
      setSubmitting(false);
    }
  };

  const renderTypeSpecificFields = () => {
    switch (selectedType) {
      case ItineraryItemType.FLIGHT:
        return (
          <>
            <Form.Item
              name="origin_airport_code"
              label="Origin Airport Code"
              rules={[{ required: true, message: 'Please input the origin airport code!' }]}
            >
              <Input placeholder="e.g., JFK" />
            </Form.Item>
            <Form.Item
              name="destination_airport_code"
              label="Destination Airport Code"
              rules={[{ required: true, message: 'Please input the destination airport code!' }]}
            >
              <Input placeholder="e.g., LAX" />
            </Form.Item>
            <Form.Item
              name="departure_datetime"
              label="Departure Time"
              rules={[{ required: true, message: 'Please select the departure time!' }]}
            >
              <DatePicker showTime className="w-full" />
            </Form.Item>
            <Form.Item
              name="arrival_datetime"
              label="Arrival Time"
              rules={[{ required: true, message: 'Please select the arrival time!' }]}
            >
              <DatePicker showTime className="w-full" />
            </Form.Item>
            <Form.Item name="transport_carrier" label="Airline">
              <Input placeholder="e.g., Delta Airlines" />
            </Form.Item>
            <Form.Item name="transport_number" label="Flight Number">
              <Input placeholder="e.g., DL123" />
            </Form.Item>
          </>
        );

      case ItineraryItemType.GROUND_TRANSPORTATION:
        return (
          <>
            <Form.Item
              name="origin_detail"
              label="Origin"
              rules={[{ required: true, message: 'Please input the origin!' }]}
            >
              <Input placeholder="e.g., Tokyo Station" />
            </Form.Item>
            <Form.Item
              name="destination_detail"
              label="Destination"
              rules={[{ required: true, message: 'Please input the destination!' }]}
            >
              <Input placeholder="e.g., Shinjuku Station" />
            </Form.Item>
            <Form.Item
              name="departure_datetime"
              label="Departure Time"
              rules={[{ required: true, message: 'Please select the departure time!' }]}
            >
              <DatePicker showTime className="w-full" />
            </Form.Item>
            <Form.Item
              name="arrival_datetime"
              label="Arrival Time"
              rules={[{ required: true, message: 'Please select the arrival time!' }]}
            >
              <DatePicker showTime className="w-full" />
            </Form.Item>
            <Form.Item name="transport_carrier" label="Transport Company">
              <Input placeholder="e.g., JR East" />
            </Form.Item>
            <Form.Item name="transport_number" label="Transport Number">
              <Input placeholder="e.g., Train 123" />
            </Form.Item>
          </>
        );

      case ItineraryItemType.CAR_RENTAL:
        return (
          <>
            <Form.Item
              name="pickup_location"
              label="Pickup Location"
              rules={[{ required: true, message: 'Please input the pickup location!' }]}
            >
              <Input placeholder="e.g., Tokyo Airport" />
            </Form.Item>
            <Form.Item name="dropoff_location" label="Dropoff Location">
              <Input placeholder="e.g., Tokyo Station" />
            </Form.Item>
            <Form.Item
              name="pickup_datetime"
              label="Pickup Time"
              rules={[{ required: true, message: 'Please select the pickup time!' }]}
            >
              <DatePicker showTime className="w-full" />
            </Form.Item>
            <Form.Item
              name="dropoff_datetime"
              label="Dropoff Time"
              rules={[{ required: true, message: 'Please select the dropoff time!' }]}
            >
              <DatePicker showTime className="w-full" />
            </Form.Item>
          </>
        );

      case ItineraryItemType.ACCOMMODATION:
        return (
          <>
            <Form.Item
              name="address"
              label="Address"
              rules={[{ required: true, message: 'Please input the address!' }]}
            >
              <Input placeholder="e.g., 123 Hotel Street, Tokyo" />
            </Form.Item>
            <Form.Item
              name="check_in_datetime"
              label="Check-in Time"
              rules={[{ required: true, message: 'Please select the check-in time!' }]}
            >
              <DatePicker showTime className="w-full" />
            </Form.Item>
            <Form.Item
              name="check_out_datetime"
              label="Check-out Time"
              rules={[{ required: true, message: 'Please select the check-out time!' }]}
            >
              <DatePicker showTime className="w-full" />
            </Form.Item>
          </>
        );

      case ItineraryItemType.ACTIVITY:
        return (
          <>
            <Form.Item name="description" label="Description">
              <Input.TextArea placeholder="e.g., Visit Tokyo Tower" />
            </Form.Item>
            <Form.Item name="location_name" label="Location">
              <Input placeholder="e.g., Tokyo Tower" />
            </Form.Item>
            <Form.Item
              name="start_datetime"
              label="Start Time"
              rules={[{ required: true, message: 'Please select the start time!' }]}
            >
              <DatePicker showTime className="w-full" />
            </Form.Item>
            <Form.Item name="end_datetime" label="End Time">
              <DatePicker showTime className="w-full" />
            </Form.Item>
          </>
        );

      default:
        return null;
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-8 rounded-lg shadow-md bg-white">
      <h1 className="text-3xl font-bold mb-8">
        {isCreateMode ? "Create a new itinerary item" : "Edit itinerary item"}
      </h1>

      <Form
        form={form}
        layout="vertical"
        requiredMark={true}
        onFinish={handleSubmit}
        className="space-y-6"
      >
        <Form.Item
          name="type"
          label="Type"
          rules={[{ required: true, message: 'Please select the type!' }]}
        >
          <Select
            placeholder="Select type"
            onChange={(value) => setSelectedType(value)}
            options={[
              { value: ItineraryItemType.FLIGHT, label: 'Flight' },
              { value: ItineraryItemType.GROUND_TRANSPORTATION, label: 'Ground Transportation' },
              { value: ItineraryItemType.CAR_RENTAL, label: 'Car Rental' },
              { value: ItineraryItemType.ACCOMMODATION, label: 'Accommodation' },
              { value: ItineraryItemType.ACTIVITY, label: 'Activity' },
            ]}
          />
        </Form.Item>

        {renderTypeSpecificFields()}

        <Form.Item name="booking_reference" label="Booking Reference">
          <Input placeholder="e.g., ABC123" />
        </Form.Item>

        <Form.Item name="booking_url" label="Booking URL">
          <Input placeholder="e.g., https://booking.com/..." />
        </Form.Item>

        <Form.Item name="notes" label="Notes">
          <Input.TextArea placeholder="Additional notes..." />
        </Form.Item>

        <Button
          className="w-full"
          type="primary"
          htmlType="submit"
          loading={submitting}
        >
          Save
        </Button>
      </Form>
    </div>
  );
};