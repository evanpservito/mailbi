"use client";
import React from "react";
import { fetchAuthSession } from "@aws-amplify/auth";

const Overview = () => {
  const getIdToken = async () => {
    try {
      const session = await fetchAuthSession();
      const idToken = session.tokens?.idToken?.toString();

      console.log("ID Token:", idToken);
      return idToken;
    } catch (error) {
      console.error("Auth error:", error);
    }
  };

  const testCall = () => {
    fetch("")
      .then((res) => res.json())
      .then((data) => console.log(data))
      .catch((err) => console.error("Fetch error:", err));
  };
  return (
    <div>
      <p>Overview</p>
      <button className="border-2 bg-amber-500" onClick={() => getIdToken()}>
        Test Token Call
      </button>
      <button className="border-2 bg-amber-500" onClick={() => testCall()}>
        Test Call
      </button>
    </div>
  );
};

export default Overview;
