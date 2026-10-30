# گزارش اجرای اصلاح آمادگی مخاطب — پاسخ به بازبینی مستقل

**تاریخ:** 2026-10-30 / ۸ آبان ۱۴۰۵  
**ورودی دستور:** `C:\Users\Hadi\Downloads\IPA004_Independent_Review_and_Codex_NextSteps_FA.md`  
**وضعیت:** اصلاحات محلی انجام شد؛ هیچ Commit، Push، انتشار یا مکاتبه‌ای انجام نشد. سایت رسمی دوباره خزش نشد، چون بازبینی مستقل شکاف شاهد مشخصی که نیازمند خزش تازه باشد معرفی نکرد.

## خط مبنا پیش از ویرایش این مرحله

`git status --short` تغییرات پژوهش قبلی و یک ZIP جدید untracked را نشان داد. ZIP متعلق به کاربر فرض و دست‌نخورده نگه داشته شد. سپس این کنترل‌ها پیش از ویرایش موفق بودند:

```text
python tools/validate_atlas.py
PASS: 4 case files validated; 5 pages/link checks passed.

python pilot/synthetic_sensor_demo.py --check
PASS: synthetic demo self-check; no outputs written.

git diff --check
exit 0 (فقط هشدار عادی LF/CRLF در PowerShell)
```

`git ls-files` نشان داد که در شروع این مرحله فقط هشت فایل اصلی شرکت در `HEAD` بودند. `git check-ignore -v` نیز تأیید کرد اسکریپت‌های تاریخی زیر `research/crawl_runs/` به علت قاعده موجود `.gitignore` با Push عادی منتشر نمی‌شوند. جزئیات وضعیت انتشار در [PUBLICATION_REVIEW_FA.md](PUBLICATION_REVIEW_FA.md) ثبت شد.

## پاسخ اجرایی به P1 تا P6

### P1 — خلاصه مدیریتی

[management-brief.html](../management-brief.html) ساخته شد: فارسی RTL، دارای viewport، CSS چاپ A4 و محتوای متمرکز بر چهار پرسش تصمیم، داده حداقلی، دامنه آزمون سایه و شرط توقف. صفحه هیچ عدد منفعت، ROI، عیب بالفعل یا ادعای دسترسی داخلی ندارد. پیوند روشن آن به بالای صفحه شرکت افزوده شد.

### P2 — تفکیک پیام مشتری از اسناد کارگاهی

لینک‌های گزارش خزش، API، نقد محتوا، دفتر شواهد و گزارش Codex از [صفحه شرکت](../index.html) حذف شدند. صفحه همچنان منابع اصلی رسمی و روش NIST را دارد. هیچ فایل پژوهشی حذف یا منتقل نشد؛ حذف لینک خصوصی‌سازی تلقی نشده است. تصمیم انتقال فایل‌های کارگاهی یا نامه به مسیر ignored در اختیار مالک مخزن باقی ماند.

### P3 و P4 — بازتولیدپذیری و نگهداری آزمون

ابزار version-controlled جدید در `tools/company_checks/validate_keyhan_dossier.py` قرار گرفت. آزمون‌های invariant از snapshot جدا هستند:

- `--mode invariants`: schema و گراف شواهد، پیوندها، RTL، صفحه مدیریتی، مسیر قدیمی و حدود ادعا؛ بدون تعداد ثابت و بدون `git show HEAD`.
- `--mode snapshot`: علاوه بر invariantها، شمارها و hashهای اجرای تاریخی 2026-10-30 را از `keyhan_sanat_snapshot.json` بررسی می‌کند.
- `--json-out`: در صورت درخواست نتیجه جدید می‌سازد و رسید تاریخی شرکت را خودکار بازنویسی نمی‌کند.

اسکریپت محلی `build_ledger.py` در مسیر ignored باقی ماند و در [README ابزار](../../../tools/company_checks/README.md) صریحاً به‌عنوان ابزار مونتاژ وابسته به اجرای تاریخی، نه بازتولید عمومی کامل، معرفی شد. رسیدهای پیشین تغییر داده نشدند.

### P5 — دموی اختصاصی مصنوعی قطر

`pilot/ipa004_synthetic_diameter_demo.py` اضافه شد. سناریو شامل قطر اسمی 100.000 میلی‌متر، نویز فرایند و اندازه‌گیری، نمونه‌گیری هر پنج قطعه، تفکیک ۱۶۰ نمونه آموزش و ۲۴۰ نمونه آزمون و انحراف تدریجی تحمیلی است. تمام خروجی‌ها برچسب `SYNTHETIC — NOT COMPANY DATA` دارند.

