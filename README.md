# Log Analyzer

یک ابزار خط فرمان (CLI) نوشته شده با Python برای تحلیل فایل‌های حجیم `access.log` سرورهای وب.

این ابزار بدون بارگذاری کل فایل در حافظه، لاگ‌ها را به صورت خط به خط پردازش می‌کند و امکان استخراج آمارهای مهم ترافیک را فراهم می‌کند.

---

## Features

- **Memory Efficient Processing**

  خواندن فایل به صورت Line-by-Line برای کاهش مصرف حافظه و امکان پردازش فایل‌های بزرگ.

- **Fault Tolerant Parsing**

  پارس کردن امن داده‌ها و نادیده گرفتن خطوط خراب یا داده‌های نامعتبر (Dirty Data) بدون متوقف شدن برنامه.

- **Log Statistics**

  استخراج اطلاعات زیر:
  - تعداد کل درخواست‌ها
  - تعداد خطوط نامعتبر
  - تعداد IPهای یکتا
  - تعداد درخواست‌های خطادار (4xx و 5xx)
  - نرخ خطا
  - پرتکرارترین Endpointها
  - توزیع درخواست‌ها در ساعات مختلف

- **Flexible CLI**

  استفاده از ماژول استاندارد `argparse` برای دریافت مسیر فایل ورودی و تعیین تعداد Endpointهای پرترافیک.

---

## Requirements

این پروژه هیچ وابستگی خارجی (Third-party Dependency) ندارد و فقط از کتابخانه‌های استاندارد Python استفاده می‌کند.

Python version:

```text
Python 3.10+
```

---

## Usage

اجرای برنامه:

```bash
python main.py path/to/access.log
```

مثال:

```bash
python main.py sample_logs/access.log
```

نمایش تعداد مشخصی از Endpointهای پرترافیک:

```bash
python main.py sample_logs/access.log --top 15
```

---

## Project Structure

```text
log-analyzer/
│
├── main.py
├── README.md
├── .gitignore
│
└── src/
    ├── __init__.py
    ├── models.py
    ├── parser.py
    └── analyzer.py
```

---

## Example Output

Running:

```bash
python main.py sample_logs/access.log
```

produces:

```text
========== Log Analysis Report ==========

Total Requests : 495044
Invalid Lines  : 4956
Unique IPs     : 4001
Error Requests : 51075
Error Rate     : 10.32%

Top 10 Endpoints
------------------------------
/                         146302
/products                 87685
/api/search               48842
/cart                     34181
/login                    31658
/static/app.js            29249
/static/style.css         24299
/health                   14549
/api/checkout             9807
/products/9820            20

Requests Per Hour
------------------------------
00:00 -> 51026
01:00 -> 50971
02:00 -> 50975
03:00 -> 50705
04:00 -> 50847
05:00 -> 51002
06:00 -> 50809
07:00 -> 50844
08:00 -> 50912
09:00 -> 36953
```

---

## Technical Decisions

### 1. Memory Management

یکی از چالش‌های اصلی در پردازش لاگ، مدیریت مصرف حافظه است.

استفاده از روش‌هایی مانند:

```python
file.readlines()
```

باعث می‌شود کل فایل وارد حافظه شود و برای فایل‌های بزرگ مصرف RAM افزایش پیدا کند.

به همین دلیل در این پروژه از پردازش خط به خط استفاده شده است:

```python
for line in file:
```

در این روش فقط یک خط در هر لحظه پردازش می‌شود.

---

### 2. Unique IP Counting

برای شمارش IPهای یکتا از ساختار داده `set` استفاده شده است.

در سیستم‌های واقعی با حجم بسیار زیاد داده، استفاده از `set` می‌تواند باعث مصرف بالای حافظه شود.

در چنین شرایطی می‌توان از الگوریتم‌های تقریبی مانند **HyperLogLog** استفاده کرد تا با مصرف حافظه کمتر، تخمین مناسبی از تعداد IPهای یکتا ارائه شود.

---

### 3. Log Parsing and Dirty Data Handling

برای استخراج اطلاعات از Regex استفاده شده است.

الگوی Regex به گونه‌ای طراحی شده که با فرمت‌های رایج Apache Access Log سازگار باشد و تغییرات جزئی مانند وجود username در بخش ident:

```text
%u %l
```

باعث invalid شدن اشتباه خطوط نشود.

همچنین قبل از ثبت اطلاعات، داده‌ها از نظر موارد زیر اعتبارسنجی می‌شوند:

- فرمت IP
- محدوده Status Code
- فرمت Timestamp
- معتبر بودن Endpoint

---

## Git History

توسعه پروژه در چند مرحله انجام شده است تا روند پیاده‌سازی مشخص باشد:

1. Initial project structure and data models
2. Implement log parsing and validation
3. Add log analysis and statistics calculation
4. Implement CLI interface
5. Clean project configuration files

---

## Future Improvements

بهبودهای قابل انجام در نسخه‌های آینده:

- استفاده از HyperLogLog برای شمارش IPهای یکتا در مقیاس بسیار بزرگ
- اضافه کردن خروجی JSON برای استفاده در سیستم‌های دیگر
- اضافه کردن Unit Test برای Parser و Analyzer
- اضافه کردن نمودارهای آماری برای تحلیل بهتر ترافیک
- پشتیبانی از فرمت‌های مختلف Web Server Log