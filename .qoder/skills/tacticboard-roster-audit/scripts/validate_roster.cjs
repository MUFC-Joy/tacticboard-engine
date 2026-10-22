#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

function arg(name, def) {
  const i = process.argv.indexOf('--' + name);
  return i >= 0 ? process.argv[i + 1] : def;
}
function has(name) {
  return process.argv.includes('--' + name);
}

const ALIAS = { '维拉': '阿斯顿维拉', '森林': '诺丁汉森林', '纽卡': '纽卡斯尔', '纽卡斯尔': '纽卡斯尔' };
const FORM_SLOTS = {
  '4-2-3-1': ['GK', 'RB', 'CB', 'CB', 'LB', 'DM', 'DM', 'RW', 'AM', 'LW', 'ST'],
  '4-3-3': ['GK', 'RB', 'CB', 'CB', 'LB', 'CM', 'DM', 'CM', 'RW', 'ST', 'LW'],
  '3-4-2-1': ['GK', 'CB', 'CB', 'CB', 'RWB', 'CM', 'CM', 'LWB', 'AM', 'AM', 'ST'],
  '4-4-2': ['GK', 'RB', 'CB', 'CB', 'LB', 'RM', 'CM', 'CM', 'LM', 'ST', 'ST'],
  '4-1-4-1': ['GK', 'RB', 'CB', 'CB', 'LB', 'DM', 'RM', 'CM', 'CM', 'LM', 'ST'],
  '3-1-6': ['GK', 'CB', 'CB', 'CB', 'DM', 'LW', 'AM', 'AM', 'RW', 'ST', 'ST'],
  '5-4-1': ['GK', 'CB', 'CB', 'CB', 'RWB', 'LWB', 'RM', 'CM', 'CM', 'LM', 'ST']
};
const ALLOWED_POS = ['GK', 'CB', 'LB', 'RB', 'LWB', 'RWB', 'DM', 'CM', 'AM', 'RM', 'LM', 'LW', 'RW', 'ST'];
const ALLOWED_FOOT = ['左', '右', '双', '待确认', null];
const ALLOWED_CONF = ['已核实', '待确认', '冲突'];
const ALLOWED_WEAK = ['回追慢', '不参与防守', '逆足限制', '防空弱', '体能掉档', '怕一对一', '压迫下失误', '易失位', '纪律差', '伤病史', '终结效率低', '待确认'];
// BIG6 18；其他 14 队 16；曼联 28（用户明确保持）
const ROSTER_TARGET = {
  '曼联': 24, '曼城': 18, '阿森纳': 18, '利物浦': 18, '热刺': 18, '切尔西': 18
};
const DEFAULT_TARGET = 16;

if (has('help') || !arg('team')) {
  console.log('用法: node validate_roster.cjs --team 切尔西 [--form 3-4-2-1] [--candidates /tmp/chelsea.json]');
  process.exit(arg('team') ? 0 : 2);
}

const defaultRoot = fs.existsSync(path.join(process.cwd(), 'src', 'players.js'))
  ? process.cwd()
  : path.resolve(__dirname, '../../../..');
const root = arg('root', defaultRoot);
const team = ALIAS[arg('team')] || arg('team');
const playersFile = path.join(root, 'src', 'players.js');
const dataFile = path.join(root, 'src', 'data.js');

function load(file, expr) {
  const src = fs.readFileSync(file, 'utf8') + '\n' + expr;
  const sandbox = {};
  vm.runInNewContext(src, sandbox, { filename: file });
  return sandbox;
}

let P, D;
try {
  P = load(playersFile, 'globalThis.__P=PLAYERS;').__P;
  D = load(dataFile, 'globalThis.__PL20=PL20; globalThis.__CLUBS=CLUBS;');
} catch (e) {
  console.error('读取 players.js/data.js 失败:', e.message);
  process.exit(2);
}

const PL20 = D.__PL20 || [];
const CLUBS = D.__CLUBS || [];
const byName = {};
P.forEach(p => { byName[p.n] = p; });
const teamPlayers = P.filter(p => p.club === team);
const allowedTags = Array.from(new Set(P.flatMap(p => p.tags || []))).sort();
const issues = [];
const warnings = [];

function out(s) { console.log(s); }
function card() {
  return PL20.find(x => x.name === team) || CLUBS.find(x => x.name === team) || {};
}
function inferForm() {
  const m = (card().sys || '').match(/(\d(?:-\d){1,3})/);
  return m ? m[1] : '4-2-3-1';
}

const form = arg('form', inferForm());
const slots = FORM_SLOTS[form] || [];

