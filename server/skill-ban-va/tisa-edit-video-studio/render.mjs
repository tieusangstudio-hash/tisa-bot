
// RENDER_REV: 4
// usage: node render.mjs <compositionId S3|S4|S5> <propsDir> <outDir> sid1 sid2 ...
// Bản nhanh (V3.49, thêm chốt chống treo ở V3.52): dựng song song theo cảnh, nhớ cảnh đã dựng (không đổi thì bỏ qua), khoá chống dựng trùng, kiểm ảnh trước khi dựng,
// và TỰ HUỶ + DỰNG LẠI cảnh nào đứng im không tiến thêm khung nào quá STALL giây (đã gặp: Chrome kẹt, 1 cảnh treo 30 phút ở 0% CPU làm cả video không xong).
// Biến môi trường (đều không bắt buộc):
//   CHROME=/path/to/chrome   (V3.55) Chrome thường bị BỎ QUA vì chậm hơn; chỉ nhận một trình duyệt khác Chrome thường. Muốn ép dùng Chrome thường: FORCE_CHROME=1.
//                            Ép dùng một trình duyệt khác. Mặc định: chrome-headless-shell của Remotion (tự tải 1 lần ~140MB; đã đo nhanh hơn Chrome thường ~1,6 lần).
//                            Chỉ khi không tải được mới rơi về Chrome trong installation-local.json
//   PAR=n    số cảnh dựng cùng lúc (mặc định tự tính theo số nhân CPU: máy 12 nhân = 3)
//   CONC=n   số tab trình duyệt cho MỖI cảnh (mặc định 4 với headless-shell, 2 với Chrome thường)
//   FORCE=1  dựng lại tất cả, bỏ qua bộ nhớ "đã dựng"
//   SEED=1   chỉ ghi nhớ các cảnh đã có file mp4 là "đã dựng" (dùng khi chắc chắn props/mã chưa đổi), không dựng
//   SLOTS=n  tổng số cảnh được dựng cùng lúc TRÊN CẢ MÁY, mọi tiến trình dựng chung một hàng đợi (mặc định máy 12 nhân = 4; đã đo: quá 3-4 cảnh cùng lúc không nhanh thêm, chỉ nghẽn và dễ treo)
//   STALL=n  số giây một cảnh không tiến thêm khung nào thì coi là treo, huỷ và dựng lại (mặc định 150)
//   GL=angle|swangle|null   cách vẽ đồ họa của Chrome (mặc định null)
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition, makeCancelSignal, ensureBrowser} from '@remotion/renderer';
import fs from 'fs'; import path from 'path'; import os from 'os'; import crypto from 'crypto';

const [comp, propsDir, OUT, ...sids] = process.argv.slice(2);
if (!comp || !propsDir || !OUT || !sids.length) { console.log('Cách dùng: node render.mjs <S3|S4|S5> <thư mục props> <thư mục ra> sid1 sid2 ...'); process.exit(1); }
fs.mkdirSync(OUT, {recursive: true});

const localConfigPath = new URL('../installation-local.json', import.meta.url);
const localConfig = fs.existsSync(localConfigPath) ? JSON.parse(fs.readFileSync(localConfigPath, 'utf8')) : {};
// V3.55: nhiều script của AI đặt sẵn CHROME=Chrome thường (chậm hơn ~1,6 lần và chiếm Chrome của người dùng). Bỏ qua nó trừ khi có FORCE_CHROME=1.
const envChrome = process.env.CHROME || '';
const laChromeThuong = /Google Chrome\.app|\/Chromium\.app/i.test(envChrome);
let browserExecutable = (envChrome && (!laChromeThuong || process.env.FORCE_CHROME)) ? envChrome : undefined;
let usingHeadlessShell = false;
if (!browserExecutable) {
  // V3.55: trình duyệt chuyên dụng của Remotion nhanh hơn Chrome thường (cảnh 754 khung: 35-43s so với 55s, và thêm luồng mới có tác dụng). Thiếu thì tải 1 lần.
  try { await ensureBrowser({logLevel: 'warn'}); usingHeadlessShell = true; }
  catch (e) {
    console.log(`Không tải được chrome-headless-shell (${String(e.message || e).split('\n')[0].slice(0, 120)}), dùng Chrome thường.`);
    browserExecutable = (envChrome && fs.existsSync(envChrome) ? envChrome : null) || (localConfig.chrome && fs.existsSync(localConfig.chrome) ? localConfig.chrome : undefined);
  }
}

