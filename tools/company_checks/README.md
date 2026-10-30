# کنترل بازتولیدپذیر پرونده کیهان صنعت قائم

این ابزار آفلاین است و هیچ درخواست شبکه خارجی یا تغییری در رسیدهای تاریخی ایجاد نمی‌کند.

```bash
python tools/company_checks/validate_keyhan_dossier.py --mode invariants
python tools/company_checks/validate_keyhan_dossier.py --mode snapshot
python tools/company_checks/validate_keyhan_dossier.py --mode all
```

`invariants` ساختار HTML، پیوندهای محلی، RTL، صفحه مدیریتی، سازگاری schema و گراف شواهد و مسیر تاریخی را بدون تعداد ثابت بررسی می‌کند. `snapshot` علاوه بر آن، شمارها و hashهای صریح مشاهده 2026-10-30 را با `keyhan_sanat_snapshot.json` مقایسه می‌کند. تغییر علمی معتبر ممکن است snapshot را نیازمند بازبینی آگاهانه کند؛ این به معنی شکست schema نیست.

گزینه `--json-out <path>` نتیجه جدیدی را فقط در مسیر انتخابی می‌نویسد. `verification_results.json` شرکت یک رسید تاریخی است و این ابزار خودکار آن را بازنویسی نمی‌کند.

اسکریپت‌های `research/crawl_runs/` همچنان ignored هستند و بخشی از ابزار عمومی نیستند. به‌ویژه `build_ledger.py` برای مونتاژ همان اجرای تاریخی نوشته شده و تا زمان عمومی‌سازی ورودی‌ها و حذف فرض‌های اجرای خاص، بازتولید عمومی کامل محسوب نمی‌شود.
