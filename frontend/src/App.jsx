import { useEffect, useState } from "react";

function App() {
  const [backendMessage, setBackendMessage] = useState("Connecting...");
  const [connectionStatus, setConnectionStatus] = useState("Checking");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Backend request failed");
        }
        return response.json();
      })
      .then((data) => {
        setBackendMessage(data.message);
        setConnectionStatus("Connected");
      })
      .catch((error) => {
        console.error("Backend connection error:", error);
        setBackendMessage("Unable to connect to backend.");
        setConnectionStatus("Disconnected");
      });
  }, []);

  return (
    <div>
      <h1>School Management Platform</h1>

      <h2>Frontend–Backend Connection Test</h2>

      <p>
        Connection Status: <strong>{connectionStatus}</strong>
      </p>

      <p>Backend Response: {backendMessage}</p>
    </div>
  );
}

export default App;