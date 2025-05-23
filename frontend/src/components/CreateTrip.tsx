import { useState } from "react";
import { Dayjs } from "dayjs";
import { Button, DatePicker, Form, Input, message } from "antd";
import { axiosInstance } from "../api/axiosInstance";

interface CreateTripRequestField {
    tripName?: string;
    destination?: string;
    dateRange?: [Dayjs, Dayjs];
}

export const CreateTrip = () => {

  const handleSubmit = (e: CreateTripRequestField) => {
    const {tripName, destination, dateRange} = e;
    const [startDate, endDate] = dateRange ?? [];
      axiosInstance.post("/trips", {
        name: tripName,
        description: destination,
        start_date: startDate?.toISOString(),
        end_date: endDate?.toISOString(),
        created_by_user_id: "0579c7bf-76e6-4783-b889-c6657157c09c", // Replace with actual user ID logic
      }).then(() => {
        message.success("Trip created successfully!");
      }).catch((error) => {
        console.error(error);
        message.error("Failed to create trip. Please try again.");
      })
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white">
      <div className="w-full max-w-xl p-8 rounded-lg shadow-md bg-white">
        <h1 className="text-3xl font-bold mb-8">Create a new trip</h1>
        <Form layout="vertical" requiredMark={true} onFinish={handleSubmit} className="space-y-6">
            <Form.Item<CreateTripRequestField> name="tripName" label="Trip name" required={true} validateTrigger={"onBlur"}>
                <Input placeholder="e.g., Tokyo Trip 2025" />
            </Form.Item>

            <Form.Item<CreateTripRequestField> name="destination" label="Destination" required={true} validateTrigger={"onBlur"}>
                <Input placeholder="e.g., Tokyo" />
            </Form.Item>

            <Form.Item<CreateTripRequestField> name="dateRange" label="Dates" required={true}>
                <DatePicker.RangePicker className="w-full" />
            </Form.Item>

            <Button className="w-full" type="primary" htmlType="submit">Create trip</Button>
          </Form>
      </div>
    </div>
  );
};
