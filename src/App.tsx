import TrackingLog from "./pages/TrackingLog/TrackingLog";
import { ChakraProvider } from "@chakra-ui/react";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home/Home";
import Login from "./pages/Login/Login";
import Footer from "./components/Footer/Footer";
import "./App.css";
import { AuthContextProvider } from "./context/AuthContext";
import Protected from "./components/Protected";

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
                  <TrackingLog />
                </Protected>
              }
            />
          </Routes>
          <Footer />
        </ChakraProvider>
      </AuthContextProvider>
    </div>
  );
}

export default App;
