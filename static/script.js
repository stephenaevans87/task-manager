// -----------------------------------
// Flask Task Manager
// Session 35 - Stability Fixes
// -----------------------------------

console.log("Session 35 JavaScript loaded.");

const taskForm = document.querySelector(".task-form");
const taskInput = document.querySelector('input[name="task"]');
const dueDateInput = document.querySelector('input[name="due_date"]');
const prioritySelect = document.querySelector('select[name="priority"]');
const categorySelect = document.querySelector('select[name="category"]');
const characterCount = document.querySelector("#character-count");
const toggleButton = document.querySelector("#toggle-completed-btn");
const taskList = document.querySelector(".task-list");
const themeToggleButton = document.querySelector("#theme-toggle-btn");

function applyTheme(theme) {
    if (theme === "dark") {
        document.body.classList.add("dark-theme");

        if (themeToggleButton) {
            themeToggleButton.textContent = "Light Mode";
        }
    } else {
        document.body.classList.remove("dark-theme");

        if (themeToggleButton) {
            themeToggleButton.textContent = "Dark Mode";
        }
    }
}

const savedTheme = localStorage.getItem("theme");

if (savedTheme === "dark") {
    applyTheme("dark");
} else {
    applyTheme("light");
}

if (themeToggleButton) {
    themeToggleButton.addEventListener("click", function () {
        const darkModeIsActive =
            document.body.classList.contains("dark-theme");

        if (darkModeIsActive) {
            applyTheme("light");
            localStorage.setItem("theme", "light");
        } else {
            applyTheme("dark");
            localStorage.setItem("theme", "dark");
        }
    });
}

if (taskInput && characterCount) {
    taskInput.addEventListener("input", function () {
        characterCount.textContent =
            taskInput.value.length + " characters";
    });
}

function getDueDateStatus(task) {
    if (task.completed && task.due_date) {
        return "completed";
    }

    if (!task.due_date) {
        return "none";
    }

    const today = new Date();
    const dueDate = new Date(task.due_date + "T00:00:00");

    today.setHours(0, 0, 0, 0);

    if (dueDate < today) {
        return "overdue";
    }

    return "upcoming";
}

function getDueDateHtml(task) {
    const status = getDueDateStatus(task);

    if (status === "completed") {
        return `
            <span class="due-date-label due-date-completed">
                Completed — due ${task.due_date}
            </span>
        `;
    }

    if (status === "overdue") {
        return `
            <span class="due-date-label due-date-overdue">
                Overdue: ${task.due_date}
            </span>
        `;
    }

    if (status === "upcoming") {
        return `
            <span class="due-date-label due-date-upcoming">
                Due ${task.due_date}
            </span>
        `;
    }

    return `
        <span class="due-date-label due-date-none">
            No due date
        </span>
    `;
}

function createTaskElement(task) {
    const listItem = document.createElement("li");

    listItem.className = "task-item";

    if (task.completed) {
        listItem.classList.add("completed");
    }

    listItem.innerHTML = `
        <div class="task-content">
            <span class="task-text">
                ${task.text}
            </span>

            <div class="task-meta">
                <span class="priority-label priority-${task.priority}">
                    ${task.priority}
                </span>

                <span class="category-label">
                    ${task.category}
                </span>

                ${getDueDateHtml(task)}
            </div>

            <div class="task-meta">
                <small>
                    Created:
                    ${task.created_at}
                </small>
            </div>
        </div>

        <div class="task-actions">
            <a class="complete-link" href="/complete/${task.id}">
                Complete
            </a>

            <a class="edit-link" href="/edit/${task.id}">
                Edit
            </a>

            <a class="delete-link" href="/delete/${task.id}">
                Delete
            </a>
        </div>
    `;

    return listItem;
}

if (taskForm && taskInput && taskList) {
    taskForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const taskText = taskInput.value.trim();
        const dueDate = dueDateInput ? dueDateInput.value : "";

        if (taskText === "") {
            alert("Please enter a task.");
            return;
        }

        fetch("/api/tasks", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                task: taskText,
                priority: prioritySelect.value,
                category: categorySelect.value,
                due_date: dueDate
            })
        })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error(
                        "Request failed with status " + response.status
                    );
                }

                return response.json();
            })
            .then(function (responseData) {
                if (!responseData.success) {
                    throw new Error(responseData.message);
                }

                const newTask = responseData.data;

                const emptyState = document.querySelector(".empty-state");

                if (emptyState) {
                    emptyState.remove();
                }

                const newTaskElement = createTaskElement(newTask);

                taskList.prepend(newTaskElement);

                taskInput.value = "";
                prioritySelect.value = "medium";
                categorySelect.value = "general";

                if (dueDateInput) {
                    dueDateInput.value = "";
                }

                if (characterCount) {
                    characterCount.textContent = "0 characters";
                }

                console.log("Task added with REST API.");
            })
            .catch(function (error) {
                console.error("AJAX Error:", error.message);
                alert("Something went wrong while adding the task.");
            });
    });
}