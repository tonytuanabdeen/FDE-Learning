/**
 * FDE Field Guide: progress tracker backend (Google Apps Script + Google Sheets)
 *
 * SETUP (about 5 minutes)
 * 1. Create a new Google Sheet, e.g. "FDE Onboarding Tracker". Share it ONLY with leadership.
 * 2. Extensions > Apps Script. Replace the contents of Code.gs with this file. Save.
 * 3. Pick `setup` in the function dropdown and click Run. Approve the permissions prompt.
 *    This creates the Dashboard, Learners and Events tabs.
 * 4. Deploy > New deployment > type "Web app".
 *      Execute as: Me
 *      Who has access: Anyone
 *    Copy the Web app URL (ends in /exec).
 * 5. In the guide HTML, paste that URL into TRACKING.endpoint and push to GitHub.
 *
 * After any change to this script: Deploy > Manage deployments > Edit > Version: New version.
 * (Editing the code alone does not update the live /exec URL.)
 */

const CONFIG = {
  ALLOWED_DOMAINS: ['salesforce.com'], // keep in sync with TRACKING.allowedDomains in the HTML
  MAX_BODY_CHARS: 60000,
  MAX_FEEDBACK_CHARS: 2000,
  STALLED_DAYS: 14
};

const STAGES = ['beginner', 'intermediate', 'advanced'];
const STAGE_LABELS = ['Beginner', 'Intermediate', 'Advanced', 'Graduated'];
const SHEETS = { learners: 'Learners', events: 'Events', dashboard: 'Dashboard' };

// Learners column positions (1-based)
const L = {
  email: 1, firstSeen: 2, lastActive: 3, stage: 4, overall: 5,
  beginner: 6, intermediate: 7, advanced: 8,
  begDone: 9, intDone: 10, advDone: 11, tasksDone: 12,
  fbBeg: 13, fbInt: 14, fbAdv: 15, rating: 16, overallFeedback: 17, snapshot: 18
};
const LEARNER_HEADERS = [
  'Email', 'First seen', 'Last active', 'Current stage', 'Overall %',
  'Beginner % (required)', 'Intermediate % (required)', 'Advanced % (required)',
  'Beginner completed', 'Intermediate completed', 'Advanced completed', 'Tasks done',
  'Beginner feedback', 'Intermediate feedback', 'Advanced feedback',
  'Rating', 'Overall Feedback', 'Snapshot (do not edit)'
];
const EVENT_HEADERS = ['Timestamp', 'Email', 'Event', 'Task / stage', 'Stage'];

/* ---------------- One-time setup ---------------- */

function setup() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  migrateLearners_(ss);
  const learners = ensureSheet_(ss, SHEETS.learners, LEARNER_HEADERS);
  learners.hideColumns(L.snapshot);
  learners.setColumnWidth(L.email, 240);
  [L.fbBeg, L.fbInt, L.fbAdv, L.overallFeedback].forEach(c => learners.setColumnWidth(c, 280));
  learners.setColumnWidth(L.rating, 70);
  const events = ensureSheet_(ss, SHEETS.events, EVENT_HEADERS);
  events.setColumnWidth(1, 160);
  events.setColumnWidth(2, 240);
  buildDashboard_(ss);
  const blank = ss.getSheetByName('Sheet1');
  if (blank && blank.getLastRow() === 0 && ss.getSheets().length > 1) ss.deleteSheet(blank);
}

function ensureSheet_(ss, name, headers) {
  const sh = ss.getSheetByName(name) || ss.insertSheet(name);
  sh.getRange(1, 1, 1, headers.length).setValues([headers]).setFontWeight('bold');
  sh.setFrozenRows(1);
  return sh;
}

// Upgrade an existing Learners tab (16-column layout) in place: insert the new
// "Rating" and "Overall Feedback" columns BEFORE the hidden Snapshot column so the
// snapshot JSON and its data shift right intact. Safe to run repeatedly — it no-ops
// once the columns exist, and does nothing on a fresh sheet (ensureSheet_ handles that).
function migrateLearners_(ss) {
  const sh = ss.getSheetByName(SHEETS.learners);
  if (!sh || sh.getLastColumn() === 0) return;
  const hdr = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
  if (hdr.indexOf('Rating') >= 0) return;                // already migrated
  const snapCol = hdr.indexOf('Snapshot (do not edit)') + 1;
  if (snapCol > 0) sh.insertColumnsBefore(snapCol, 2);   // moves Snapshot + its data to col 18
}

