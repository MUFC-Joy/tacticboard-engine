#!/usr/bin/env node
'use strict';

const fs = require('fs');

const input = process.argv[2];
const output = process.argv[3];
if (!input || !output) {
  console.error('用法: node make_review.cjs <candidates.json> <review.html>');
  process.exit(2);
}

let data;
try {
  data = JSON.parse(fs.readFileSync(input, 'utf8'));
} catch (e) {
  console.error('候选 JSON 读取失败:', e.message);
  process.exit(2);
}
if (Array.isArray(data)) data = { team: '球队', form: '', rows: data };
const team = data.team || '球队';
const form = data.form || '';
const rows = Array.isArray(data.rows) ? data.rows : [];

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, m => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[m]));
}
function list(v) {
  return Array.isArray(v) ? v.filter(Boolean).join(' / ') : (v || '');
}
function links(v) {
  const arr = Array.isArray(v) ? v : (v ? [v] : []);
  if (!arr.length) return '<span class="muted">无来源</span>';
  return arr.map((u, i) => '<a href="' + esc(u) + '" target="_blank" rel="noopener">来源 ' + (i + 1) + '</a>').join(' · ');
}
function badge(conf) {
  if (conf === '已核实') return '<span class="badge ok">已核实</span>';
  if (conf === '冲突') return '<span class="badge bad">冲突</span>';
  return '<span class="badge warn">待确认</span>';
}

const cards = rows.map((r, i) => {
  const tags = (Array.isArray(r.tags) ? r.tags : []).map(t => '<span class="tag">' + esc(t) + '</span>').join('');
  return `
<section class="card" data-card="${i}">
  <div class="top"><b>${esc(r.n || '未命名')}</b>${badge(r.conf)}</div>
  <div class="en">${esc(list(r.en))}</div>
  <div class="meta">
    <span class="kv">位置 <b>${esc(list(r.pos) || '待确认')}</b></span>
    <span class="kv">惯用脚 <b>${esc(r.foot || '待确认')}</b></span>
  </div>
  <div class="tags">${tags || '<span class="muted">标签待确认</span>'}</div>
  <div class="weak">弱点：${esc(r.weak || '待确认')}</div>
  ${r.weakNote ? '<div class="weaknote">弱点依据：' + esc(r.weakNote) + '</div>' : ''}
  ${r.note ? '<div class="note">备注：' + esc(r.note) + '</div>' : ''}
  <div class="src">${links(r.src)}</div>
  <label class="check"><input type="checkbox" data-check="${i}"> <span>确认这行，写入 players.js</span></label>
  <input class="memo" data-memo="${i}" placeholder="要改哪格？例如：脚改成左；标签删掉攻击型">
</section>`;
}).join('');

