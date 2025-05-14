import jwt from "jsonwebtoken";
import User from "../models/userSchema.js";

export const authenticate = async (req, res, next) => {
  const authToken = req.headers.authorization;
  console.log(authToken);

  if (!authToken || !authToken.startsWith("Bearer ")) {
    console.log("no token found");
    return res.status(401).json({ success: false, message: "Unauthorized" });
  }

  try {
    const token = authToken.split(" ")[1];
    console.log("Incoming bearer:", authToken);
    const decoded = jwt.verify(token, process.env.JWT_TOKEN);
    console.log("Decoded JWT payload:", decoded);

    req.userId = decoded.userId;
    console.log("user id found: ", decoded);
    next();
  } catch (error) {
    if (error.name === "TokenExpiredError") {
      console.log("Token expired");
      return res
        .status(401)
        .json({ success: false, message: "Session Expired" });
    }
    return res.status(401).json({ success: false, message: "Unauthorized" });
  }
};

export const restrict = (roles) => async (req, res, next) => {
  const userId = req.userId;
  const user = await User.findById(userId);

  if (!user) {
    return res.status(401).json({ success: false, message: "Unauthorized" });
  }

  console.log(user, "user 1");

  if (!roles.includes(user.role)) {
    return res.status(401).json({ success: false, message: "Unauthorized" });
  }

  next();
};
