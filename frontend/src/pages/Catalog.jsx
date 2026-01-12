import { useEffect, useState } from "react";
import api from "../api";

export default function Catalog() {
  const [programs, setPrograms] = useState([]);

  useEffect(() => {
    api.get("/catalog/programs").then((res) => {
      setPrograms(res.items);
    });
  }, []);

  return (
    <div className="container">
      <h1>Public Catalog</h1>

      <ul>
        {programs.map((p) => (
          <li key={p.id}>
            <b>{p.title}</b>
          </li>
        ))}
      </ul>
    </div>
  );
}