function buildDashboard_(ss) {
  let sh = ss.getSheetByName(SHEETS.dashboard);
  if (sh) { sh.getCharts().forEach(c => sh.removeChart(c)); sh.clear(); }
  else sh = ss.insertSheet(SHEETS.dashboard, 0);

  const d = CONFIG.STALLED_DAYS;
  const rows = [
    ['FDE onboarding: leadership summary', ''],
    ['Live from the Field Guide. Per-person detail is on Learners; every tick and untick is on Events.', ''],
    ['', ''],
    ['Headline', 'Value'],
    ['Joiners signed in', '=COUNTA(Learners!A2:A)'],
    ['Active in the last 7 days', '=COUNTIF(Learners!C2:C,">="&(TODAY()-7))'],
    ['Completed Beginner', '=COUNTA(Learners!I2:I)'],
    ['Completed Intermediate', '=COUNTA(Learners!J2:J)'],
    ['Graduated (completed Advanced)', '=COUNTA(Learners!K2:K)'],
    ['Stalled: no activity for ' + d + '+ days, not graduated',
      '=COUNTIFS(Learners!C2:C,"<"&(TODAY()-' + d + '),Learners!D2:D,"<>Graduated")'],
    ['Average overall progress', '=IFERROR(AVERAGE(Learners!E2:E),0)'],
    ['Median days to complete Beginner', '=IFERROR(ROUND(MEDIAN(FILTER(Learners!I2:I-Learners!B2:B,Learners!I2:I<>"")),1),"–")'],
    ['Median days to graduate', '=IFERROR(ROUND(MEDIAN(FILTER(Learners!K2:K-Learners!B2:B,Learners!K2:K<>"")),1),"–")'],
    ['', ''],
    ['Where joiners are now', 'Joiners'],
    ['Beginner', '=COUNTIF(Learners!D2:D,"Beginner")'],
    ['Intermediate', '=COUNTIF(Learners!D2:D,"Intermediate")'],
    ['Advanced', '=COUNTIF(Learners!D2:D,"Advanced")'],
    ['Graduated', '=COUNTIF(Learners!D2:D,"Graduated")']
  ];
  sh.getRange(1, 1, rows.length, 2).setValues(rows);
  sh.getRange('A1').setFontSize(16).setFontWeight('bold');
  sh.getRange('A2').setFontColor('#65718a');
  sh.getRange('A4:B4').setFontWeight('bold').setBackground('#eef1f8');
  sh.getRange('A15:B15').setFontWeight('bold').setBackground('#eef1f8');
  sh.getRange('B11').setNumberFormat('0%');
  sh.setColumnWidth(1, 340);
  sh.setColumnWidth(2, 90);

  // Roster, sorted by progress (lowest first, so people who need help sit at the top)
  sh.getRange('D4:G4').setValues([['Joiner', 'Current stage', 'Overall %', 'Last active']])
    .setFontWeight('bold').setBackground('#eef1f8');
  sh.getRange('D5').setFormula(
    '=IFERROR(SORT(FILTER({Learners!A2:A,Learners!D2:D,Learners!E2:E,Learners!C2:C},Learners!A2:A<>""),3,TRUE),"No joiners yet")');
  sh.getRange('F5:F').setNumberFormat('0%');
  sh.getRange('G5:G').setNumberFormat('yyyy-mm-dd');
  sh.setColumnWidth(4, 240);
  sh.setColumnWidth(5, 120);

  const chart = sh.newChart()
    .setChartType(Charts.ChartType.BAR)
    .addRange(sh.getRange('A15:B19'))
    .setNumHeaders(1)
    .setPosition(21, 1, 0, 0)
    .setOption('title', 'Joiners by current stage')
    .setOption('legend', { position: 'none' })
    .build();
  sh.insertChart(chart);
  sh.setFrozenRows(0);
}

/* ---------------- Web app endpoints ---------------- */