// ---- số luồng: đã đo trên máy 12 nhân (cảnh 370-720 khung): 1 cảnh dù 2 hay 10 luồng vẫn ~12 khung/giây (nghẽn ở khâu tuần tự),
// nhưng nhiều CẢNH cùng lúc thì nhanh gần tỉ lệ: 1 cảnh 160s, 2 cảnh 88s, 3 cảnh 75s, 4 cảnh 74s. Nên mặc định: vài cảnh cùng lúc, mỗi cảnh 2 luồng. ----
const CPUS = os.cpus().length;
const PAR = Math.max(1, Math.min(sids.length, Number(process.env.PAR) || (CPUS >= 8 ? Math.min(4, Math.floor(CPUS / 4)) : 1)));
const CONC = Math.max(1, Number(process.env.CONC) || (usingHeadlessShell ? 4 : 2));
const SLOTS = Math.max(1, Number(process.env.SLOTS) || (CPUS >= 8 ? Math.min(4, Math.floor(CPUS / 3)) : 1));
const STALL_MS = Math.max(3, Number(process.env.STALL) || 150) * 1000;
const GL = process.env.GL === undefined ? null : (process.env.GL === 'null' ? null : process.env.GL);
const PARAMS = {codec: 'h264', crf: 16, x264Preset: 'veryfast', pixelFormat: 'yuv420p', imageFormat: 'jpeg', jpegQuality: 92, muted: true};

// ---- mã nguồn đồ họa + file public: dùng để biết cảnh có cần dựng lại không ----
const SRC_DIR = path.resolve('src'); const PUB_DIR = path.resolve('public');
const srcText = fs.readdirSync(SRC_DIR).filter(f => /\.(tsx?|jsx?|css)$/.test(f)).sort().map(f => f + '\n' + fs.readFileSync(path.join(SRC_DIR, f), 'utf8')).join('\n');
const srcHash = crypto.createHash('sha1').update(srcText).digest('hex');
const ASSET_RE = /\.(png|jpe?g|webp|gif|svg|mp4|mov|webm|m4v|mp3|wav|m4a|aac|ttf|otf|woff2?)$/i;
function collectAssets(x, out) {
  if (Array.isArray(x)) x.forEach(v => collectAssets(v, out));
  else if (x && typeof x === 'object') Object.values(x).forEach(v => collectAssets(v, out));
  else if (typeof x === 'string' && ASSET_RE.test(x) && !/^(https?:|data:|file:)/i.test(x)) out.add(x.replace(/^\/+/, ''));
}
// Mẫu đồ họa ghi cứng đường dẫn ảnh trong mã nguồn (vd carousel dùng s3/info2..7.png): props chỉ ghi "type": "carousel".
// Lấy mọi 'thư-mục/ảnh.png' viết sẵn trong mã nguồn rồi gắn với tên mẫu đồ họa đứng gần nhất phía trên (đăng ký ở bảng cuối S5/S4 hoặc tên hàm).
function assetsNeededBySource(propsText) {
  const need = new Set();
  for (const m of srcText.matchAll(/img:\s*'((?:s\d+|img)\/[^']+?\.(?:png|jpe?g|webp))'/g)) {
    // chỉ bắt buộc khi cảnh này thật sự dùng mẫu carousel
    if (/"type"\s*:\s*"carousel"/.test(propsText)) need.add(m[1]);
  }
  return need;
}
function preflight(sid, propsText, props) {
  const need = new Set(); collectAssets(props, need); assetsNeededBySource(propsText).forEach(a => need.add(a));
  const missing = [...need].filter(a => !fs.existsSync(path.join(PUB_DIR, a)));
  return {need: [...need], missing};
}

// ---- khoá: hai tiến trình dựng cùng một cảnh thì tiến trình sau CHỜ rồi dùng kết quả, không dựng đè ----
const heldLocks = new Set();
const alive = pid => { try { process.kill(pid, 0); return true; } catch (e) { return e.code === 'EPERM'; } };
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function takeLock(sid) {
  const lf = path.join(OUT, `${sid}.lock`);
  for (let waited = 0; ; waited += 2) {
    try { fs.writeFileSync(lf, JSON.stringify({pid: process.pid, t: Date.now()}), {flag: 'wx'}); heldLocks.add(lf); return {lf, waited}; }
    catch (e) {
      if (e.code !== 'EEXIST') throw e;
      let pid = 0; try { pid = JSON.parse(fs.readFileSync(lf, 'utf8')).pid; } catch (e2) {}
      if (!pid || !alive(pid)) { try { fs.unlinkSync(lf); } catch (e3) {} continue; }
      if (waited === 0) console.log(`${sid} đang được tiến trình ${pid} dựng, em chờ cho xong rồi dùng kết quả (không dựng đè).`);
      if (waited > 3600) throw new Error(`${sid}: chờ tiến trình ${pid} quá 1 giờ`);
      await sleep(2000);
    }
  }
}
function dropLock(lf) { heldLocks.delete(lf); try { fs.unlinkSync(lf); } catch (e) {} }
const cleanup = () => { for (const lf of heldLocks) { try { fs.unlinkSync(lf); } catch (e) {} } };
process.on('exit', cleanup);
for (const s of ['SIGINT', 'SIGTERM', 'SIGHUP']) process.on(s, () => { cleanup(); process.exit(130); });


