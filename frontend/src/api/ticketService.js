// src/api/ticketService.js
import { authAPI } from "./base";

const ticketService = {
  getAll: () => authAPI.get("tickets/"),
  getById: (id) => authAPI.get(`tickets/${id}/`),
};

export default ticketService;
