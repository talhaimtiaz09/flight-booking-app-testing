import axios from "axios";
import React, { useState, useEffect } from "react";
import { BACKENDURL } from "../Config/Config";
import { toast } from "react-toastify"; // make sure toast is imported

const SearchFlight = () => {
  const [searchParams, setSearchParams] = useState({
    from: "",
    to: "",
    departDate: "",
  });
  const [results, setResults] = useState([]);
  const [allFlights, setAllFlights] = useState([]);

  const handleChange = (e) =>
    setSearchParams({ ...searchParams, [e.target.name]: e.target.value });

  const handleSearch = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post(
        `${BACKENDURL}/api/v1/flights/search`,
        searchParams
      );

      const data = res.data;

      if (res.status == 200) {
        setResults(data);
        toast.success("Flights fetched successfully!");
      } else {
        setResults([]);
        toast.warn("No flights found.");
      }
    } catch (error) {
      console.error("Error fetching flights:", error);
      toast.error(
        error?.response?.data?.message ||
          "Something went wrong while searching."
      );
      setResults([]);
    }
  };

  // Fetch all flights on mount
  useEffect(() => {
    const fetchFlights = async () => {
      try {
        const res = await axios.get(`${BACKENDURL}/api/v1/flights/all`);
        console.log(res);
        if (res.status === 200) setAllFlights(res.data);
      } catch (err) {
        console.error("Failed to fetch all flights:", err);
      }
    };
    fetchFlights();
  }, []);

  return (
    <div className="max-w-6xl mx-auto mt-6">
      <form
        onSubmit={handleSearch}
        className="flex flex-wrap items-center gap-4 p-4 bg-white shadow rounded-xl"
      >
        {["from", "to", "departDate"].map((field) => (
          <input
            key={field}
            name={field}
            type={field === "departDate" ? "date" : "text"}
            placeholder={field}
            value={searchParams[field]}
            onChange={handleChange}
            className="p-2 border rounded w-full sm:w-auto"
            required
          />
        ))}
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Search
        </button>
      </form>

      {results.length > 0 && (
        <div className="mt-6 grid gap-4">
          <h2 className="text-xl font-bold mb-2">Search Results</h2>
          {results.map((flight) => (
            <div
              key={flight._id}
              className="p-4 bg-white border rounded shadow-sm"
            >
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-semibold text-lg">
                    {flight.from} → {flight.to}
                  </h3>
                  <p className="text-sm text-gray-600">
                    Depart: {flight.departDate} at {flight.departTime}
                  </p>
                  <p className="text-sm text-gray-600">
                    Arrive: {flight.arriveDate} at {flight.arriveTime}
                  </p>
                </div>
                <div className="text-right">
                  <img
                    src={flight.airlineLogo}
                    alt="airline logo"
                    className="w-12 h-12 object-contain mb-2"
                  />
                  <p className="text-md font-bold">${flight.price}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* All Flights Table */}
      <div className="mt-10">
        <h2 className="text-2xl font-bold mb-4">All Flights</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border shadow rounded">
            <thead className="bg-gray-100">
              <tr>
                <th className="text-left p-3 border-b">From</th>
                <th className="text-left p-3 border-b">To</th>
                <th className="text-left p-3 border-b">Depart</th>
                <th className="text-left p-3 border-b">Arrive</th>
                <th className="text-left p-3 border-b">Airline</th>
                <th className="text-left p-3 border-b">Price</th>
              </tr>
            </thead>
            <tbody>
              {allFlights.map((flight) => (
                <tr key={flight._id} className="border-b hover:bg-gray-50">
                  <td className="p-3">{flight.from}</td>
                  <td className="p-3">{flight.to}</td>
                  <td className="p-3">
                    {flight.departDate} @ {flight.departTime}
                  </td>
                  <td className="p-3">
                    {flight.arriveDate} @ {flight.arriveTime}
                  </td>
                  <td className="p-3 flex items-center gap-2">
                    {/* <img
                      src={flight.airlineLogo}
                      alt="logo"
                      className="w-6 h-6 object-contain"
                    /> */}
                    {flight.airlineName || "N/A"}
                  </td>
                  <td className="p-3 font-semibold text-green-700">
                    ${flight.price}
                  </td>
                </tr>
              ))}
              {allFlights.length === 0 && (
                <tr>
                  <td colSpan="6" className="p-4 text-center text-gray-500">
                    No flights available.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default SearchFlight;