// ---- hàng đợi chung của cả máy: mở 5 video cùng lúc cũng chỉ có SLOTS cảnh thật sự dựng, cảnh còn lại xếp hàng (V3.52) ----
const SLOT_DIR = path.join(os.tmpdir(), 'tisa-render-slots');
async function takeSlot(sid) {
  fs.mkdirSync(SLOT_DIR, {recursive: true});
  for (let waited = 0; ; waited++) {
    for (let i = 0; i < SLOTS; i++) {
      const sf = path.join(SLOT_DIR, `slot-${i}.lock`);
      try { fs.writeFileSync(sf, JSON.stringify({pid: process.pid, sid, t: Date.now()}), {flag: 'wx'}); heldLocks.add(sf); return sf; }
      catch (e) {
        if (e.code !== 'EEXIST') throw e;
        let pid = 0; try { pid = JSON.parse(fs.readFileSync(sf, 'utf8')).pid; } catch (e2) {}
        if (!pid || !alive(pid)) { try { fs.unlinkSync(sf); } catch (e3) {} i--; }   // chủ ổ đã chết: dọn rồi thử lại đúng ổ này
      }
    }
    if (waited === 0) console.log(`${sid} xếp hàng: máy đang dựng đủ ${SLOTS} cảnh, tới lượt sẽ tự chạy`);
    await sleep(1000);
  }
}
const dropSlot = sf => dropLock(sf);

// ---- chuẩn bị tất cả cảnh trước khi mở Chrome: thiếu ảnh thì báo ngay, không mất 10 phút mới biết ----
const jobs = [];
const problems = [];
for (const sid of sids) {
  const pf = path.join(propsDir, `${sid}.json`);
  if (!fs.existsSync(pf)) { problems.push(`${sid}: không có file ${pf}`); continue; }
  const propsText = fs.readFileSync(pf, 'utf8');
  const inputProps = JSON.parse(propsText);
  const pre = preflight(sid, propsText, inputProps);
  if (pre.missing.length) problems.push(`${sid}: thiếu ${pre.missing.length} tệp trong ${PUB_DIR}: ${pre.missing.join(', ')}`);
  const h = crypto.createHash('sha1').update(comp).update(propsText).update(srcHash).update(JSON.stringify(PARAMS));
  for (const a of pre.need.sort()) { try { const st = fs.statSync(path.join(PUB_DIR, a)); h.update(`${a}:${st.size}:${Math.floor(st.mtimeMs)}`); } catch (e) {} }
  jobs.push({sid, inputProps, hash: h.digest('hex')});
}
if (problems.length) {
  console.log('DỪNG TRƯỚC KHI DỰNG: có tệp ảnh/video thiếu hoặc props hỏng. Sửa xong chạy lại (chưa tốn thời gian dựng).');
  problems.forEach(p => console.log('  - ' + p));
  process.exit(2);
}

const hashFile = sid => path.join(OUT, `${sid}.hash`);
const outFile = sid => path.join(OUT, `${sid}.mp4`);
const upToDate = j => !process.env.FORCE && fs.existsSync(outFile(j.sid)) && fs.existsSync(hashFile(j.sid)) && fs.readFileSync(hashFile(j.sid), 'utf8').trim() === j.hash;

if (process.env.SEED) {
  for (const j of jobs) if (fs.existsSync(outFile(j.sid))) { fs.writeFileSync(hashFile(j.sid), j.hash); console.log(`${j.sid} đã ghi nhớ là đã dựng`); }
  process.exit(0);
}

if (jobs.every(upToDate)) { jobs.forEach(j => console.log(`${j.sid} bỏ qua: đã dựng, không có gì đổi`)); console.log('Tất cả cảnh đã mới nhất, không cần dựng lại.'); process.exit(0); }