function doPost(e) {
  try {
    // The guide submits a hidden form whose field is named "payload", so the JSON arrives as
    // e.parameter.payload. Fall back to the raw body for clients that POST JSON directly.
    var raw = (e && e.parameter && e.parameter.payload)
      || (e && e.postData && e.postData.contents)
      || '';
    if (!raw) return json_({ ok: false, error: 'No payload' });
    if (raw.length > CONFIG.MAX_BODY_CHARS) return json_({ ok: false, error: 'Payload too large' });
    const body = JSON.parse(raw);
    if (body.action !== 'sync') return json_({ ok: false, error: 'Unknown action' });
    const email = cleanEmail_(body.email);
    if (!email) return json_({ ok: false, error: 'Email domain not allowed' });

    const lock = LockService.getScriptLock();
    lock.waitLock(15000);
    try { return json_(upsert_(email, body)); }
    finally { lock.releaseLock(); }
  } catch (err) {
    return json_({ ok: false, error: String((err && err.message) || err) });
  }
}

// Returns a learner's ticked tasks so progress follows them to a new browser / device.
// The guide reads this over JSONP (a <script> tag): a cross-origin fetch to Apps Script is
// blocked by CORS (no Access-Control-Allow-Origin on the /exec redirect), but a <script>
// tag is CORS-exempt. So when a `callback` param is present we wrap the JSON as callback(...).
// Free-text feedback is deliberately NOT returned: the endpoint is public (anyone could query
// any email). If you want feedback to cross devices too, add `feedback: snap ... ` below and
// accept that privacy trade-off (or lock the web app down to your domain first).
function doGet(e) {
  const p = (e && e.parameter) || {};
  if (p.action !== 'get') return reply_({ ok: true, service: 'fde-field-guide-tracker' }, e);
  const email = cleanEmail_(p.email);
  if (!email) return reply_({ ok: false, error: 'Email domain not allowed' }, e);
  const sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEETS.learners);
  if (!sh) return reply_({ ok: false, error: 'Run setup() first' }, e);
  const row = findRow_(sh, email);
  if (!row) return reply_({ ok: true, found: false }, e);
  const snap = parse_(sh.getRange(row, L.snapshot).getValue()) || {};
  const prog = snap.progress || {};
  return reply_({
    ok: true, found: true,
    progress: Object.keys(prog).map(id => ({ id: id, at: prog[id].at || '' })),
    milestones: snap.milestones || {}
  }, e);
}

/* ---------------- Core write ---------------- */

function upsert_(email, body) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sh = ss.getSheetByName(SHEETS.learners);
  const ev = ss.getSheetByName(SHEETS.events);
  if (!sh || !ev) throw new Error('Run setup() first');

  const now = new Date();
  const existing = findRow_(sh, email);
  const rowNum = existing || sh.getLastRow() + 1;
  const old = existing ? (parse_(sh.getRange(rowNum, L.snapshot).getValue()) || {}) : {};
  const firstSeen = existing ? sh.getRange(rowNum, L.firstSeen).getValue() : now;

  const progress = cleanProgress_(body.progress);
  const stats = body.stats || {};
  const stg = stats.stages || {};
  const reset = body.reason === 'reset';
  const events = [];

  if (!existing) events.push([now, email, 'First visit', '', '']);
  if (reset) events.push([now, email, 'Reset progress', '', '']);

  // Task-level diff against the last snapshot
  const oldP = old.progress || {};
  Object.keys(progress).forEach(id => {
    if (!oldP[id]) events.push([toDate_(progress[id].at) || now, email, 'Ticked', id, progress[id].stage]);
  });
  Object.keys(oldP).forEach(id => {
    if (!progress[id]) events.push([now, email, 'Unticked', id, oldP[id].stage || '']);
  });

  // Stage-level diff + first completion dates
  const oldDone = old.stagesDone || {};
  const stagesDone = {};
  const ms = reset ? {} : (old.milestones || {});
  STAGES.forEach(s => {
    stagesDone[s] = !!(stg[s] && stg[s].done);
    if (stagesDone[s] && !oldDone[s]) events.push([now, email, 'Stage completed', s, s]);
    if (!stagesDone[s] && oldDone[s]) events.push([now, email, 'Stage reopened', s, s]);
    if (stagesDone[s] && !ms[s]) {
      const at = toDate_(stg[s].completedAt);
      ms[s] = (at || now).toISOString();
    }
  });

  const fb = body.feedback || {};
  const stage = STAGE_LABELS.indexOf(stats.currentStage) >= 0 ? stats.currentStage : 'Beginner';
  const row = [
    email, firstSeen, now, stage, pct_(stats.overallPct),
    pct_(stg.beginner && stg.beginner.pct),
    pct_(stg.intermediate && stg.intermediate.pct),
    pct_(stg.advanced && stg.advanced.pct),
    stagesDone.beginner ? toDate_(ms.beginner) : '',
    stagesDone.intermediate ? toDate_(ms.intermediate) : '',
    stagesDone.advanced ? toDate_(ms.advanced) : '',
    Object.keys(progress).length,
    safeText_(fb.beginner), safeText_(fb.intermediate), safeText_(fb.advanced),
    cleanRating_(body.rating), safeText_(body.overallFeedback),
    JSON.stringify({ progress: progress, stagesDone: stagesDone, milestones: ms })
  ];
  sh.getRange(rowNum, 1, 1, row.length).setValues([row]);
  sh.getRange(rowNum, L.firstSeen, 1, 2).setNumberFormat('yyyy-mm-dd hh:mm');
  sh.getRange(rowNum, L.overall, 1, 4).setNumberFormat('0%');
  sh.getRange(rowNum, L.begDone, 1, 3).setNumberFormat('yyyy-mm-dd');

  if (events.length) {
    const start = ev.getLastRow() + 1;
    ev.getRange(start, 1, events.length, EVENT_HEADERS.length).setValues(events);
    ev.getRange(start, 1, events.length, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');
  }
  return { ok: true, events: events.length };
}

