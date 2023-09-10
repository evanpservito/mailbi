import TrackingLog from "./pages/TrackingLog/TrackingLog";
import { ChakraProvider } from "@chakra-ui/react";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home/Home";
import Login from "./pages/Login/Login";
import PackageStatus from "./pages/PackageStatus/PackageStatus";
import Footer from "./components/Footer/Footer";
import "./App.css";
import { AuthContextProvider } from "./context/AuthContext";
import Protected from "./components/Protected";
import { Navbar } from "./components/Navbar/Navbar";
import CustomMessage from "./pages/CustomMessage/CustomMessage";

function App() {
  return (
    <div className="App">
      <AuthContextProvider>
        <ChakraProvider>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route
              path="/tracking-log"
              element={
                <Protected>
                  <Navbar />
                  <TrackingLog />
                  <Footer />
                </Protected>
              }
            />
            <Route
              path="/package-status"
              element={
                <Protected>
                  <Navbar />
                  <PackageStatus />
                  <Footer />
                </Protected>
              }
            />
            <Route
              path="/custom-message"
              element={
                <Protected>
                  <Navbar />
                  <CustomMessage />
                  <Footer />
                </Protected>
              }
            />
          </Routes>
        </ChakraProvider>
      </AuthContextProvider>
    </div>
  );
}

export default App;
