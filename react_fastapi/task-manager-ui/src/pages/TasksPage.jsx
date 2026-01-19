// src/pages/TasksPage.jsx
import { useEffect, useState } from "react";
import { tasksApi } from "../api/tasksApi";
import { usersApi } from "../api/usersApi";

const STATUSES = ["TODO", "IN_PROGRESS", "DONE"];

export default function TasksPage() {
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);

  const [form, setForm] = useState({
    title: "",
    description: "",
    assignee_user_id: "",
  });

  const [filters, setFilters] = useState({
    status: "",
    assignee_user_id: "",
    q: "",
  });

  const [error, setError] = useState("");

  function clean(obj) {
    const out = {};
    for (const [k, v] of Object.entries(obj)) {
      if (v !== "" && v !== null && v !== undefined) out[k] = v;
    }
    return out;
  }

  function parseApiError(e, fallback = "Request failed") {
    const detail = e?.response?.data?.detail;

    // FastAPI validation errors (422) often come like:
    // detail: [{ loc: [...], msg: "...", type: "...", ... }]
    if (Array.isArray(detail) && detail.length > 0) {
      const first = detail[0] || {};
      const loc = Array.isArray(first.loc) ? first.loc.join(" → ") : "";
      const msg = first.msg || fallback;
      return loc ? `${loc}: ${msg}` : msg;
    }

    if (typeof detail === "string") return detail;

    // Axios fallback message
    if (typeof e?.message === "string") return e.message;

    return fallback;
  }

  async function loadAll() {
    setError("");
    try {
      const query = clean(filters);

      // Convert assignee filter to number if present (prevents 422 in strict backends)
      if (query.assignee_user_id) {
        query.assignee_user_id = Number(query.assignee_user_id);
      }

      const [tRes, uRes] = await Promise.all([
        tasksApi.list({ page: 1, size: 100, ...query }),
        usersApi.list(1, 100),
      ]);

      setTasks(tRes.data);
      setUsers(uRes.data);
    } catch (e) {
      setError(parseApiError(e, "Failed to load tasks/users"));
    }
  }

  useEffect(() => {
    loadAll();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function onCreate(e) {
    e.preventDefault();
    setError("");

    try {
      await tasksApi.create({
        title: form.title,
        description: form.description,
        // IMPORTANT: send null (not "") when unassigned
        assignee_user_id: form.assignee_user_id
          ? Number(form.assignee_user_id)
          : null,
      });

      setForm({ title: "", description: "", assignee_user_id: "" });
      await loadAll();
    } catch (e) {
      setError(parseApiError(e, "Failed to create task"));
    }
  }

  async function onTransition(id, status) {
    setError("");
    try {
      await tasksApi.transition(id, status);
      await loadAll();
    } catch (e) {
      setError(parseApiError(e, "Transition failed"));
    }
  }

  async function onDelete(id) {
    setError("");
    try {
      await tasksApi.remove(id);
      await loadAll();
    } catch (e) {
      setError(parseApiError(e, "Delete failed"));
    }
  }

  return (
    <div className="page">
      <h2>Tasks</h2>

      <form className="row" onSubmit={onCreate}>
        <input
          placeholder="Title"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          required
        />
        <input
          placeholder="Description"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          required
        />
        <select
          value={form.assignee_user_id}
          onChange={(e) => setForm({ ...form, assignee_user_id: e.target.value })}
        >
          <option value="">Unassigned</option>
          {users.map((u) => (
            <option key={u.id} value={u.id}>
              {u.full_name} (#{u.id})
            </option>
          ))}
        </select>
        <button type="submit">Create</button>
      </form>

      <div className="row" style={{ marginTop: 12 }}>
        <input
          placeholder="Search (q)"
          value={filters.q}
          onChange={(e) => setFilters({ ...filters, q: e.target.value })}
        />
        <select
          value={filters.status}
          onChange={(e) => setFilters({ ...filters, status: e.target.value })}
        >
          <option value="">All Status</option>
          {STATUSES.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <select
          value={filters.assignee_user_id}
          onChange={(e) => setFilters({ ...filters, assignee_user_id: e.target.value })}
        >
          <option value="">All Assignees</option>
          {users.map((u) => (
            <option key={u.id} value={u.id}>
              {u.full_name} (#{u.id})
            </option>
          ))}
        </select>
        <button type="button" onClick={loadAll}>
          Apply Filters
        </button>
      </div>

      {error ? <p className="error">{error}</p> : null}

      <table className="table" style={{ marginTop: 12 }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Status</th>
            <th>Assignee</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((t) => (
            <tr key={t.id}>
              <td>{t.id}</td>
              <td>{t.title}</td>
              <td>{t.status}</td>
              <td>{t.assignee_user_id ?? "-"}</td>
              <td className="actions">
                {STATUSES.map((s) => (
                  <button
                    key={s}
                    onClick={() => onTransition(t.id, s)}
                    disabled={t.status === s}
                    type="button"
                  >
                    {s}
                  </button>
                ))}
                <button type="button" onClick={() => onDelete(t.id)}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
          {tasks.length === 0 ? (
            <tr>
              <td colSpan="5" style={{ textAlign: "center", padding: 12 }}>
                No tasks found
              </td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </div>
  );
}