console.log(`Dựng ${jobs.length} cảnh · ${PAR} cảnh cùng lúc × ${CONC} luồng (máy ${CPUS} nhân, tối đa ${SLOTS} cảnh cùng lúc trên cả máy, ${usingHeadlessShell ? 'chrome-headless-shell' : 'Chrome thường'})`);
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts'), publicDir: PUB_DIR, onProgress: () => {}});
const NON_RETRY = /Failed to load resource|404|cannot be decoded|EncodingError|ENOENT|Could not find|not found/i;
const chromiumOptions = {gl: GL};

async function runOne(j) {
  const {sid, inputProps} = j;
  if (upToDate(j)) { console.log(`${sid} bỏ qua: đã dựng, không có gì đổi`); return; }
  const {lf, waited} = await takeLock(sid);
  let slotFile = null;
  try {
    if (waited && upToDate(j)) { console.log(`${sid} đã được tiến trình khác dựng xong, dùng luôn`); return; }
    slotFile = await takeSlot(sid);
    // selectComposition cũng có thể kẹt (Chrome không trả lời): giới hạn thời gian, quá hạn thì thử lại tối đa 3 lần.
    let composition = null;
    for (let k = 0; k < 3 && !composition; k++) {
      try {
        composition = await Promise.race([
          selectComposition({serveUrl, id: comp, inputProps, browserExecutable, chromiumOptions}),
          new Promise((_, rej) => setTimeout(() => rej(new Error(`selectComposition treo quá ${STALL_MS / 1000}s`)), STALL_MS)),
        ]);
      } catch (err) { console.log(`${sid} chọn cảnh lần ${k} lỗi: ${err.message}`); if (k === 2 || NON_RETRY.test(err.message)) throw err; }
    }
    const t0 = Date.now(); let last = -1;
    const part = path.join(OUT, `${sid}.part.mp4`);
    for (let attempt = 0; attempt < 3; attempt++) {
      // Chốt chống treo: không tiến thêm khung nào quá STALL_MS thì huỷ và dựng lại cảnh này (không để cả video chờ mãi).
      const {cancelSignal, cancel} = makeCancelSignal();
      let lastTick = Date.now(), lastSig = '', stalled = false;
      const dog = setInterval(() => { if (Date.now() - lastTick > STALL_MS) { stalled = true; clearInterval(dog); cancel(); } }, 3000);
      try {
        await renderMedia({composition, serveUrl, ...PARAMS, outputLocation: part, inputProps, browserExecutable, concurrency: CONC, chromiumOptions, cancelSignal,
          offthreadVideoCacheSizeInBytes: 512 * 1024 * 1024,
          onProgress: ({progress, renderedFrames, encodedFrames}) => {
            const sig = renderedFrames + '/' + encodedFrames; if (sig !== lastSig) { lastSig = sig; lastTick = Date.now(); }
            const p = Math.floor(progress * 4); if (p !== last) { last = p; console.log(`${sid} ${p * 25}%`); }
          }});
        clearInterval(dog);
        break;
      } catch (err) {
        clearInterval(dog);
        const msg = stalled ? `treo: ${STALL_MS / 1000}s không tiến thêm khung nào, đã huỷ` : err.message;
        console.log(`${sid} attempt ${attempt} failed: ${msg}`);
        last = -1;
        if (attempt === 2 || (!stalled && NON_RETRY.test(err.message))) { try { fs.unlinkSync(part); } catch (e) {} throw new Error(msg); }
      }
    }
    fs.renameSync(part, outFile(sid));        // ghi trọn vẹn rồi mới thay file cũ: không bao giờ để lại file dở
    fs.writeFileSync(hashFile(sid), j.hash);
    const sec = (Date.now() - t0) / 1000;
    console.log(`${sid} done ${composition.durationInFrames}f in ${sec.toFixed(1)}s (${(composition.durationInFrames / sec).toFixed(1)} khung/giây)`);
  } finally { if (slotFile) dropSlot(slotFile); dropLock(lf); }
}

let failed = 0; const queue = jobs.slice();
const tAll = Date.now();
await Promise.all(Array.from({length: PAR}, async () => {
  for (let j; (j = queue.shift());) { try { await runOne(j); } catch (err) { failed++; console.log(`${j.sid} LỖI: ${err.message}`); } }
}));
fs.rmSync(serveUrl, {recursive: true, force: true});
console.log(`Xong sau ${((Date.now() - tAll) / 1000).toFixed(0)}s${failed ? `, ${failed} cảnh lỗi` : ''}`);
process.exit(failed ? 1 : 0);
