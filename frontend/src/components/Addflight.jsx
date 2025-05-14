import { useEffect, useState } from "react";
import { toast } from "react-toastify";

import React from "react";
import { BACKENDURL } from "../Config/Config";
import axios from "axios";

const Addflight = () => {
  const [airlines, setAirlines] = useState([]);
  const [form, setForm] = useState({
    from: "",
    to: "",
    departDate: "",
    arriveDate: "",
    departTime: "",
    arriveTime: "",
    price: "",
    airlineUid: "",
  });

  useEffect(() => {
    fetch(`${BACKENDURL}/api/v1/flights/getAllAirlines`)
      .then((res) => res.json())
      .then(setAirlines);
  }, []);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(form);

    try {
      const res = await axios.post(
        `${BACKENDURL}/api/v1/flights/addFlight`,
        form
      );

      const data = res.data;
      console.log("data # ", data);

      if (res.status === 200 || res.status === 201) {
        toast.success("Flight added!");
        setForm({});
      } else {
        toast.error(data.message || "Failed to add flight.");
      }
    } catch (error) {
      console.error("Error adding flight:", error);
      toast.error(
        error?.response?.data?.message ||
          "Something went wrong while adding flight."
      );
    }
  };

  return (
    <div className="max-w-xl p-6 mx-auto mt-6 bg-white shadow rounded-xl">
      <h2 className="text-xl font-semibold mb-4">Add Flight</h2>
      <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
        {[
          "from",
          "to",
          "departDate",
          "arriveDate",
          "departTime",
          "arriveTime",
          "price",
        ].map((field) => (
          <input
            key={field}
            className="p-2 border rounded"
            placeholder={field}
            name={field}
            type={
              field.includes("Date")
                ? "date"
                : field.includes("Time")
                ? "time"
                : "text"
            }
            value={form[field] || ""}
            onChange={handleChange}
            required
          />
        ))}
        <select
          name="airlineUid"
          value={form.airlineUid}
          onChange={handleChange}
          className="col-span-2 p-2 border rounded"
          required
        >
          <option value="">Select Airline</option>
          {airlines.map((a) => (
            <option key={a._id} value={a._id}>
              {a.airlineName}
            </option>
          ))}
        </select>
        <button
          type="submit"
          className="col-span-2 bg-green-600 text-white p-2 rounded hover:bg-green-700"
        >
          Add Flight
        </button>
      </form>
    </div>
  );
};

export default Addflight;
