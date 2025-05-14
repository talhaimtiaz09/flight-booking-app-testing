import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import { BACKENDURL } from "../Config/Config";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { TbEdit } from "react-icons/tb";
import uploadImageToCloudinary from "../utils/uploadImageToCloudinary";
import { authContext } from "../context/authContext";
import { toast } from "react-toastify";

const Profile = () => {
  const { dispatch } = useContext(authContext);

  const [userData, setUserData] = useState({});
  const [tickets, setTickets] = useState([]);
  const [userName, setUserName] = useState("");
  const [profilePic, setProfilePic] = useState(null);
  const navigate = useNavigate();

  const isUserLoggedIn = localStorage.getItem("isUserLoggedIn") === "true"; // Check login status

  useEffect(() => {
    if (isUserLoggedIn) {
      const token = localStorage.getItem("token");

      axios
        .get(BACKENDURL + "/api/v1/auth/getUser", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((response) => {
          setUserData(response.data.user);
          setTickets(response.data.tickets);
          setUserName(response.data.user.name);
        })
        .catch((error) => {
          console.error("Error fetching user data:", error);
        });
    } else {
      navigate("/login"); // Redirect if not logged in
    }
  }, [navigate, isUserLoggedIn]);

  const handleLogout = () => {
    dispatch({ type: "LOGOUT" });
    toast.success("Logged out successfully");
    navigate("/login");
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (file) {
      try {
        // Upload image to Cloudinary
        const imageData = await uploadImageToCloudinary(file);
        setProfilePic(imageData.secure_url); // Set profile picture URL
      } catch (error) {
        console.error("Error uploading image:", error);
      }
    }
  };

  const handleProfileUpdate = async () => {
    try {
      const token = localStorage.getItem("token");
      if (token === null) {
        navigate("/login");
      } else {
        let updatedData = { name: userName };

        if (profilePic) {
          const imageData = await uploadImageToCloudinary(profilePic);
          updatedData.profilePic = imageData.secure_url;
        }

        const response = await axios.put(
          BACKENDURL + "/api/v1/auth/updateUser",
          updatedData,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        toast.success("Profile updated successfully");
        setUserData(response.data.user);
      }
    } catch (error) {
      console.error("Error updating profile:", error);
    }
  };

  return (
    <div className="px-[30px] md:px-[30px]">
      <div className="max-w-[800px] mx-auto">
        <h1 className="mt-5 text-3xl font-semibold">Profile</h1>

        {isUserLoggedIn ? (
          <div className="my-5">
            {/* Profile Picture */}
            <div className="w-[100px] h-[100px] rounded-full overflow-hidden relative">
              <div className="w-full h-full object-cover absolute flex justify-center items-center bg-black/40 opacity-0 hover:opacity-100 cursor-pointer">
                <label htmlFor="profile-pic-upload">
                  <TbEdit className="text-white text-[40px] cursor-pointer" />
                </label>
                <input
                  id="profile-pic-upload"
                  type="file"
                  accept="image/*"
                  style={{ display: "none" }}
                  onChange={handleImageUpload}
                />
              </div>
              <img
                src={profilePic || userData.profilePic}
                alt="Profile"
                className="w-full h-full object-cover"
              />
            </div>

            {/* User Name */}
            <div className="mt-5">
              <div className="flex gap-2 items-center">
                <p className="text-lg font-medium">User Name: </p>
                <input
                  type="text"
                  value={userName}
                  className="outline-none border-b-2 focus:border-blue-500 p-1"
                  onChange={(e) => setUserName(e.target.value)}
                />
              </div>
              <p className="mt-2">User Email: {userData.email}</p>
            </div>

            {/* Update Profile Button */}
            <div className="flex gap-4 mt-4">
              <button
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition duration-200"
                onClick={handleProfileUpdate}
              >
                Update Profile
              </button>

              {/* Logout Button */}
              <button
                className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition duration-200"
                onClick={handleLogout}
              >
                Logout
              </button>
            </div>

            {/* Tickets Table */}
            {tickets.length > 0 ? (
              <div className="mt-5">
                <table className="table-auto w-full">
                  <thead>
                    <tr className="border-b">
                      <th className="p-3">Ticket ID</th>
                      <th className="p-3">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tickets.map((ticket) => (
                      <tr key={ticket._id} className="border-b">
                        <td className="text-center">{ticket.uid}</td>
                        <td className="text-center">
                          <Link
                            to={`/ticket/${ticket.uid}`}
                            className="text-blue-500 underline"
                          >
                            Go to Ticket
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="mt-5">No tickets found</p>
            )}
          </div>
        ) : (
          <div className="my-5 text-center">
            <h2 className="text-xl font-medium mb-4">
              Please{" "}
              <Link to="/login" className="text-blue-600">
                Sign In
              </Link>{" "}
              or{" "}
              <Link to="/signup" className="text-blue-600">
                Register
              </Link>{" "}
              to view your profile.
            </h2>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;
