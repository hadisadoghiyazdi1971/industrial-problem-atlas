# فهرست API و منابع ماشین‌خوان عمومی — 2026-10-30

کشف از HTML و هدر `Link` انجام شد؛ مسیر یا شناسه حدس زده نشد. فقط GET بدون حساب و با محدودکردن فیلدهای پاسخ انجام شد. این فهرست درباره محتوای وب است؛ API کارخانه در منابع بررسی‌شده تأیید نشد (`NOT_PUBLICLY_VERIFIABLE`).

- ریشه اعلام‌شده: https://www.ksgco.com/wp-json/ ؛ درخواست محدود: [فراداده ریشه](https://www.ksgco.com/wp-json/?_fields=name,description,url,home,namespaces)، پاسخ 200.
- هر صفحه، alternate اختصاصی از نوع `application/json` داشت؛ ۲۵ مورد زیر با `_fields=id,date_gmt,modified_gmt,link,status,type` خوانده شد و همگی 200 و `status=publish` داشتند.
- پارامتر `_fields` بر اساس [مستندات رسمی WordPress](https://developer.wordpress.org/rest-api/using-the-rest-api/global-parameters/) است؛ روش اعلام لینک در [Discovery](https://developer.wordpress.org/rest-api/using-the-rest-api/discovery/) توضیح داده شده است.
- داده کاربران/نویسندگان، دیدگاه‌ها، محتوای کامل، توکن، کوکی یا داده تولید درخواست یا ذخیره نشد.

| صفحه عمومی اعلام‌کننده | endpoint دقیق اعلام‌شده | آخرین تغییر ثبت‌شده CMS (UTC) |
|---|---|---|
| [/](https://www.ksgco.com/) | [wp/v2/pages/51](https://www.ksgco.com/wp-json/wp/v2/pages/51?_fields=id,date_gmt,modified_gmt,link,status,type) | 2022-04-18T05:26:35Z |
| [/aboutus/](https://www.ksgco.com/aboutus/) | [wp/v2/pages/2](https://www.ksgco.com/wp-json/wp/v2/pages/2?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-23T22:48:49Z |
| [/units/](https://www.ksgco.com/units/) | [wp/v2/pages/24](https://www.ksgco.com/wp-json/wp/v2/pages/24?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-28T20:20:33Z |
| [/units/machining/](https://www.ksgco.com/units/machining/) | [wp/v2/pages/160](https://www.ksgco.com/wp-json/wp/v2/pages/160?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-23T22:12:32Z |
| [/units/casting/](https://www.ksgco.com/units/casting/) | [wp/v2/pages/161](https://www.ksgco.com/wp-json/wp/v2/pages/161?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-23T22:13:23Z |
| [/units/specialized-quality-control-laboratory/](https://www.ksgco.com/units/specialized-quality-control-laboratory/) | [wp/v2/pages/162](https://www.ksgco.com/wp-json/wp/v2/pages/162?_fields=id,date_gmt,modified_gmt,link,status,type) | 2019-08-06T08:01:41Z |
| [/units/rd/](https://www.ksgco.com/units/rd/) | [wp/v2/pages/163](https://www.ksgco.com/wp-json/wp/v2/pages/163?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-23T22:13:16Z |
| [/aboutus/mission/](https://www.ksgco.com/aboutus/mission/) | [wp/v2/pages/209](https://www.ksgco.com/wp-json/wp/v2/pages/209?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-23T22:55:52Z |
| [/contactus/](https://www.ksgco.com/contactus/) | [wp/v2/pages/26](https://www.ksgco.com/wp-json/wp/v2/pages/26?_fields=id,date_gmt,modified_gmt,link,status,type) | 2021-07-26T08:15:27Z |
| [/%d8%aa%d9%88%d8%a7%d9%86%d9%85%d9%86%d8%af%db%8c-%d9%87%d8%a7%db%8c-%d8%b3%d8%a7%d8%b2%d9%85%d8%a7%d9%86/](https://www.ksgco.com/%d8%aa%d9%88%d8%a7%d9%86%d9%85%d9%86%d8%af%db%8c-%d9%87%d8%a7%db%8c-%d8%b3%d8%a7%d8%b2%d9%85%d8%a7%d9%86/) | [wp/v2/pages/296](https://www.ksgco.com/wp-json/wp/v2/pages/296?_fields=id,date_gmt,modified_gmt,link,status,type) | 2022-02-28T08:44:11Z |
| [/products/](https://www.ksgco.com/products/) | [wp/v2/pages/20](https://www.ksgco.com/wp-json/wp/v2/pages/20?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-21T21:52:46Z |
| [/products/passengercars/](https://www.ksgco.com/products/passengercars/) | [wp/v2/pages/107](https://www.ksgco.com/wp-json/wp/v2/pages/107?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-21T23:19:27Z |
| [/products/truck/](https://www.ksgco.com/products/truck/) | [wp/v2/pages/111](https://www.ksgco.com/wp-json/wp/v2/pages/111?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-21T23:18:36Z |
| [/products/road-machines/](https://www.ksgco.com/products/road-machines/) | [wp/v2/pages/115](https://www.ksgco.com/wp-json/wp/v2/pages/115?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-21T23:17:59Z |
| [/products/agriculture/](https://www.ksgco.com/products/agriculture/) | [wp/v2/pages/117](https://www.ksgco.com/wp-json/wp/v2/pages/117?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-21T23:23:42Z |
| [/products/railway/](https://www.ksgco.com/products/railway/) | [wp/v2/pages/119](https://www.ksgco.com/wp-json/wp/v2/pages/119?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-21T23:27:27Z |
| [/products/seegroup/](https://www.ksgco.com/products/seegroup/) | [wp/v2/pages/121](https://www.ksgco.com/wp-json/wp/v2/pages/121?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-21T23:30:53Z |
| [/quality/](https://www.ksgco.com/quality/) | [wp/v2/pages/22](https://www.ksgco.com/wp-json/wp/v2/pages/22?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-11-24T06:43:50Z |
| [/quality/certificates/](https://www.ksgco.com/quality/certificates/) | [wp/v2/pages/135](https://www.ksgco.com/wp-json/wp/v2/pages/135?_fields=id,date_gmt,modified_gmt,link,status,type) | 2019-08-03T10:45:04Z |
| [/quality/qualitypolicies/](https://www.ksgco.com/quality/qualitypolicies/) | [wp/v2/pages/137](https://www.ksgco.com/wp-json/wp/v2/pages/137?_fields=id,date_gmt,modified_gmt,link,status,type) | 2019-08-03T11:23:43Z |
| [/units/quality-control/](https://www.ksgco.com/units/quality-control/) | [wp/v2/pages/164](https://www.ksgco.com/wp-json/wp/v2/pages/164?_fields=id,date_gmt,modified_gmt,link,status,type) | 2019-08-08T03:22:51Z |
| [/%d8%ae%d8%a8%d8%b1%d9%86%d8%a7%d9%85%d9%87/](https://www.ksgco.com/%d8%ae%d8%a8%d8%b1%d9%86%d8%a7%d9%85%d9%87/) | [wp/v2/pages/294](https://www.ksgco.com/wp-json/wp/v2/pages/294?_fields=id,date_gmt,modified_gmt,link,status,type) | 2022-11-10T05:15:32Z |
| [/aboutus/history/](https://www.ksgco.com/aboutus/history/) | [wp/v2/pages/207](https://www.ksgco.com/wp-json/wp/v2/pages/207?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-23T22:49:42Z |
| [/aboutus/omessage/](https://www.ksgco.com/aboutus/omessage/) | [wp/v2/pages/208](https://www.ksgco.com/wp-json/wp/v2/pages/208?_fields=id,date_gmt,modified_gmt,link,status,type) | 2018-03-23T22:51:03Z |
| [/quality-2/](https://www.ksgco.com/quality-2/) | [wp/v2/pages/564](https://www.ksgco.com/wp-json/wp/v2/pages/564?_fields=id,date_gmt,modified_gmt,link,status,type) | 2022-02-28T09:16:41Z |

## اعلام‌شده ولی فراخوانی نشده

- لینک‌های oEmbed هر صفحه، RSS و خوراک دیدگاه‌ها فقط ثبت شدند؛ برای پرسش صنعتی نیاز نبود. `xmlrpc.php?rsd` و `wlwmanifest.xml` معرفی متادیتا هستند و فراخوانی نشدند.
- namespaceهای `contact-form-7/v1`، `wp-site-health/v1` و `wp-block-editor/v1` در فراداده ریشه دیده شدند؛ وجودشان مجوز دسترسی عمومی به همه مسیرها نیست. هیچ زیرمسیر آن‌ها خوانده نشد.
- پیکربندی عمومی frontend به `wp-admin/admin-ajax.php` اشاره داشت؛ فقط مشاهده شد و درخواست مستقلی به آن انجام نشد؛ فرم تماس هم ارسال نشد.
- sitemap کاربران اعلام شده بود و عمداً خوانده نشد. فقط sitemap صفحات عمومی خوانده شد.

## چه چیزی نتیجه نمی‌شود؟

وجود REST API وردپرس به معنای دسترسی به CNC، تجهیزات سنجش، PLC، MES یا ERP نیست. timestamp قدیمی رکورد CMS به‌تنهایی اثبات نمی‌کند تجهیزات یا فعالیت کارخانه قدیمی‌اند. شماره نسخه فایل‌های پوسته/پلاگین، مدرک آسیب‌پذیری یا نیاز قطعی به وصله خاص نیست؛ ممیزی امنیتی انجام نشده است.

## رسیدها

[رسید ریشه و قواعد](discovery/2026-10-30/access_and_api_receipts.json) · [رسید ۲۵ صفحه API](discovery/2026-10-30/advertised_page_api_receipts.json) · [لینک‌های کشف‌شده در HTML](discovery/2026-10-30/public_inventory.json). پاسخ‌ها به فراداده لازم محدود شده‌اند؛ HTML و PDF کامل در مخزن نیستند.
