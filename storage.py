from models import db, Task


def task_to_dict(task):

    return {
        "id": task.id,
        "text": task.text,
        "completed": task.completed,
        "created_at": task.created_at,
        "completed_at": task.completed_at,
        "priority": task.priority,
        "category": task.category,
        "user_id": task.user_id
    }


def load_tasks(user_id):

    tasks = Task.query.filter_by(
        user_id=user_id
    ).all()

    return [
        task_to_dict(task)
        for task in tasks
    ]


def search_tasks(search_text, user_id):

    tasks = Task.query.filter(
        Task.user_id == user_id,
        Task.text.like(
            f"%{search_text}%"
        )
    ).all()

    return [
        task_to_dict(task)
        for task in tasks
    ]


def get_task(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return None

    return task_to_dict(task)


def add_task(text, created_at, priority, category, user_id):

    task = Task(
        text=text,
        completed=False,
        created_at=created_at,
        completed_at=None,
        priority=priority,
        category=category,
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return task_to_dict(task)


def delete_task(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return

    db.session.delete(task)
    db.session.commit()


def update_task(task_id, text, priority, category):

    task = Task.query.get(task_id)

    if task is None:
        return

    task.text = text
    task.priority = priority
    task.category = category

    db.session.commit()


def toggle_complete(task_id, completed, completed_at):

    task = Task.query.get(task_id)

    if task is None:
        return

    task.completed = completed
    task.completed_at = completed_at

    db.session.commit()