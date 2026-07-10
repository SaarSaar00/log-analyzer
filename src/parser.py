import re
from datetime import datetime
from models import LogEntry

LOG_PATTERN = (
    r"(\S+)\s+-\s+-\s+"
    r"\[(.*?)\]\s+"
    r"\"[A-Z]+\s+(.*?)\s+HTTP/\d(?:\.\d)?\"\s+"
    r"(\d{3})"
)


def validate_ip(ip: str) -> bool:
    parts = ip.split(".")

    if len(parts) != 4:
        return False

    for part in parts:
        if not part.isdigit():
            return False

        if not 0 <= int(part) <= 255:
            return False

    return True


def validate_status(status_code: int) -> bool:
    return 100 <= status_code <= 599


def validate_endpoint(endpoint: str) -> bool:
    return bool(endpoint) and endpoint.startswith("/")


def validate_timestamp(timestamp: str) -> bool:
    try:
        datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S")
        return True
    except ValueError:
        return False


def normalize_endpoint(endpoint: str) -> str:
    parts = endpoint.strip("/").split("/")

    if not parts or parts == [""]:
        return "/"

    return f"/{parts[0]}"


def parse_line(line: str) -> LogEntry | None:
    match = re.match(LOG_PATTERN, line)

    if match is None:
        return None

    ip = match.group(1)
    timestamp = match.group(2)
    endpoint = match.group(3)
    status_code = int(match.group(4))

    if not validate_ip(ip):
        return None

    if not validate_timestamp(timestamp):
        return None

    if not validate_endpoint(endpoint):
        return None

    if not validate_status(status_code):
        return None

    endpoint = normalize_endpoint(endpoint)
    hour = int(timestamp.split(":")[1])

    return LogEntry(ip, endpoint, status_code, hour)