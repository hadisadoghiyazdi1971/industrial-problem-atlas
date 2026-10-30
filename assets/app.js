/* Industrial Problem Atlas | no framework, no tracker, no external API */
'use strict';
const DATA_PATH = 'data/problems.json';
const STATUS_LABELS = {
  concept: 'طرح مسئله', needs_data: 'داده در حال بررسی',
  pilot: 'پایلوت محدود', validated: 'ارزیابی مستقل'
};
const LEVEL_LABELS = {
  illustrative: 'صرفاً سناریوی پیشنهادی', public_source: 'مستندات عمومی',
  authorized_observation: 'مشاهده با مجوز', measured: 'نتیجه اندازه‌گیری‌شده'
};
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = String(text);
  return node;
}
function append(parent, ...children) {
  children.forEach(child => parent.appendChild(child));
  return parent;
}
function labelForStatus(key) { return STATUS_LABELS[key] || 'نامشخص'; }
function pill(key) { return el('span', 'status-pill status-' + key, labelForStatus(key)); }
function fail(target, message) { target.replaceChildren(el('div','notice error',message)); }
async function loadData() {
  const response = await fetch(DATA_PATH, {cache:'no-store'});
  if (!response.ok) throw new Error('HTTP ' + response.status);
  const result = await response.json();
  if (!Array.isArray(result.problems)) throw new Error('Invalid catalog');
  return result;
}
function makeCard(problem) {
  const article = el('article','problem-card');
  const top = el('div','card-top');
  append(top, el('span','id-label',problem.id), pill(problem.status));
  const heading = el('h3');
  const link = el('a','card-title',problem.title_fa);
  link.href = 'problem.html?id=' + encodeURIComponent(problem.id);
  heading.appendChild(link);
  const desc = el('p','card-desc',problem.summary_fa);
  const tail = el('div','card-bottom');
  append(tail,el('span','sector-label',problem.sector),el('span','card-link','بررسی پرونده ←'));
  append(article,top,heading,desc,tail);
  if(problem.lead) article.classList.add('featured');
  return article;
}
function initHome(data) {
  const list = document.getElementById('problem-list');
  const count = document.getElementById('total-count');
  const search = document.getElementById('search-input');
  const sector = document.getElementById('sector-select');
  [...new Set(data.problems.map(x=>x.sector))].sort().forEach(name => {
    const option = el('option','',name); option.value = name; sector.appendChild(option);
  });
  const render = () => {
    const term = search.value.trim().toLocaleLowerCase('fa');
    const filtered = data.problems.filter(p =>
      (!sector.value || p.sector===sector.value) &&
      (!term || [p.id,p.title_fa,p.title_en,p.summary_fa,p.sector].join(' ').toLocaleLowerCase('fa').includes(term)));
    list.replaceChildren(...(filtered.length ? filtered.map(makeCard) : [el('div','notice','پرونده‌ای مطابق جستجوی شما پیدا نشد.') ]));
    count.textContent = filtered.length.toLocaleString('fa-IR')+' پرونده از '+data.problems.length.toLocaleString('fa-IR');
  };
  search.addEventListener('input',render);
  sector.addEventListener('change',render);
  render();
}
function makeBullets(items) {
  const ul = el('ul','detail-list');
  items.forEach(item => ul.appendChild(append(el('li'),el('span','',item))));
  return ul;
}
function section(title, nodeOrItems, className='') {
  const wrap = el('section','detail-section '+className);
  wrap.appendChild(el('h2','',title));
  if (Array.isArray(nodeOrItems)) wrap.appendChild(makeBullets(nodeOrItems));
  else wrap.appendChild(nodeOrItems);
  return wrap;
}
function makeReferences(refs) {
  const ul = el('ul','detail-list');
  refs.forEach(ref=>{
    const li=el('li'); const a=el('a','text-link',ref.label);
    a.href=ref.url; a.target='_blank'; a.rel='noopener noreferrer';
    li.appendChild(a);
    li.appendChild(el('span','reference-tag',' — زمینه مرتبط، نه تأیید نتیجه'));
    ul.appendChild(li);
  });
  return ul;
}
function initProblem(data) {
  const target=document.getElementById('problem-detail');
  const id=new URLSearchParams(location.search).get('id');
  if (!id || !/^IPA-\d{3,5}$/.test(id)) return fail(target,'شناسه پرونده نامعتبر است. از فهرست پرونده‌ها یک مورد انتخاب کنید.');
  const p=data.problems.find(x=>x.id===id);
  if (!p) return fail(target,'پرونده با این شناسه پیدا نشد.');
  document.title=p.title_fa+' | اطلس مسائل صنعت و جامعه';
  const heading=el('header','detail-hero');
  const meta=el('div','detail-meta');
  append(meta,el('span','id-label',p.id),pill(p.status),el('span','sector-label',p.sector));
  append(heading,meta,el('h1','',p.title_fa),el('p','english-title',p.title_en),el('p','detail-summary',p.summary_fa));
  if (p.case_url) {
    const caseLink=el('a','btn primary','مطالعه پیشنهاد اختصاصی بر اساس منابع عمومی ←');
    caseLink.href=p.case_url;
    caseLink.style.marginTop='12px';
    heading.appendChild(caseLink);
  }
  const evidence=el('div','evidence-banner');
  append(evidence,el('b','','سطح شواهد: '+(LEVEL_LABELS[p.evidence_level]||'نامشخص')),el('span','','تاریخ بازبینی: '+p.updated+' | شواهد آزمایش صنعتی برای این پرونده گزارش نشده است.'));
  const main=el('div','detail-layout');
  const body=el('div','detail-body');
  append(body,
    section('تعریف دقیق مسئله',el('p','',p.problem_fa)),
    section('چرا این مسئله مهم است؟',el('p','',p.why_it_matters)),
    section('داده‌های لازم',p.data_needed),
    section('خط مبنای مهندسی',p.baseline_methods),
    section('روش‌های پیشرفته قابل بررسی',p.advanced_options),
    section('معیارهای ارزیابی',p.evaluation),
    section('خطرها و حدود اعتبار',p.risks),
    section('گام‌های پیشنهادی برای آزمون',p.next_steps)
  );
  if (p.references?.length) body.appendChild(section('منابع و کارهای مرتبط (نه سند تأیید)',makeReferences(p.references)));
  const side=el('aside','detail-side');
  const student=el('div','sidebar-card');
  append(student,el('div','overline','کاربرد آموزشی'),el('h3','','تمرین دانشجویی'),el('p','',p.student_challenge));
  const org=el('div','sidebar-card');
  append(org,el('div','overline','پرسش از سازمان'),el('h3','','قبل از ساخت مدل')); org.appendChild(makeBullets(p.org_questions));
  const href=el('a','btn primary sidebar-btn','گفت‌وگو درباره مسئله ←'); href.href='organizations.html';
  append(org,href);
  append(side,student,org);append(main,body,side);
  target.replaceChildren(heading,evidence,main);
}
document.addEventListener('DOMContentLoaded',async()=>{
  const page=document.body.dataset.page;
  if (!['home','problem'].includes(page)) return;
  const target=document.getElementById(page==='home'?'problem-list':'problem-detail');
  try { const data=await loadData(); if(page==='home') initHome(data); else initProblem(data); }
  catch(err) { console.error(err); fail(target,'دریافت داده پرونده‌ها ممکن نشد. اگر سایت را از فایل باز کرده‌اید، RUN_LOCAL.cmd را اجرا کنید.'); }
});
