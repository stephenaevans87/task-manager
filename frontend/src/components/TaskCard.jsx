function TaskCard({ task }) {
  return (
    <article className="task-card">
      <h2>{task.text}</h2>

      <div className="task-meta">
        <span>Priority: {task.priority || "None"}</span>
        <span>Category: {task.category || "None"}</span>
        <span>Status: {task.completed ? "Completed" : "Incomplete"}</span>
      </div>

      <p className="task-date">Created: {task.created_at}</p>
    </article>
  );
}

export default TaskCard;