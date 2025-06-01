import React from "react";

export interface ErrorViewProps {
    icon: string;
    title: string;
    details: string;
    children?: React.ReactNode
}

export const ErrorView: React.FC<ErrorViewProps> = (props: ErrorViewProps) => {
    const { icon, title, details, children } = props;
    return (
        <div className="w-full max-w-6xl mx-auto p-6">
            <div className="text-center py-24 bg-white rounded-2xl shadow-sm border border-gray-100">
                <div className="max-w-md mx-auto">
                    <div className="text-6xl mb-6">{icon}</div>
                    <h3 className="text-xl font-semibold text-gray-700 mb-2">{title}</h3>
                    <p className="text-gray-500">{details}</p>
                    {children}
                </div>
            </div>
        </div>
    );
}