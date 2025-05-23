import { useState } from 'react';
import { Dayjs } from 'dayjs';
import { Button, DatePicker, Form, Input, message } from 'antd';
import { axiosInstance } from '../api/axiosInstance';

export const CreateTrip = () => {
  const [tripName, setTripName] = useState('');
  const [destination, setDestination] = useState('');
  const [startDate, setStartDate] = useState<Dayjs | null>(null);
  const [endDate, setEndDate] = useState<Dayjs | null>(null);

  const handleDateRangeChange = (dates: [Dayjs | null, Dayjs | null] | null) => {
    if (dates && dates[0]) {
      setStartDate(dates[0]);
    }
    if (dates && dates[1]) {
      setEndDate(dates[1]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axiosInstance.post('/trips', {
        name: tripName,
        description: destination,
        start_date: startDate?.toISOString(),
        end_date: endDate?.toISOString(),
        created_by_user_id: 'user-id-here', // Replace with actual user ID logic
      });
      message.success('Trip created successfully!');
    } catch (error) {
      console.error(error);
      message.error('Failed to create trip. Please try again.');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white">
      <div className="w-full max-w-xl p-8 rounded-lg shadow-md bg-white">
        <h1 className="text-3xl font-bold mb-8">Create a new trip</h1>
        <Form layout='vertical' requiredMark={true} onFinish={handleSubmit} className="space-y-6">
            <Form.Item name="tripName" label="Trip name">
                <Input placeholder="e.g., Tokyo Trip 2025" value={tripName} required={true} onChange={e => setTripName(e.target.value)} />
            </Form.Item>

            <Form.Item name="destination" label="Destination">
                <Input placeholder="e.g., Tokyo" required={true} value={destination} onChange={e => setDestination(e.target.value)} />
            </Form.Item>

            <Form.Item name="dateRange" label="Dates">
                <DatePicker.RangePicker className="w-full" value={[startDate, endDate]} onChange={handleDateRangeChange} />
            </Form.Item>

            <Button className="w-full" type="primary" htmlType="submit">Create trip</Button>
          </Form>
      </div>
    </div>
  );
};
