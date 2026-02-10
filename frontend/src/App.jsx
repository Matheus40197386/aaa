import React, { useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [cnpj, setCnpj] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState(null);
  const [items, setItems] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [table, setTable] = useState({ columns: [], rows: [] });

  async function handleLogin(e) {
    e.preventDefault();
    const res = await axios.post(`${API_URL}/auth/login`, { cnpj, password });
    setToken(res.data.access_token);
  }

  async function loadSpreadsheets() {
    const res = await axios.get(`${API_URL}/spreadsheets`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setItems(res.data);
  }

  async function loadData(id) {
    setSelectedId(id);
    const res = await axios.get(`${API_URL}/spreadsheets/${id}/data?limit=100`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setTable(res.data);
  }

  if (!token) {
    return (
      <div style={{ padding: 24 }}>
        <h1>Portal Clientes</h1>
        <form onSubmit={handleLogin}>
          <div>
            <input placeholder="CNPJ" value={cnpj} onChange={(e) => setCnpj(e.target.value)} />
          </div>
          <div>
            <input placeholder="Senha" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          <button type="submit">Entrar</button>
        </form>
      </div>
    );
  }

  return (
    <div style={{ padding: 24 }}>
      <h1>Portal Clientes</h1>
      <button onClick={loadSpreadsheets}>Carregar Planilhas</button>
      <ul>
        {items.map((it) => (
          <li key={it.id}>
            <button onClick={() => loadData(it.id)}>{it.title}</button>
          </li>
        ))}
      </ul>

      {selectedId && (
        <div>
          <h3>Dados</h3>
          <table border="1" cellPadding="6">
            <thead>
              <tr>
                {table.columns.map((c) => (
                  <th key={c}>{c}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {table.rows.map((row, idx) => (
                <tr key={idx}>
                  {table.columns.map((c) => (
                    <td key={c}>{row[c]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
