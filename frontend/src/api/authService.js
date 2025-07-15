import { publicAPI } from "./base";

const authService = {
  register: (formData) =>
    publicAPI.post("users/register/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    }),

  login: (data) => publicAPI.post("users/login/", data),
  refresh: (data) => publicAPI.post("users/token/refresh/", data),
  logout: () => {
    localStorage.clear();
    window.location.href = "/login";
  },
};

export default authService;
