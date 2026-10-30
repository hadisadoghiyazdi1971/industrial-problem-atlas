بسته افزودنی امن IPA — پرونده چندلایه کیهان صنعت قائم
==================================================
این ZIP فقط فایل‌های جدید دارد؛ هیچ یک از فایل‌های فعلی Codex (از جمله index.html اصلی، company.json، research یا data/problems.json) در ZIP جایگزین نمی‌شود.

نصب:
۱) ZIP را استخراج و همه محتویاتش را در ریشه پوشه:
H:\HadiSadoghiYazdi\industrial-problem-atlas
کپی کنید؛ ساختار companies/ و tools/ را با پوشه‌های موجود ادغام کنید.

۲) روی ACTIVATE_SITE.cmd دوبار کلیک کنید. این اسکریپت فقط یک کادر کوچک پیوند به صفحه جدید را به سه HTML موجود اضافه می‌کند (اگر موجود باشند):
   index.html
   companies/index.html
   companies/keyhan-sanat-ghaem/index.html
   قبل از تغییر هر فایل، نسخه پشتیبان را خارج از مخزن، در Documents/IndustrialAtlasLocalBackups نگه می‌دارد. اجرای مجدد تکرار ایجاد نمی‌کند.

۳) این دستور را در ریشه مخزن اجرا کنید:
py -3 tools\verify_company_briefing.py
خروجی باید PASS باشد. سپس با RUN_LOCAL.cmd، صفحه را در مرورگر ببینید.

۴) در GitHub Desktop تغییرات را بازبینی، Commit و Push کنید. پس از پایان Pages Deploy، حتماً URL زیر را در مرورگر باز و تست کنید:
https://hadisadoghiyazdi1971.github.io/industrial-problem-atlas/companies/keyhan-sanat-ghaem/briefing/

۵) تا وقتی URL در سایت عمومی باز نمی‌شود، نامه شرکت را ارسال نکنید.

مهم: فایل‌ها و گزارش‌های Codex درباره شرکت، آزمایش‌ها و پژوهش قبلی حفظ می‌شوند.
این بسته هیچ Commit/Push یا نامه‌ای به‌طور خودکار نمی‌فرستد.
شواهد در صفحه به منابع رسمی وب پیوند دارند و دادهٔ داخلی یا همکاری شرکت ادعا نشده است.
نامه‌های Word/PDF دانشگاه و شرکت جدا از ZIP سایت ارائه می‌شوند و نباید با سایت در GitHub منتشر شوند.
