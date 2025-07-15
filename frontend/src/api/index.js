// src/api/index.js
import auth from "./authService";
import user from "./userService";
import movie from "./movieService";
import booking from "./bookingService";
import ticket from "./ticketService";

const api = {
  auth,
  user,
  movie,
  booking,
  ticket,
};

export default api;
