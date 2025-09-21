"use client";
import React from "react";

const Dashboard = () => {
  const testCall = () => {
    fetch("")
      .then((res) => res.json())
      .then((data) => console.log(data))
      .catch((err) => console.error("Fetch error:", err));
  };
  return (
    <div>
      <p>Dashboard</p>
      <button className="border-2 bg-amber-500" onClick={() => testCall()}>
        Test Call
      </button>
    </div>
  );
};

export default Dashboard;
