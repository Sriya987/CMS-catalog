import { useEffect, useState } from "react";
import api from "../api";

export default function Programs() {
  const [programs, setPrograms] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/cms/programs")
      .then((data) => setPrograms(data))
      .catch(() => setError("Failed to load programs"));
  }, []);

  return (
    <div className="container">
      <h1>Programs (CMS)</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {programs.length === 0 ? (
        <p>No programs created yet.</p>
      ) : (
        <table width="100%" cellPadding="8">
          <thead>
            <tr style={{ textAlign: "left" }}>
              <th>Title</th>
              <th>Status</th>
              <th>Primary Language</th>
            </tr>
          </thead>
          <tbody>
            {programs.map((p) => (
              <tr key={p.id}>
                <td><b>{p.title}</b></td>
                <td>{p.status}</td>
                <td>{p.language_primary}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
