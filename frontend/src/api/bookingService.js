// src/api/bookingService.js
import { authAPI } from "./base";

const bookingService = {
  getAll: () => authAPI.get("bookings/"),
  create: (data) => authAPI.post("bookings/create/", data),
  cancel: (id) => authAPI.delete(`bookings/${id}/cancel/`),
};

export default bookingService;
