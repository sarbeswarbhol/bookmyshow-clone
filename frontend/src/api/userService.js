// src/api/userService.js
import { authAPI } from "./base";

const userService = {
  getProfile: () => authAPI.get("users/profile/"),
  updateProfile: (data) => authAPI.put("users/profile/", data),
};

export default userService;
