import axiosClient from "./axiosClient";

export const usersApi = {
  create: (payload) => axiosClient.post("/users", payload),
  list: (page = 1, size = 50) => axiosClient.get(`/users?page=${page}&size=${size}`),
};
