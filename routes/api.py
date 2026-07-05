from flask import Blueprint
from flask import request
from flask import session
from flask import jsonify
from datetime import datetime

from extensions import limiter

from storage import (
    load_tasks,
    get_task,
    add_task,
    delete_task,
    update_task,
    toggle_complete
)


api_bp = Blueprint("api", __name__, url_prefix="/api")


def api_success(data=None, message="Success", status_code=200):

    return jsonify(
        {
            "success": True,
            "message": message,
            "data": data
        }
    ), status_code


def api_error(message="Something went wrong", status_code=400):

    return jsonify(
        {
            "success": False,
            "message": message,
            "data": None
        }
    ), status_code


def require_login():

    if "user_id" not in session:
        return False

    return True


def parse_due_date(value):

    if value is None or value == "":
        return None

    try:
        return datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()

    except ValueError:
        return "invalid"


def get_user_task(task_id):

    task = get_task(task_id)

    if task is None:
        return None

    if task["user_id"] != session["user_id"]:
        return None

    return task


@api_bp.route("/tasks", methods=["GET"])
@limiter.limit("100 per minute")
def get_tasks():

    if not require_login():
        return api_error("Unauthorized", 401)

    tasks = load_tasks(session["user_id"])

    return api_success(
        tasks,
        "Tasks retrieved successfully",
        200
    )


@api_bp.route("/tasks", methods=["POST"])
@limiter.limit("30 per minute")
def create_task():

    if not require_login():
        return api_error("Unauthorized", 401)

    data = request.get_json()

    if data is None:
        return api_error("Missing JSON data", 400)

    task_text = data.get("task", "").strip()
    priority = data.get("priority", "medium")
    category = data.get("category", "general")
    due_date = parse_due_date(
        data.get("due_date")
    )

    print("RAW API DUE DATE:", data.get("due_date"))
    print("PARSED API DUE DATE:", due_date)

    if task_text == "":
        return api_error("Task text is required", 400)

    if due_date == "invalid":
        return api_error("Due date must use YYYY-MM-DD format", 400)

    if priority not in ["low", "medium", "high"]:
        priority = "medium"

    if category not in ["general", "work", "school", "personal", "errands"]:
        category = "general"

    new_task = add_task(
        text=task_text,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        priority=priority,
        category=category,
        user_id=session["user_id"],
        due_date=due_date
    )

    return api_success(
        new_task,
        "Task created successfully",
        201
    )


@api_bp.route("/tasks/<int:task_id>", methods=["GET"])
@limiter.limit("100 per minute")
def get_single_task(task_id):

    if not require_login():
        return api_error("Unauthorized", 401)

    task = get_user_task(task_id)

    if task is None:
        return api_error("Task not found", 404)

    return api_success(
        task,
        "Task retrieved successfully",
        200
    )


@api_bp.route("/tasks/<int:task_id>", methods=["PATCH"])
@limiter.limit("60 per minute")
def patch_task(task_id):

    if not require_login():
        return api_error("Unauthorized", 401)

    task = get_user_task(task_id)

    if task is None:
        return api_error("Task not found", 404)

    data = request.get_json()

    if data is None:
        return api_error("Missing JSON data", 400)

    text = data.get("text", task["text"]).strip()
    priority = data.get("priority", task["priority"])
    category = data.get("category", task["category"])
    completed = data.get("completed", task["completed"])

    if "due_date" in data:
        due_date = parse_due_date(
            data.get("due_date")
        )
    else:
        due_date = parse_due_date(
            task["due_date"]
        )

    if text == "":
        return api_error("Task text is required", 400)

    if due_date == "invalid":
        return api_error("Due date must use YYYY-MM-DD format", 400)

    if priority not in ["low", "medium", "high"]:
        priority = task["priority"]

    if category not in ["general", "work", "school", "personal", "errands"]:
        category = task["category"]

    update_task(
        task_id,
        text,
        priority,
        category,
        due_date
    )

    completed_at = task["completed_at"]

    if completed != task["completed"]:

        if completed:
            completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            completed_at = None

        toggle_complete(
            task_id,
            int(completed),
            completed_at
        )

    updated_task = get_task(task_id)

    return api_success(
        updated_task,
        "Task updated successfully",
        200
    )


@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@limiter.limit("30 per minute")
def delete_single_task(task_id):

    if not require_login():
        return api_error("Unauthorized", 401)

    task = get_user_task(task_id)

    if task is None:
        return api_error("Task not found", 404)

    delete_task(task_id)

    return api_success(
        None,
        "Task deleted successfully",
        200
    )