from datetime import datetime


def format_datetime(datetime_string):

    if datetime_string is None:
        return None

    try:

        dt = datetime.strptime(
            datetime_string,
            "%Y-%m-%d %H:%M:%S"
        )

    except ValueError:

        dt = datetime.fromisoformat(datetime_string)

    return dt.strftime("%b %d, %Y — %I:%M %p")