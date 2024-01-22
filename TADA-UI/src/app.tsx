import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";

import LoginPage from './pages/loginPage'
import EyAuthentication from './components/authentication/eyAuthentication'
import WithAppInsights from'./services/azure/appInsights/appInsights'
 function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/TADA/*" element={<EyAuthentication />} />
      </Routes>
    </Router>
  );
}
export default WithAppInsights(App);