Shewhart و EWMA جداگانه روی بودجه برابر **۵ شروع رخداد هشدار در هر ۱۰۰۰ نمونه سالم** با ۶۰۰ اجرای کالیبراسیون تنظیم و با ۴۰۰ اجرای مستقل سالم کنترل شدند. نرخ مستقل به‌ترتیب 5.333333 و 4.9375 بود. در تنها سناریوی نمایش، EWMA زودتر هشدار داد؛ این عدد نتیجه تصادفی همین شبیه‌سازی و **فاقد معنای منفعت شرکت** است. نتیجه واقعی به اعتبار سنجش، روش نمونه‌گیری و رخداد مرجع شرکت وابسته است. خروجی‌های محلی در `pilot/output/ipa004_synthetic_diameter/` ساخته شدند و طبق `.gitignore` منتشر نمی‌شوند. XML نمودار SVG معتبر بود؛ رندر تصویری در این محیط انجام نشد.

### P6 — مرورگر و نسخه مستقر

برای مرور واقعی صفحه محلی، Browser رسمی راه‌اندازی شد؛ فهرست مرورگرهای قابل اتصال خالی بود (`No browser is available`). طبق راهنمای Browser از ابزار کنترل نامرتبط جایگزین استفاده نشد. بنابراین رندر موبایل، تعداد قطعی صفحات چاپ و نسخه آنلاین مستقر تأیید نشده‌اند. ساختار، viewport، CSS چاپ A4، پیوندها و مسیرهای HTTP محلی با آزمون آفلاین کنترل شدند. بازبینی واقعی مرورگر و GitHub Pages همچنان دروازه انتشار است.

## نامه اولیه

[DRAFT_EMAIL_FA.md](../outreach/DRAFT_EMAIL_FA.md) به خلاصه مدیریتی مستقیم پیوند می‌دهد. بخش قابل ارسال با احتساب عنوان و metadata، ۱۸۳ واژه دارد و زیر سقف تقریبی ۲۵۰ واژه است. هیچ اختلاف محتوای سایت، گواهینامه، API یا آمار خزش را برجسته نمی‌کند. نقش تهیه‌کننده به عنوان طرح مستقل بیان شده و نمایندگی دانشگاه/شرکت ادعا نشده است. نامه ارسال نشده است.

## آزمون‌های نهایی این مرحله

```text
python tools/company_checks/validate_keyhan_dossier.py --mode invariants
PASS: 30 checks; mode=invariants; failures=0

python tools/company_checks/validate_keyhan_dossier.py --mode snapshot --skip-http
PASS: 36 checks; mode=snapshot; failures=0

python pilot/ipa004_synthetic_diameter_demo.py --check
PASS: comparable false-alarm budget calibrated and independently checked.

python -m py_compile pilot/ipa004_synthetic_diameter_demo.py tools/company_checks/validate_keyhan_dossier.py
exit 0
```

آزمون‌های عمومی مخزن، هر دو حالت کنترل شرکت، دموهای مصنوعی، `git diff --check` و snapshot محتوای IPA-001 تا IPA-003 در پایان دوباره اجرا شدند. نتیجه نهایی: اعتبارسنج اطلس PASS، دموی عمومی PASS، دموی IPA-004 PASS، کنترل شرکت در حالت `all` برابر **۳۷ کنترل موفق و صفر شکست**، و `git diff --check` با کد خروج صفر. هشدارهای LF/CRLF ویندوز خطای محتوایی نبودند.

## مسیرهای دقیق برای GitHub Desktop

فایل‌های اصلی این مرحله که باید در تب **Changes** دیده شوند:

- `companies/keyhan-sanat-ghaem/management-brief.html`
- `companies/keyhan-sanat-ghaem/index.html`
- `companies/keyhan-sanat-ghaem/outreach/DRAFT_EMAIL_FA.md`
- `companies/keyhan-sanat-ghaem/research/PUBLICATION_REVIEW_FA.md`
- `companies/keyhan-sanat-ghaem/research/CLIENT_READINESS_RUN_REPORT.md`
- `pilot/ipa004_synthetic_diameter_demo.py`
- `tools/company_checks/validate_keyhan_dossier.py`
- `tools/company_checks/keyhan_sanat_snapshot.json`
- `tools/company_checks/README.md`
- `.github/workflows/validate.yml`

فایل `companies/keyhan-sanat-ghaem.zip` نیز untracked دیده می‌شود، اما در این کار ساخته یا تغییر داده نشده و برای Commit توصیه نشده است. فهرست کامل پژوهش قبلی در وضعیت Git باقی است و باید طبق تصمیم انتشار مالک انتخاب شود.
