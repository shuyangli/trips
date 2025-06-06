import { ConfigProvider } from "antd";
import { BrowserRouter, Route, Routes } from "react-router";

import "./App.css";
import { CreateTrip } from "./components/CreateTrip";
import { EditTrip } from "./components/EditTrip";
import { TripList } from "./components/TripList";
import { AuthStatusContext } from "./contexts/AuthStatusContext";
import { type AuthStatus, useAuthStatus } from "./hooks/useAuthStatus";
import { TripDetailPage } from "./components/TripDetails";
import { WebLayout } from "./components/WebLayout";
import { CreateItineraryItem } from "./components/CreateItineraryItem";

export const App = () => {
  const authStatus: AuthStatus = useAuthStatus();
  return (
    // TODO: figure out the correct locale to use for antd components..
    <BrowserRouter>
      <ConfigProvider locale={{ locale: navigator.language }}>
        <AuthStatusContext.Provider value={authStatus}>
          <Routes>
            <Route path="/" element={<WebLayout />}>
              <Route index element={<TripList />} />
              <Route path="create" element={<CreateTrip />} />
              <Route path="trip/:tripId" element={<TripDetailPage />} />
              <Route path="trip/:tripId/edit" element={<EditTrip />} />
              <Route path="trip/:tripId/createItinerary" element={<CreateItineraryItem />} />
              {/* <Route path="trip/:tripId/timeline" element={<TripTimelinePage />} /> */}
            </Route>
          </Routes>
        </AuthStatusContext.Provider>
      </ConfigProvider>
    </BrowserRouter>
  );
};
