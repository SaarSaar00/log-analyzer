import unittest
from src.parser import parse_line

class TestParser(unittest.TestCase):
    def test_valid_log_line(self):
        line = '203.0.113.42 - - [01/Jun/2026:09:14:22 +0000] "GET /products/1877 HTTP/1.1" 200 5324 "-" "Mozilla/5.0"'
        entry = parse_line(line)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.ip, "203.0.113.42")
        self.assertEqual(entry.endpoint, "/products/1877")
        self.assertEqual(entry.status_code, 200)
        self.assertEqual(entry.hour, 9)

    def test_invalid_log_line(self):
        line = 'This is a broken and dirty log line'
        entry = parse_line(line)
        self.assertIsNone(entry)

if __name__ == "__main__":
    unittest.main()