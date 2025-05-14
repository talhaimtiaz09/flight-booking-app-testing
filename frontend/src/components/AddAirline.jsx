import { useState } from "react";
import { toast } from "react-toastify";
import React from "react";
import { BACKENDURL } from "../Config/Config";
import axios from "axios";

const AddAirline = () => {
  const [airlineName, setAirlineName] = useState("");
  const [airlineLogo, setAirlineLogo] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const airlineData = {
      airlineLogo: airlineLogo,
      airlineName: airlineName,
    };

    try {
      const res = await axios.post(
        `${BACKENDURL}/api/v1/flights/addAirline`,
        airlineData
      );

      if (res.status === 201) {
        toast.success("✅ Airline added successfully!");
        setAirlineName("");
        setAirlineLogo("");
      } else {
        toast.error(
          `⚠️ Failed to add airline: ${res.data?.message || "Unknown error"}`
        );
      }
    } catch (error) {
      const message =
        error.response?.data?.message ||
        error.message ||
        "Something went wrong.";
      toast.error(`❌ Error: ${message}`);
      console.error("Add Airline Error:", error);
    }
  };

  return (
    <div className="max-w-md p-6 mx-auto mt-6 bg-white shadow rounded-xl">
      <h2 className="text-xl font-semibold mb-4">Add Airline</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          className="w-full p-2 border rounded"
          placeholder="Airline Name"
          value={airlineName}
          onChange={(e) => setAirlineName(e.target.value)}
          required
        />
        <input
          className="w-full p-2 border rounded"
          placeholder="Airline Logo URL"
          value={airlineLogo}
          onChange={(e) => setAirlineLogo(e.target.value)}
          required
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
        >
          Add Airline
        </button>
      </form>
    </div>
  );
};

export default AddAirline;
