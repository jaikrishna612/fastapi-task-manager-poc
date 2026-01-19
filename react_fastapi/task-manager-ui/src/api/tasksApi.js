import axiosClient from "./axiosClient";

export const tasksApi = {
  create: (payload) => axiosClient.post("/tasks", payload),
  list: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return axiosClient.get(`/tasks?${query}`);
  },
  transition: (id, status) => axiosClient.post(`/tasks/${id}/transition`, { status }),
  remove: (id) => axiosClient.delete(`/tasks/${id}`),
};