/* ---------------- Helpers ---------------- */

function findRow_(sh, email) {
  const last = sh.getLastRow();
  if (last < 2) return 0;
  const hit = sh.getRange(2, L.email, last - 1, 1).createTextFinder(email).matchEntireCell(true).findNext();
  return hit ? hit.getRow() : 0;
}

function cleanEmail_(v) {
  const email = String(v || '').trim().toLowerCase();
  const m = /^[a-z0-9._%+'-]+@([a-z0-9.-]+\.[a-z]{2,})$/.exec(email);
  if (!m) return '';
  if (CONFIG.ALLOWED_DOMAINS.length && CONFIG.ALLOWED_DOMAINS.indexOf(m[1]) < 0) return '';
  return email;
}

function cleanProgress_(list) {
  const out = {};
  const stages = STAGES.concat(['other']);
  (Array.isArray(list) ? list : []).slice(0, 200).forEach(p => {
    if (!p || !/^[A-Za-z0-9_-]{1,60}$/.test(String(p.id))) return;
    out[p.id] = {
      stage: stages.indexOf(p.stage) >= 0 ? p.stage : 'other',
      at: toDate_(p.at) ? String(p.at) : ''
    };
  });
  return out;
}

// Stops spreadsheet formula injection from free-text feedback (=, +, -, @ prefixes).
function safeText_(v) {
  const s = String(v || '').slice(0, CONFIG.MAX_FEEDBACK_CHARS);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function pct_(v) {
  const n = Number(v);
  return isFinite(n) ? Math.max(0, Math.min(1, n)) : 0;
}

// Clamp the star rating to a whole 1–5, or blank if not rated yet.
function cleanRating_(v) {
  const n = Math.round(Number(v));
  return (isFinite(n) && n >= 1 && n <= 5) ? n : '';
}

function toDate_(v) {
  if (!v) return null;
  const d = new Date(v);
  return isNaN(d.getTime()) ? null : d;
}

function parse_(v) {
  try { return v ? JSON.parse(v) : null; } catch (e) { return null; }
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

// JSONP-aware reply: if the request carries a valid `callback` param, return callback(json)
// as JavaScript so a cross-origin <script> read works (CORS-exempt); otherwise plain JSON.
function reply_(obj, e) {
  const body = JSON.stringify(obj);
  const cb = e && e.parameter && e.parameter.callback;
  if (cb && /^[A-Za-z_$][\w$]*$/.test(cb)) { // validate to prevent response injection
    return ContentService.createTextOutput(cb + '(' + body + ')')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService.createTextOutput(body).setMimeType(ContentService.MimeType.JSON);
}
