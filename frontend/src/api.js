// const API_URL = "http://localhost:8000";

// function headers() {
//   const token = localStorage.getItem("token");
//   return {
//     "Content-Type": "application/json",
//     ...(token ? { Authorization: `Bearer ${token}` } : {}),
//   };
// }

// export default {
//   async get(path) {
//     const res = await fetch(API_URL + path, {
//       headers: headers(),
//     });
//     if (!res.ok) throw await res.json();
//     return res.json();
//   },

//   async post(path, body) {
//     const res = await fetch(API_URL + path, {
//       method: "POST",
//       headers: headers(),
//       body: JSON.stringify(body),
//     });
//     if (!res.ok) throw await res.json();
//     return res.json();
//   },
// };

import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
