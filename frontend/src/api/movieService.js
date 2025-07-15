// src/api/movieService.js
import { publicAPI } from "./base";

const movieService = {
  getAll: () => publicAPI.get("movies/"),
  getBySlug: (slug) => publicAPI.get(`movies/${slug}/`),
};

export default movieService;
