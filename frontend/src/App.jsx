import { useEffect, useState } from "react";
import "./App.css";

function getDueDateStatus(task) {
  if (task.completed && task.due_date) {
    return "completed-with-due-date";
  }

  if (!task.due_date) {
    return "no-due-date";
  }

  const today = new Date();
  const dueDate = new Date(`${task.due_date}T00:00:00`);

  today.setHours(0, 0, 0, 0);

  if (dueDate < today) {
    return "overdue";
  }

  return "upcoming";
}

function getDueDateLabel(task) {
  const status = getDueDateStatus(task);

  if (status === "no-due-date") {
    return "No due date";
  }

  if (status === "overdue") {
    return `Overdue: ${task.due_date}`;
  }

  if (status === "completed-with-due-date") {
    return `Completed — due ${task.due_date}`;
  }

  return `Due: ${task.due_date}`;
}

function App() {
  const [tasks, setTasks] = useState([]);
  const [taskText, setTaskText] = useState("");
  const [priority, setPriority] = useState("medium");
  const [category, setCategory] = useState("general");
  const [dueDate, setDueDate] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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

  useEffect(() => {
    fetchTasks();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();

    if (taskText.trim() === "") {
      setError("Task text is required.");
      return;
    }

    try {
      const response = await fetch("/api/tasks", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          task: taskText,
          priority: priority,
          category: category,
          due_date: dueDate,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to create task.");
      }

      const data = await response.json();

      setTasks([data.data, ...tasks]);
      setTaskText("");
      setPriority("medium");
      setCategory("general");
      setDueDate("");
      setError("");
    } catch (err) {
      setError(err.message);
    }
  }

  async function toggleTask(task) {
    try {
      const response = await fetch(`/api/tasks/${task.id}`, {
        method: "PATCH",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: task.text,
          priority: task.priority,
          category: task.category,
          due_date: task.due_date,
          completed: !task.completed,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to update task.");
      }

      const data = await response.json();

      setTasks(
        tasks.map((currentTask) =>
          currentTask.id === task.id ? data.data : currentTask
        )
      );
    } catch (err) {
      setError(err.message);
    }
  }

  async function deleteTask(taskId) {
    try {
      const response = await fetch(`/api/tasks/${taskId}`, {
        method: "DELETE",
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Failed to delete task.");
      }

      setTasks(tasks.filter((task) => task.id !== taskId));
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main className="app">
      <header className="app-header">
        <h1>React Task Manager</h1>
        <p>Tasks loaded from the Flask REST API.</p>
      </header>

      <form className="task-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={taskText}
          placeholder="Add a new task..."
          onChange={(event) => setTaskText(event.target.value)}
        />

        <select
          value={priority}
          onChange={(event) => setPriority(event.target.value)}
        >
          <option value="low">Low priority</option>
          <option value="medium">Medium priority</option>
          <option value="high">High priority</option>
        </select>

        <select
          value={category}
          onChange={(event) => setCategory(event.target.value)}
        >
          <option value="general">General</option>
          <option value="work">Work</option>
          <option value="school">School</option>
          <option value="personal">Personal</option>
          <option value="errands">Errands</option>
        </select>

        <input
          type="date"
          value={dueDate}
          onChange={(event) => setDueDate(event.target.value)}
        />

        <button type="submit">Add Task</button>
      </form>

      {loading && <p className="status-message">Loading tasks...</p>}

      {error && <p className="error-message">{error}</p>}

      {!loading && !error && tasks.length === 0 && (
        <p className="status-message">No tasks found.</p>
      )}

      {!loading && !error && tasks.length > 0 && (
        <section className="task-list">
          {tasks.map((task) => {
            const dueDateStatus = getDueDateStatus(task);

            return (
              <article
                key={task.id}
                className={`task-card ${task.completed ? "completed" : ""}`}
              >
                <div className="task-card-header">
                  <h2>{task.text}</h2>

                  <span className={`due-date-badge ${dueDateStatus}`}>
                    {getDueDateLabel(task)}
                  </span>
                </div>

                <div className="task-meta">
                  <span>Priority: {task.priority}</span>
                  <span>Category: {task.category}</span>
                  <span>Status: {task.completed ? "Completed" : "Active"}</span>
                  <span>Created: {task.created_at}</span>
                </div>

                <div className="task-actions">
                  <button onClick={() => toggleTask(task)}>
                    {task.completed ? "Mark Active" : "Mark Complete"}
                  </button>

                  <button
                    className="danger-button"
                    onClick={() => deleteTask(task.id)}
                  >
                    Delete
                  </button>
                </div>
              </article>
            );
          })}
        </section>
      )}
    </main>
  );
}

export default App;