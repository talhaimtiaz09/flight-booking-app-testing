import React, { useState } from "react";
import SearchFlight from "../components/SearchFlight";
import AddAirline from "../components/AddAirline";
import Addflight from "../components/Addflight";

const FlightManagement = () => {
  const [activeTab, setActiveTab] = useState("search");

  const renderSection = () => {
    switch (activeTab) {
      case "search":
        return <SearchFlight />;
      case "airline":
        return <AddAirline />;
      case "flight":
        return <Addflight />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-blue-900 mb-6">
          Flight Management Dashboard
        </h1>

        {/* Tabs */}
        <div className="flex justify-center gap-4 mb-6">
          <button
            className={`px-4 py-2 rounded-full font-medium ${
              activeTab === "search"
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-800"
            }`}
            onClick={() => setActiveTab("search")}
          >
            Search Flights
          </button>
          <button
            className={`px-4 py-2 rounded-full font-medium ${
              activeTab === "airline"
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-800"
            }`}
            onClick={() => setActiveTab("airline")}
          >
            Add Airline
          </button>
          <button
            className={`px-4 py-2 rounded-full font-medium ${
              activeTab === "flight"
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-800"
            }`}
            onClick={() => setActiveTab("flight")}
          >
            Add Flight
          </button>
        </div>

        {/* Active Section */}
        <section className="bg-white p-6 rounded-2xl shadow-md">
          {renderSection()}
        </section>
      </div>
    </div>
  );
};

export default FlightManagement;
