import TrackingLog from "./components/TrackingLog/TrackingLog";
import { ChakraProvider } from "@chakra-ui/react";
import "./App.css";

function App() {
  return (
    <div className="App">
      <ChakraProvider>
        <TrackingLog />
      </ChakraProvider>
    </div>
  );
}

export default App;
