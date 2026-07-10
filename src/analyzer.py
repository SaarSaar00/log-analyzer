from src.models import LogEntry

class LogAnalyzer:
    def __init__(self):
        self.total_requests = 0
        self.invalid_lines = 0
        self.error_requests = 0
        self.unique_ips = set()
        self.endpoint_counts = {}
        self.hourly_counts = {}

    def process_entry(self, entry: LogEntry | None) -> None:
        if entry is None:
            self.invalid_lines += 1
            return

        self.total_requests += 1
        self.unique_ips.add(entry.ip)

        self.endpoint_counts[entry.endpoint] = self.endpoint_counts.get(entry.endpoint, 0) + 1
        self.hourly_counts[entry.hour] = self.hourly_counts.get(entry.hour, 0) + 1

        if 400 <= entry.status_code <= 599:
            self.error_requests += 1

    def get_statistics(self) -> dict:
        error_rate = 0
        if self.total_requests > 0:
            error_rate = (self.error_requests / self.total_requests) * 100

        return {
            "total_requests": self.total_requests,
            "invalid_lines": self.invalid_lines,
            "unique_ips_count": len(self.unique_ips),
            "error_requests": self.error_requests,
            "error_rate": error_rate,
            "endpoint_counts": self.endpoint_counts,
            "hourly_counts": self.hourly_counts,
        }