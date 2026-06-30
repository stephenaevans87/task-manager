import { useEffect, useState } from "react";
import "./App.css";
import TaskCard from "./components/TaskCard";

function App() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchTasks() {
      try {
        const response = await fetch("/api/tasks", {
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Failed to fetch tasks.");
        }

        const data = await response.json();

        setTasks(data.data || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchTasks();
  }, []);

  return (
    <main className="app">
      <header className="app-header">
        <h1>React Task Manager</h1>
        <p>Tasks loaded from the Flask REST API.</p>
      </header>

      {loading && <p className="status-message">Loading tasks...</p>}

      {error && <p className="error-message">{error}</p>}

      {!loading && !error && tasks.length === 0 && (
        <p className="status-message">No tasks found.</p>
      )}

      {!loading && !error && tasks.length > 0 && (
        <section className="task-list">
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}
        </section>
      )}
    </main>
  );
}

export default App;