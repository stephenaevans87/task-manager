from flask import Blueprint, render_template, request, redirect, abort
from flask import session
from datetime import datetime

from storage import (
    load_tasks,
    search_tasks,
    get_task,
    add_task,
    delete_task,
    update_task,
    toggle_complete
)


tasks_bp = Blueprint("tasks", __name__)


# ===================================
# MAIN PAGE
# ===================================

@tasks_bp.route("/", methods=["GET", "POST"])
def home():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        task_text = request.form.get(
            "task",
            ""
        ).strip()

        priority = request.form.get(
            "priority",
            "medium"
        )

        category = request.form.get(
            "category",
            "general"
        )

        if task_text == "":
            return redirect("/")

        allowed_priorities = [
            "low",
            "medium",
            "high"
        ]

        if priority not in allowed_priorities:
            priority = "medium"

        allowed_categories = [
            "general",
            "work",
            "school",
            "personal",
            "errands"
        ]

        if category not in allowed_categories:
            category = "general"

        add_task(
            text=task_text,
            created_at=datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            priority=priority,
            category=category,
            user_id=session["user_id"]
        )

        return redirect("/")

    search_term = request.args.get(
        "search",
        ""
    ).strip()

    if search_term:

        tasks = search_tasks(
            search_term,
            session["user_id"]
        )

    else:

        tasks = load_tasks(
            session["user_id"]
        )

    current_filter = request.args.get(
        "filter",
        "all"
    )

    if current_filter == "active":

        tasks = [
            task for task in tasks
            if not task["completed"]
        ]

    elif current_filter == "completed":

        tasks = [
            task for task in tasks
            if task["completed"]
        ]

    current_sort = request.args.get(
        "sort",
        "date"
    )

    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2
    }

    if current_sort == "priority":

        tasks.sort(
            key=lambda task: (
                task["completed"],
                priority_order.get(
                    task["priority"],
                    1
                ),
                task["created_at"]
            )
        )

    else:

        tasks.sort(
            key=lambda task: task["created_at"],
            reverse=True
        )

    return render_template(
        "index.html",
        tasks=tasks,
        current_filter=current_filter,
        current_sort=current_sort,
        search_term=search_term
    )


@tasks_bp.route("/delete/<int:task_id>")
def delete(task_id):

    if "user_id" not in session:
        return redirect("/login")

    task = get_task(task_id)

    if task is None:
        abort(404)

    if task["user_id"] != session["user_id"]:
        abort(404)

    delete_task(task_id)

    return redirect("/")


@tasks_bp.route("/complete/<int:task_id>")
def complete(task_id):

    if "user_id" not in session:
        return redirect("/login")

    task = get_task(task_id)

    if task is None:
        abort(404)

    if task["user_id"] != session["user_id"]:
        abort(404)

    completed = not bool(
        task["completed"]
    )

    if completed:

        completed_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    else:

        completed_at = None

    toggle_complete(
        task_id,
        int(completed),
        completed_at
    )

    return redirect("/")


@tasks_bp.route(
    "/edit/<int:task_id>",
    methods=["GET", "POST"]
)
def edit_task(task_id):

    if "user_id" not in session:
        return redirect("/login")

    task = get_task(task_id)

    if task is None:
        abort(404)

    if task["user_id"] != session["user_id"]:
        abort(404)

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        if title == "":
            return redirect(
                f"/edit/{task_id}"
            )

        priority = request.form.get(
            "priority",
            "medium"
        )

        category = request.form.get(
            "category",
            "general"
        )

        allowed_priorities = [
            "low",
            "medium",
            "high"
        ]

        if priority not in allowed_priorities:
            priority = "medium"

        allowed_categories = [
            "general",
            "work",
            "school",
            "personal",
            "errands"
        ]

        if category not in allowed_categories:
            category = "general"

        update_task(
            task_id,
            title,
            priority,
            category
        )

        return redirect("/")

    return render_template(
        "edit.html",
        task=task
    )