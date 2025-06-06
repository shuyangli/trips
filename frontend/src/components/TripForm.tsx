import { useEffect, useState } from "react";
import { Dayjs } from "dayjs";
import dayjs from "dayjs";
import { Button, DatePicker, Form, Input, Select } from "antd";

export interface TripFormData {
  tripName?: string;
  destination?: string;
  dateRange?: [Dayjs, Dayjs];
  participants?: string[];
}

export interface TripFormProps {
  initialValues?: {
    name?: string;
    description?: string;
    start_date?: string;
    end_date?: string;
  };
  onSubmit: (data: TripFormData) => Promise<void>;
}

export const TripForm = ({ initialValues, onSubmit }: TripFormProps) => {
  const [form] = Form.useForm();
  const [submitting, setSubmitting] = useState(false);
  const isCreateMode = initialValues === undefined;

  useEffect(() => {
    if (initialValues) {
      const dateRange: [Dayjs, Dayjs] | undefined =
        initialValues.start_date && initialValues.end_date
          ? [dayjs(initialValues.start_date), dayjs(initialValues.end_date)]
          : undefined;

      form.setFieldsValue({
        tripName: initialValues.name,
        destination: initialValues.description,
        dateRange,
      });
    }
  }, [form, initialValues]);

  const handleSubmit = async (values: TripFormData) => {
    try {
      setSubmitting(true);
      await onSubmit(values);
    } catch (error) {
      // Error handling is done in the parent component
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-8 rounded-lg shadow-md bg-white">
      <h1 className="text-3xl font-bold mb-8">
        {isCreateMode ? "Create a new trip" : "Edit trip"}
      </h1>

      <Form
        form={form}
        layout="vertical"
        requiredMark={true}
        onFinish={handleSubmit}
        className="space-y-6"
      >
        <Form.Item<TripFormData>
          name="tripName"
          label="Trip name"
          rules={[{ required: true, message: 'Please input the trip name!' }]}
          validateTrigger={"onBlur"}
        >
          <Input placeholder="e.g., Tokyo Trip 2025" />
        </Form.Item>

        <Form.Item<TripFormData>
          name="destination"
          label="Destination"
          rules={[{ required: true, message: 'Please input the destination!' }]}
          validateTrigger={"onBlur"}
        >
          <Input placeholder="e.g., Tokyo" />
        </Form.Item>

        <Form.Item<TripFormData>
          name="dateRange"
          label="Dates"
          rules={[{ required: true, message: 'Please select the date range!' }]}
          validateTrigger={"onBlur"}
        >
          <DatePicker.RangePicker className="w-full" />
        </Form.Item>

        <Form.Item<TripFormData>
          name="participants"
          label={"Invite participants"}
        >
          <Select
            mode="tags"
            placeholder="Enter email addresses (press Enter or comma to add)"
            style={{ width: '100%' }}
            tokenSeparators={[',', ' ']}
            notFoundContent={null}
            filterOption={false}
          />
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