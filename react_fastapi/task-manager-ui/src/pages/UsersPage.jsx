import { useEffect, useState } from "react";
import { usersApi } from "../api/usersApi";

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ full_name: "", email: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadUsers() {
    setLoading(true);
    setError("");
    try {
      const res = await usersApi.list(1, 100);
      setUsers(res.data);
    } catch (e) {
      setError(e?.response?.data?.detail || "Failed to load users");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadUsers();
  }, []);

  async function onCreate(e) {
    e.preventDefault();
    setError("");
    try {
      await usersApi.create(form);
      setForm({ full_name: "", email: "" });
      await loadUsers();
    } catch (e) {
      setError(e?.response?.data?.detail || "Failed to create user");
    }
  }

  return (
    <div className="page">
      <h2>Users</h2>

      <form className="row" onSubmit={onCreate}>
        <input
          placeholder="Full name"
          value={form.full_name}
          onChange={(e) => setForm({ ...form, full_name: e.target.value })}
          required
        />
        <input
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          required
        />
        <button type="submit">Create</button>
      </form>

      {error ? <p className="error">{error}</p> : null}
      {loading ? <p>Loading...</p> : null}

      <table className="table">
        <thead>
          <tr>
            <th>ID</th><th>Name</th><th>Email</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.full_name}</td>
              <td>{u.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
