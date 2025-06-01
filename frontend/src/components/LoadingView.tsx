import { Spin } from "antd";

export interface LoadingViewProps {
    details: string;
}

export const LoadingView = ({ details }: LoadingViewProps) => {
    return (
    <div className="w-full max-w-6xl mx-auto p-6">
        <div className="flex flex-col items-center justify-center py-24">
        <Spin size="large" />
        <p className="mt-6 text-gray-600 text-lg">{details}</p>
        </div>
    </div>
    );
}