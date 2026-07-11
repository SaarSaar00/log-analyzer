import argparse
import os
import gzip
import time
import json
from src.parser import parse_line
from src.analyzer import LogAnalyzer


def main():
    parser = argparse.ArgumentParser(description="Log Analyzer - A CLI tool to analyze access logs")
    parser.add_argument("log_file", help="Path to the access log file")
    parser.add_argument("--top", type=int, default=10, help="Number of top endpoints to show (default: 10)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()
    file_path = args.log_file

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    analyzer = LogAnalyzer()
    start_time = time.time()
    open_func = gzip.open if file_path.endswith(".gz") else open

    try:
        with open_func(file_path, "rt", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                entry = parse_line(line)
                analyzer.process_entry(entry)
    except Exception as e:
        print(f"Failed to read the file: {e}")
        return

    exec_time = time.time() - start_time
    stats = analyzer.get_statistics()

    if args.json:
        stats["execution_time_seconds"] = round(exec_time, 4)
        print(json.dumps(stats, indent=4))
        return

    print("\n========== Log Analysis Report ==========\n")
    print(f"Execution Time : {exec_time:.4f} seconds")
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

    if stats["suspicious_ips"]:
        print("\nSuspicious Activities (Brute-force attempts)")
        print("-" * 30)
        for ip, count in stats["suspicious_ips"].items():
            print(f"IP: {ip:<15} - {count} failed logins on /login")

    if stats["error_spikes"]:
        print("\nError Spikes (5xx errors >= 5%)")
        print("-" * 30)
        for hour, rate in stats["error_spikes"].items():
            print(f"Hour {hour:02d}:00 -> {rate:.2f}% error rate")


if __name__ == "__main__":
    main()