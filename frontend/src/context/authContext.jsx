import React, { createContext, useEffect, useReducer } from "react";

// Utility function to safely get parsed localStorage value
const getLocalStorageItem = (key) => {
  try {
    const item = localStorage.getItem(key);
    return item && item !== "undefined" ? JSON.parse(item) : null;
  } catch (error) {
    return null;
  }
};

// Initial state from localStorage
const initialState = {
  user: getLocalStorageItem("user"),
  token: localStorage.getItem("token") || null,
  isAdmin: getLocalStorageItem("isAdmin"),
  isUserLoggedIn: !!localStorage.getItem("token"),
};

export const authContext = createContext(initialState);

const authReducer = (state, action) => {
  switch (action.type) {
    case "LOGIN_START":
      return {
        user: null,
        token: null,
        isAdmin: null,
        isUserLoggedIn: false,
      };

    case "LOGIN_SUCCESS":
      return {
        user: action.payload.user,
        token: action.payload.token,
        isAdmin: action.payload.isAdmin,
        isUserLoggedIn: true,
      };

    case "LOGOUT":
      // Clear localStorage on logout
      localStorage.removeItem("user");
      localStorage.removeItem("token");
      localStorage.removeItem("isAdmin");
      localStorage.removeItem("isUserLoggedIn");
      return {
        user: null,
        token: null,
        isAdmin: null,
        isUserLoggedIn: false,
      };

    default:
      return state;
  }
};

export const AuthContextProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Sync to localStorage on state change
  useEffect(() => {
    if (state.user) localStorage.setItem("user", JSON.stringify(state.user));
    if (state.token) localStorage.setItem("token", state.token);
    if (state.isAdmin !== null) {
      localStorage.setItem("isAdmin", JSON.stringify(state.isAdmin));
    }
    localStorage.setItem(
      "isUserLoggedIn",
      JSON.stringify(state.isUserLoggedIn)
    );
  }, [state]);

  return (
    <authContext.Provider
      value={{
        user: state.user,
        token: state.token,
        isAdmin: state.isAdmin,
        isUserLoggedIn: state.isUserLoggedIn,
        dispatch,
      }}
    >
      {children}
    </authContext.Provider>
  );
};
