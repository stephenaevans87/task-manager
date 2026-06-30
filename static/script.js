// -----------------------------------
// Flask Task Manager
// Session 22 - REST API Layer
// -----------------------------------

console.log("Session 22 JavaScript loaded.");

const taskForm = document.querySelector(".task-form");
const taskInput = document.querySelector('input[name="task"]');
const prioritySelect = document.querySelector('select[name="priority"]');
const categorySelect = document.querySelector('select[name="category"]');
const characterCount = document.querySelector("#character-count");
const toggleButton = document.querySelector("#toggle-completed-btn");
const taskList = document.querySelector(".task-list");
const themeToggleButton = document.querySelector("#theme-toggle-btn");


// -----------------------------------
// Theme Preference
// -----------------------------------

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


// -----------------------------------
// Character Counter
// -----------------------------------

if (taskInput && characterCount) {

    taskInput.addEventListener("input", function () {

        characterCount.textContent =
            taskInput.value.length + " characters";

    });

}


// -----------------------------------
// Create Task Element
// -----------------------------------

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


// -----------------------------------
// AJAX Add Task
// -----------------------------------

if (taskForm && taskInput && taskList) {

    taskForm.addEventListener("submit", function (event) {

        event.preventDefault();

        const taskText = taskInput.value.trim();

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
                category: categorySelect.value
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

                characterCount.textContent = "0 characters";

                console.log("Task added with REST API.");

            })

            .catch(function (error) {

                console.error("AJAX Error:", error.message);

                alert("Something went wrong while adding the task.");

            });

    });

}


// -----------------------------------
// Show / Hide Completed Tasks
// -----------------------------------

let completedVisible = true;

if (toggleButton) {

    toggleButton.addEventListener("click", function () {

        const completedTasks =
            document.querySelectorAll(".task-item.completed");

        completedTasks.forEach(function (task) {

            if (completedVisible) {
                task.style.display = "none";
            } else {
                task.style.display = "";
            }

        });

        completedVisible = !completedVisible;

        toggleButton.textContent =
            completedVisible
                ? "Hide Completed Tasks"
                : "Show Completed Tasks";

    });

}