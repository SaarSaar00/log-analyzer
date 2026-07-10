class LogEntry:
    def __init__(self, ip: str, endpoint: str, status_code: int, hour: int):
        self.ip = ip
        self.endpoint = endpoint
        self.status_code = status_code
        self.hour = hour