const dataJson = JSON.stringify(data).replace(/</g, '\\u003c');
const html = `<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>${esc(team)} · 球员审核</title>
<style>
:root{--bg:#0c1015;--card:#151a21;--card2:#1b222c;--line:#2a323d;--txt:#e8eef5;--mut:#93a0af;
--green:#23c55e;--red:#e2383f;--amber:#f0b429;--blue:#4ea1ff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--txt);font:14px/1.55 -apple-system,BlinkMacSystemFont,"PingFang SC",Roboto,"Microsoft YaHei",sans-serif}
main{max-width:520px;margin:0 auto;padding:14px 12px 96px}
header{padding:4px 2px 10px}
h1{font-size:19px;margin:0 0 4px}
.sub{font-size:12px;color:var(--mut);line-height:1.6}
.legend{font-size:11px;color:var(--mut);margin-top:8px}
.badge{display:inline-block;font-size:10px;border:1px solid;border-radius:99px;padding:1px 7px;margin-left:6px;white-space:nowrap}
.badge.ok{color:#8ef0b3;border-color:rgba(35,197,94,.5);background:rgba(35,197,94,.1)}
.badge.warn{color:#f5d28a;border-color:rgba(240,180,41,.5);background:rgba(240,180,41,.1)}
.badge.bad{color:#ffb4b7;border-color:rgba(226,56,63,.5);background:rgba(226,56,63,.1)}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:13px;margin:0 0 10px}
.card.done{border-color:rgba(35,197,94,.55)}
.top{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:15px}
.en{font-size:11px;color:var(--mut);margin-top:2px;overflow-wrap:anywhere}
.meta{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;margin-top:8px}
.kv{color:var(--mut)}
.kv b{color:var(--txt);font-weight:700}
.tags{display:flex;gap:5px;flex-wrap:wrap;margin-top:8px}
.tag{font-size:10.5px;color:#a8d2ff;background:rgba(78,161,255,.12);border:1px solid rgba(78,161,255,.35);border-radius:99px;padding:2px 7px}
.weak{font-size:12px;color:#d3dce6;margin-top:8px}
.weaknote{font-size:11px;color:#8fa3b8;margin-top:4px;line-height:1.55}
.note{font-size:11.5px;color:#b9c6d3;margin-top:6px;background:rgba(255,255,255,.03);border-radius:6px;padding:6px 8px}
.src{font-size:11px;color:var(--mut);margin-top:8px;overflow-wrap:anywhere}
.src a{color:#a8d2ff;text-decoration:none;margin-right:4px}
.muted{color:#6b7887}
.check{display:flex;align-items:center;gap:9px;margin-top:11px;border-top:1px dashed #ffffff14;padding-top:10px;font-size:12.5px;min-height:42px}
.check input{width:22px;height:22px;accent-color:var(--green);flex:0 0 22px}
.memo{display:block;width:100%;margin-top:8px;background:var(--card2);border:1px solid var(--line);color:var(--txt);
border-radius:8px;padding:10px;font:12px/1.5 inherit;min-height:40px}
.memo::placeholder{color:#6b7887}
footer{position:fixed;left:0;right:0;bottom:0;background:rgba(12,16,21,.97);border-top:1px solid var(--line);
padding:10px 12px calc(10px + env(safe-area-inset-bottom));z-index:9}
.fbar{max-width:520px;margin:0 auto;display:flex;gap:8px;align-items:center}
.count{font-size:12px;color:var(--mut);flex:0 0 auto;min-width:80px}
.count b{color:#fff}
button{font:13px/1.2 inherit;border-radius:9px;min-height:42px;padding:10px 12px;border:1px solid var(--line);
background:var(--card2);color:var(--txt)}
button.primary{background:rgba(35,197,94,.16);border-color:rgba(35,197,94,.55);color:#dfffe9;font-weight:700}
button:active{transform:scale(.98)}
#fallback{display:none;margin-top:8px}
#fallback textarea{width:100%;height:90px;background:var(--card2);border:1px solid var(--line);color:var(--txt);
border-radius:8px;padding:8px;font:11px/1.5 ui-monospace,Menlo,monospace}
.toast{position:fixed;left:50%;bottom:70px;transform:translateX(-50%);background:#1f2a35;border:1px solid #3a4a5a;
color:#fff;border-radius:99px;padding:7px 13px;font-size:12px;opacity:0;pointer-events:none;transition:opacity .2s;z-index:20}
.toast.on{opacity:1}
@media(min-width:521px){main{padding-top:20px}}
</style></head>
<body>
<main>
<header>
  <h1>${esc(team)} · 球员审核</h1>
  <div class="sub">${esc(form || '阵型待确认')} · ${rows.length} 行候选 · 勾选=同意写入；不勾=不写。<br>
  要改的写在备注里。底栏下载的 JSON 只包含已勾选行。</div>
  <div class="legend">${badge('已核实')} 来源较硬 · ${badge('待确认')} 需你判断 · ${badge('冲突')} 来源互相矛盾</div>
</header>
${cards}
<div id="fallback"><textarea id="copyBox" readonly></textarea></div>
</main>
<footer><div class="fbar">
  <div class="count">已确认 <b id="cnt">0</b>/${rows.length}</div>
  <button class="primary" id="download">下载确认 JSON</button>
  <button id="copy">复制</button>
</div></footer>
<div class="toast" id="toast">已复制</div>
<script>
const DATA = ${dataJson};
const rows = Array.isArray(DATA.rows) ? DATA.rows : [];
const boxes = Array.prototype.slice.call(document.querySelectorAll('[data-check]'));
const memos = Array.prototype.slice.call(document.querySelectorAll('[data-memo]'));
const cards = Array.prototype.slice.call(document.querySelectorAll('[data-card]'));
const cnt = document.getElementById('cnt');
function selected() {
  return rows.map(function(r, i) {
    if (!boxes[i] || !boxes[i].checked) return null;
    const out = Object.assign({}, r);
    const memo = (memos[i] && memos[i].value || '').trim();
    if (memo) out.reviewNote = memo;
    out.confirmed = true;
    return out;
  }).filter(Boolean);
}
function update() {
  let n = 0;
  boxes.forEach(function(b, i) {
    if (b.checked) n++;
    cards[i].classList.toggle('done', b.checked);
  });
  cnt.textContent = String(n);
}
boxes.forEach(function(b) { b.addEventListener('change', update); });
update();
function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('on');
  setTimeout(function() { t.classList.remove('on'); }, 1400);
}
document.getElementById('download').addEventListener('click', function() {
  const payload = { team: DATA.team || '', form: DATA.form || '', rows: selected() };
  if (!payload.rows.length) { toast('先勾选至少一行'); return; }
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = (DATA.team || 'team') + '-confirmed.json';
  document.body.appendChild(a);
  a.click();
  setTimeout(function() { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  toast('已下载 ' + payload.rows.length + ' 行');
});
document.getElementById('copy').addEventListener('click', function() {
  const payload = { team: DATA.team || '', form: DATA.form || '', rows: selected() };
  if (!payload.rows.length) { toast('先勾选至少一行'); return; }
  const text = JSON.stringify(payload, null, 2);
  const fallback = document.getElementById('fallback');
  const box = document.getElementById('copyBox');
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(function() { toast('已复制'); }).catch(function() {
      box.value = text; fallback.style.display = 'block'; box.focus(); box.select(); toast('请手动复制');
    });
  } else {
    box.value = text; fallback.style.display = 'block'; box.focus(); box.select(); toast('请手动复制');
  }
});
</script>
</body></html>`;

try {
  fs.writeFileSync(output, html);
  console.log('已生成 ' + output + '（' + rows.length + ' 行）');
} catch (e) {
  console.error('写入审查页失败:', e.message);
  process.exit(1);
}
