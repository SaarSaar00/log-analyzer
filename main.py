import argparse
import os
from src.parser import parse_line
from src.analyzer import LogAnalyzer


def main():
    parser = argparse.ArgumentParser(description="Log Analyzer - A CLI tool to analyze access logs")
    parser.add_argument("log_file", help="Path to the access log file")
    parser.add_argument("--top", type=int, default=10, help="Number of top endpoints to show (default: 10)")

    args = parser.parse_args()
    file_path = args.log_file

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    analyzer = LogAnalyzer()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                entry = parse_line(line)
                analyzer.process_entry(entry)
    except Exception as e:
        print(f"Failed to read the file: {e}")
        return

    stats = analyzer.get_statistics()

    print("\n========== Log Analysis Report ==========\n")
    print(f"Total Requests : {stats['total_requests']}")
    print(f"Invalid Lines  : {stats['invalid_lines']}")
    print(f"Unique IPs     : {stats['unique_ips_count']}")
    print(f"Error Requests : {stats['error_requests']}")
    print(f"Error Rate     : {stats['error_rate']:.2f}%\n")

    print(f"Top {args.top} Endpoints")
    print("-" * 30)
    sorted_endpoints = sorted(
        stats["endpoint_counts"].items(),
        key=lambda item: item[1],
        reverse=True
    )
    for endpoint, count in sorted_endpoints[:args.top]:
        print(f"{endpoint:<25} {count}")

    print("\nRequests Per Hour")
    print("-" * 30)
    for hour in sorted(stats["hourly_counts"]):
        count = stats["hourly_counts"][hour]
        print(f"{hour:02d}:00 -> {count}")


if __name__ == "__main__":
    main()