out('球队: ' + team);
out('现有球员: ' + teamPlayers.length);
out('阵型: ' + form + (FORM_SLOTS[form] ? '' : '（未知阵型）'));
if (!teamPlayers.length) warnings.push('players.js 里没有该队球员');
if (!slots.length) warnings.push('未知阵型，无法计算槽位');

if (slots.length) {
  const need = {};
  slots.forEach(s => { need[s] = (need[s] || 0) + 1; });
  out('槽位需求 / 现有可打人数（精确位置）:');
  Object.keys(need).forEach(s => {
    const have = teamPlayers.filter(p => (p.pos || []).includes(s)).length;
    out('  ' + s + ': 需要 ' + need[s] + ' / 现有 ' + have);
    if (have < need[s]) warnings.push(s + ' 缺 ' + (need[s] - have) + ' 人（按精确位置计）');
  });
}

function asArray(v) {
  if (v == null) return [];
  return Array.isArray(v) ? v : [v];
}

const candPath = arg('candidates');
let rows = [];
if (candPath) {
  let json;
  try {
    json = JSON.parse(fs.readFileSync(candPath, 'utf8'));
  } catch (e) {
    console.error('候选 JSON 读取失败:', e.message);
    process.exit(2);
  }
  rows = Array.isArray(json) ? json : (json.rows || []);
  out('候选: ' + rows.length + ' 行');
  const seen = {};
  rows.forEach((r, i) => {
    const tag = '#' + (i + 1) + ' ' + (r.n || '(无名字)');
    if (!r.n) issues.push(tag + ': 缺 n');
    if (!asArray(r.en).length) warnings.push(tag + ': 缺英文/别名 en');
    if (!r.club) issues.push(tag + ': 缺 club');
    else if (r.club !== team) issues.push(tag + ': club=' + r.club + ' 与 --team=' + team + ' 不符');
    const pos = asArray(r.pos);
    if (!pos.length) issues.push(tag + ': 缺 pos');
    pos.forEach(p => { if (!ALLOWED_POS.includes(p)) issues.push(tag + ': 非法位置 ' + p); });
    if (!('foot' in r) || !ALLOWED_FOOT.includes(r.foot)) issues.push(tag + ': 非法惯用脚 ' + JSON.stringify(r.foot));
    const tags = asArray(r.tags);
    if (!tags.length) warnings.push(tag + ': 缺 tags');
    tags.forEach(t => { if (!allowedTags.includes(t)) issues.push(tag + ': 未在现有词表里的标签 ' + t); });
    const src = asArray(r.src);
    if (!src.length) issues.push(tag + ': 缺来源 URL');
    src.forEach(u => { if (!/^https?:\/\//.test(String(u))) issues.push(tag + ': 来源不是 URL ' + u); });
    if (!ALLOWED_CONF.includes(r.conf)) issues.push(tag + ': conf 需为 已核实/待确认/冲突');
    if (r.weak && !ALLOWED_WEAK.includes(r.weak)) warnings.push(tag + ': 弱点不在词表 ' + r.weak);
    if (!r.weak || r.weak === '待确认') {
      if (!r.weakNote || String(r.weakNote).trim().length < 6) {
        issues.push(tag + ': 弱点未研究；补 weak 或 weakNote（依据/无可靠来源说明）');
      }
    } else if (!r.weakNote) {
      warnings.push(tag + ': 建议补 weakNote（弱点依据）');
    }
    if (byName[r.n]) issues.push(tag + ': 已在 players.js（' + byName[r.n].club + '）');
    if (seen[r.n]) issues.push(tag + ': 候选内重名');
    seen[r.n] = 1;
  });
  const add = rows.filter(r => r.n && !byName[r.n]).length;
  const target = ROSTER_TARGET[team] || DEFAULT_TARGET;
  out('预计补后人数: ' + (teamPlayers.length + add) + ' / 目标 ' + target);
  if (teamPlayers.length + add < target) warnings.push('补后不足目标 ' + target + ' 人，可能缺少替补/位置深度');
  if (teamPlayers.length + add > target) warnings.push('补后超过目标 ' + target + ' 人，检查是否重复/超编/已离队未移出');
}

out('');
if (issues.length) {
  out('阻断问题:');
  issues.forEach(x => out('  ✗ ' + x));
}
if (warnings.length) {
  out('提醒:');
  warnings.forEach(x => out('  ! ' + x));
}
if (!issues.length && !warnings.length) out('通过: 没有发现 schema 问题');
out('');
out('已读: src/players.js / src/data.js；未写入任何文件');
process.exit(issues.length ? 1 : 0);
