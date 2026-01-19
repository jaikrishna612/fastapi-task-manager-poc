import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import UsersPage from "../pages/UsersPage";
import TasksPage from "../pages/TasksPage";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <div className="nav">
        <NavLink to="/users">Users</NavLink>
        <NavLink to="/tasks">Tasks</NavLink>
      </div>

      <Routes>
        <Route path="/" element={<UsersPage />} />
        <Route path="/users" element={<UsersPage />} />
        <Route path="/tasks" element={<TasksPage />} />
      </Routes>
    </BrowserRouter>
  );
}
