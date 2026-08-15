/* ============================================================
   手写转 Excel 工作台
   流程：上传 → OCR 识别 → 强制逐行复核 → 导出
   保证：导出前每一行都必须经人工确认（强制门槛）
   ============================================================ */

"use strict";

/* ---------- 状态 ---------- */

const state = {
  step: 1,
  enhanced: true,
  images: [], // { id, file, name, size, url, status: pending|running|done|error, progress, lines: [], scale }
  activeImageId: null,
  filter: "all",
  recognizing: false,
};

let uid = 0;
const nextId = () => ++uid;
const LOW_CONF = 60;

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => [...document.querySelectorAll(sel)];

const els = {
  stepper: $("#stepper"),
  dropzone: $("#dropzone"),
  fileInput: $("#file-input"),
  thumbGrid: $("#thumb-grid"),
  btnToRecognize: $("#btn-to-recognize"),
  uploadHint: $("#upload-hint"),
  enhanceToggle: $("#enhance-toggle"),
  btnStartRecognize: $("#btn-start-recognize"),
  recognizeHint: $("#recognize-hint"),
  progressList: $("#progress-list"),
  btnBackUpload: $("#btn-back-upload"),
  btnToReview: $("#btn-to-review"),
  reviewProgress: $("#review-progress"),
  imageStrip: $("#image-strip"),
  viewerFilename: $("#viewer-filename"),
  zoomRange: $("#zoom-range"),
  zoomVal: $("#zoom-val"),
  zoomIn: $("#zoom-in"),
  zoomOut: $("#zoom-out"),
  viewerScroll: $("#viewer-scroll"),
  viewerCanvas: $("#viewer-canvas"),
  viewerImg: $("#viewer-img"),
  viewerOverlay: $("#viewer-overlay"),
  filterGroup: $("#filter-group"),
  btnAddLine: $("#btn-add-line"),
  linesList: $("#lines-list"),
  btnBackRecognize: $("#btn-back-recognize"),
  btnToExport: $("#btn-to-export"),
  exportSummary: $("#export-summary"),
  previewTable: $("#preview-table"),
  btnBackReview: $("#btn-back-review"),
  btnExport: $("#btn-export"),
  btnRestart: $("#btn-restart"),
  toastViewport: $("#toast-viewport"),
};

/* ---------- 工具 ---------- */

function toast(msg, type = "") {
  const t = document.createElement("div");
  t.className = `toast ${type}`;
  t.textContent = msg;
  els.toastViewport.appendChild(t);
  setTimeout(() => {
    t.style.transition = "opacity .3s";
    t.style.opacity = "0";
    setTimeout(() => t.remove(), 300);
  }, 2600);
}

function fmtSize(bytes) {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(0) + " KB";
  return (bytes / 1024 / 1024).toFixed(1) + " MB";
}

function getActiveImage() {
  return state.images.find((i) => i.id === state.activeImageId) || null;
}

/* ---------- 步骤导航 ---------- */

function goStep(n) {
  state.step = n;
  $$(".panel").forEach((p) => p.classList.add("hidden"));
  $(`#step-${n}`).classList.remove("hidden");
  renderStepper();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function renderStepper() {
  $$(".step").forEach((btn) => {
    const n = +btn.dataset.step;
    btn.classList.toggle("is-active", n === state.step);
    btn.classList.toggle("is-done", n < state.step);
    btn.disabled = n > state.step;
  });
}

els.stepper.addEventListener("click", (e) => {
  const btn = e.target.closest(".step");
  if (!btn || btn.disabled) return;
  const n = +btn.dataset.step;
  if (n === 4 && !allVerified()) return; // 强制门槛
  if (n === 3 && !recognitionReady()) return;
  if (n === 2 && state.images.length === 0) return;
  goStep(n);
});

/* ============================================================
   步骤 1：上传
   ============================================================ */

els.dropzone.addEventListener("click", () => els.fileInput.click());
els.dropzone.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") {
    e.preventDefault();
    els.fileInput.click();
  }
});

["dragenter", "dragover"].forEach((ev) =>
  els.dropzone.addEventListener(ev, (e) => {
    e.preventDefault();
    els.dropzone.classList.add("is-drag");
  })
);
["dragleave", "drop"].forEach((ev) =>
  els.dropzone.addEventListener(ev, (e) => {
    e.preventDefault();
    els.dropzone.classList.remove("is-drag");
  })
);
els.dropzone.addEventListener("drop", (e) => addFiles(e.dataTransfer.files));

els.fileInput.addEventListener("change", () => {
  addFiles(els.fileInput.files);
  els.fileInput.value = "";
});

function addFiles(fileList) {
  const files = [...fileList].filter((f) => f.type.startsWith("image/"));
  const skipped = fileList.length - files.length;
  if (skipped > 0) toast(`已跳过 ${skipped} 个非图片文件`, "err");
  if (files.length === 0) return;

  files.forEach((file) => {
    state.images.push({
      id: nextId(),
      file,
      name: file.name,
      size: file.size,
      url: URL.createObjectURL(file),
      status: "pending",
      progress: 0,
      lines: [],
      scale: 1,
      error: "",
    });
  });
  renderThumbs();
  toast(`已添加 ${files.length} 张图片`);
}

function renderThumbs() {
  els.thumbGrid.innerHTML = "";
  state.images.forEach((img, idx) => {
    const el = document.createElement("div");
    el.className = "thumb";
    el.innerHTML = `
      <img class="thumb-img" src="${img.url}" alt="" />
      <div class="thumb-name" title="${esc(img.name)}">${esc(img.name)}</div>
      <div class="thumb-meta">${idx + 1} · ${fmtSize(img.size)}</div>
      <div class="thumb-ops">
        <button class="thumb-op" data-op="left" title="前移">←</button>
        <button class="thumb-op" data-op="right" title="后移">→</button>
        <button class="thumb-op danger" data-op="del" title="移除">✕</button>
      </div>`;
    el.addEventListener("click", (e) => {
      const op = e.target.closest(".thumb-op")?.dataset.op;
      if (!op) return;
      const i = state.images.indexOf(img);
      if (op === "del") {
        if (!confirm(`确定移除「${img.name}」吗？`)) return;
        URL.revokeObjectURL(img.url);
        state.images.splice(i, 1);
      } else if (op === "left" && i > 0) {
        [state.images[i - 1], state.images[i]] = [state.images[i], state.images[i - 1]];
      } else if (op === "right" && i < state.images.length - 1) {
        [state.images[i + 1], state.images[i]] = [state.images[i], state.images[i + 1]];
      }
      renderThumbs();
    });
    els.thumbGrid.appendChild(el);
  });

  const has = state.images.length > 0;
  els.btnToRecognize.disabled = !has;
  els.uploadHint.textContent = has
    ? `共 ${state.images.length} 张图片，顺序即识别顺序（可用 ← → 调整）`
    : "请先添加至少一张图片";
  els.uploadHint.classList.toggle("warn", false);
}

els.btnToRecognize.addEventListener("click", () => {
  if (state.images.length === 0) return;
  goStep(2);
  renderProgressList();
});

/* ============================================================
   步骤 2：OCR 识别
   ============================================================ */

els.enhanceToggle.addEventListener("change", () => {
  state.enhanced = els.enhanceToggle.checked;
  if (state.images.some((i) => i.status === "done")) {
    els.recognizeHint.textContent = "增强设置将在下次识别时生效";
  }
});

els.btnBackUpload.addEventListener("click", () => goStep(1));

els.btnStartRecognize.addEventListener("click", async () => {
  if (state.recognizing) return;
  if (state.images.length === 0) return;

  const anyDone = state.images.some((i) => i.status === "done");
  if (
    anyDone &&
    !confirm("重新识别会清空已有的识别与核对结果，确定继续吗？")
  )
    return;

  state.recognizing = true;
  els.btnStartRecognize.disabled = true;
  els.btnStartRecognize.textContent = "识别中…";

  try {
    const worker = await getWorker();
    for (const img of state.images) {
      if (img.status === "done" && !anyDone) continue;
      await recognizeOne(worker, img);
    }
  } catch (err) {
    console.error(err);
    toast("识别失败：" + (err.message || err), "err");
  } finally {
    state.recognizing = false;
    els.btnStartRecognize.disabled = false;
    els.btnStartRecognize.textContent = "开始识别";
    renderProgressList();
    updateReviewEntry();
  }
});

let _worker = null;
async function getWorker() {
  if (_worker) return _worker;
  if (typeof Tesseract === "undefined") {
    throw new Error("OCR 引擎（Tesseract.js）未加载，请检查网络后刷新页面");
  }
  toast("首次使用需下载识别模型（约 15MB），请稍候…");
  _worker = await Tesseract.createWorker(["chi_sim", "eng"], 1, {
    logger: (m) => {
      if (m.status === "recognizing text" && m.progress != null) {
        const img = state.images.find((i) => i.status === "running");
        if (img) {
          img.progress = m.progress;
          updateProgressCard(img);
        }
      } else if (m.status === "loading language traineddata" && m.progress != null) {
        els.recognizeHint.textContent = `正在下载识别模型… ${Math.round(m.progress * 100)}%`;
      }
    },
  });
  return _worker;
}

/* 图像增强：灰度 + 2%~98% 对比度拉伸 + 小图放大 */
async function preprocess(img) {
  const bitmap = await createImageBitmap(img.file);
  const scale = state.enhanced
    ? bitmap.width < 1000
      ? Math.min(2.5, 1000 / bitmap.width)
      : 1
    : 1;
  const w = Math.round(bitmap.width * scale);
  const h = Math.round(bitmap.height * scale);
  const canvas = document.createElement("canvas");
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  ctx.drawImage(bitmap, 0, 0, w, h);
  bitmap.close?.();

  if (state.enhanced && w * h <= 16e6) {
    const data = ctx.getImageData(0, 0, w, h);
    const px = data.data;
    const hist = new Uint32Array(256);
    for (let i = 0; i < px.length; i += 4) {
      const g = (px[i] * 299 + px[i + 1] * 587 + px[i + 2] * 114) / 1000 | 0;
      px[i] = px[i + 1] = px[i + 2] = g;
      hist[g]++;
    }
    const total = w * h;
    let lo = 0, hi = 255, acc = 0;
    for (let v = 0; v < 256; v++) { acc += hist[v]; if (acc >= total * 0.02) { lo = v; break; } }
    acc = 0;
    for (let v = 255; v >= 0; v--) { acc += hist[v]; if (acc >= total * 0.02) { hi = v; break; } }
    if (hi > lo) {
      const range = hi - lo;
      const lut = new Uint8ClampedArray(256);
      for (let v = 0; v < 256; v++) lut[v] = ((v - lo) / range) * 255;
      for (let i = 0; i < px.length; i += 4) {
        px[i] = px[i + 1] = px[i + 2] = lut[px[i]];
      }
    }
    ctx.putImageData(data, 0, 0);
  }
  return { canvas, scale };
}

async function recognizeOne(worker, img) {
  img.status = "running";
  img.progress = 0;
  img.error = "";
  renderProgressList();
  try {
    const { canvas, scale } = await preprocess(img);
    img.scale = scale;
    const { data } = await worker.recognize(canvas, {}, { blocks: true, text: true });
    img.lines = parseLines(data, scale);
    img.status = "done";
    img.progress = 1;
  } catch (err) {
    console.error(err);
    img.status = "error";
    img.error = err.message || String(err);
  }
  updateProgressCard(img);
}

/* 从 Tesseract 结果提取行（带回原坐标系的包围盒） */
function parseLines(data, scale) {
  const lines = [];
  const push = (text, conf, bbox) => {
    const t = (text || "").replace(/\s+$/g, "").trim();
    if (!t) return;
    lines.push({
      id: nextId(),
      text: t,
      conf: conf == null ? null : Math.round(conf),
      bbox: bbox
        ? {
            x0: bbox.x0 / scale,
            y0: bbox.y0 / scale,
            x1: bbox.x1 / scale,
            y1: bbox.y1 / scale,
          }
        : null,
      status: "unverified",
      edited: false,
      manual: false,
    });
  };

  try {
    const blocks = data.blocks || [];
    for (const b of blocks)
      for (const p of b.paragraphs || [])
        for (const ln of p.lines || []) {
          const words = ln.words || [];
          let bbox = null;
          if (words.length) {
            bbox = words.reduce(
              (a, w) => ({
                x0: Math.min(a.x0, w.bbox.x0),
                y0: Math.min(a.y0, w.bbox.y0),
                x1: Math.max(a.x1, w.bbox.x1),
                y1: Math.max(a.y1, w.bbox.y1),
              }),
              { x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity }
            );
          }
          push(ln.text, ln.confidence, bbox);
        }
  } catch (e) {
    console.warn("解析 OCR 结构失败，退回纯文本行", e);
  }

  if (lines.length === 0 && data.text) {
    (data.text || "").split(/\n+/).forEach((t) => push(t, data.confidence, null));
  }
  return lines;
}

function renderProgressList() {
  els.progressList.innerHTML = "";
  state.images.forEach((img) => els.progressList.appendChild(progressCardEl(img)));
  updateReviewEntry();
}

function progressCardEl(img) {
  const el = document.createElement("div");
  el.className = "progress-card" + (img.status === "error" ? " is-error" : "");
  el.dataset.img = img.id;

  const statusMap = {
    pending: "等待中",
    running: `${Math.round((img.progress || 0) * 100)}%`,
    done: `${img.lines.length} 行`,
    error: "失败",
  };
  const cls =
    img.status === "done" ? "ok" : img.status === "error" ? "err" : "";

  el.innerHTML = `
    <img class="pc-thumb" src="${img.url}" alt="" />
    <div class="pc-main">
      <div class="pc-name">${esc(img.name)}</div>
      <div class="pc-bar"><div class="pc-bar-fill" style="width:${img.status === "done" ? 100 : (img.progress || 0) * 100}%"></div></div>
    </div>
    <span class="pc-status ${cls}">${statusMap[img.status] || ""}</span>`;

  if (img.status === "error") {
    const retry = document.createElement("button");
    retry.className = "btn-mini";
    retry.textContent = "重试";
    retry.style.marginLeft = "8px";
    retry.addEventListener("click", async () => {
      try {
        const worker = await getWorker();
        await recognizeOne(worker, img);
      } catch (err) {
        toast("重试失败：" + (err.message || err), "err");
      }
      updateReviewEntry();
    });
    el.appendChild(retry);
  }
  return el;
}

function updateProgressCard(img) {
  const old = els.progressList.querySelector(`[data-img="${img.id}"]`);
  if (old) els.progressList.replaceChild(progressCardEl(img), old);
}

function recognitionReady() {
  return (
    state.images.length > 0 &&
    state.images.every((i) => i.status === "done" || i.status === "error")
  );
}

function updateReviewEntry() {
  const ok = recognitionReady() && !state.recognizing;
  const errCount = state.images.filter((i) => i.status === "error").length;
  els.btnToReview.disabled = !ok || errCount > 0;
  els.recognizeHint.textContent = !ok
    ? ""
    : errCount > 0
    ? `⚠ 有 ${errCount} 张识别失败，请重试或返回上一步移除`
    : "识别完成，请进入复核";
  els.recognizeHint.classList.toggle("warn", ok && errCount > 0);
}

els.btnToReview.addEventListener("click", () => {
  if (!recognitionReady()) return;
  const first = state.images.find((i) => i.status === "done");
  if (!first) return;
  state.activeImageId = first.id;
  state.filter = "all";
  goStep(3);
  renderReview();
});

/* ============================================================
   步骤 3：逐行复核（强制）
   ============================================================ */

els.btnBackRecognize.addEventListener("click", () => goStep(2));

els.filterGroup.addEventListener("click", (e) => {
  const btn = e.target.closest(".filter");
  if (!btn) return;
  state.filter = btn.dataset.filter;
  $$(".filter").forEach((f) => f.classList.toggle("is-active", f === btn));
  renderLines();
});

els.imageStrip.addEventListener("click", (e) => {
  const tab = e.target.closest(".img-tab");
  if (!tab) return;
  state.activeImageId = +tab.dataset.img;
  renderReview();
});

els.btnAddLine.addEventListener("click", () => {
  const img = getActiveImage();
  if (!img) return;
  const line = {
    id: nextId(),
    text: "",
    conf: null,
    bbox: null,
    status: "unverified",
    edited: true,
    manual: true,
  };
  img.lines.push(line);
  renderLines();
  const row = els.linesList.querySelector(`[data-line="${line.id}"]`);
  if (row) startEdit(line.id, row);
});

function renderReview() {
  renderImageStrip();
  renderViewer();
  renderLines();
  updateReviewStats();
  updateExportEntry();
}

function renderImageStrip() {
  els.imageStrip.innerHTML = "";
  state.images.forEach((img) => {
    if (img.status !== "done") return;
    const total = img.lines.length;
    const done = img.lines.filter((l) => l.status === "verified").length;
    const all = total > 0 && done === total;
    const tab = document.createElement("button");
    tab.className = "img-tab" + (img.id === state.activeImageId ? " is-active" : "");
    tab.dataset.img = img.id;
    tab.innerHTML = `
      <img src="${img.url}" alt="" />
      <span>${esc(img.name)}</span>
      <span class="done-dot">${all ? "✓" : `${done}/${total}`}</span>`;
    els.imageStrip.appendChild(tab);
  });
}

/* ---------- 原图查看器 ---------- */

function renderViewer() {
  const img = getActiveImage();
  if (!img) return;
  els.viewerFilename.textContent = img.name;
  els.viewerImg.src = img.url;
  const sync = () => {
    const { naturalWidth: w, naturalHeight: h } = els.viewerImg;
    if (!w) return;
    els.viewerOverlay.setAttribute("viewBox", `0 0 ${w} ${h}`);
    drawOverlay(null);
    applyZoom();
  };
  els.viewerImg.onload = sync;
  if (els.viewerImg.complete) sync();
}

function applyZoom() {
  const z = (+els.zoomRange.value || 100) / 100;
  els.viewerImg.style.width = `${els.viewerImg.naturalWidth * z}px`;
  els.zoomVal.textContent = `${els.zoomRange.value}%`;
}

els.zoomRange.addEventListener("input", applyZoom);
els.zoomIn.addEventListener("click", () => {
  els.zoomRange.value = Math.min(300, +els.zoomRange.value + 20);
  applyZoom();
});
els.zoomOut.addEventListener("click", () => {
  els.zoomRange.value = Math.max(30, +els.zoomRange.value - 20);
  applyZoom();
});

/* 在原图上绘制某行的位置框 */
function drawOverlay(line) {
  const svg = els.viewerOverlay;
  svg.innerHTML = "";
  if (!line || !line.bbox) return;
  const b = line.bbox;
  const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  rect.setAttribute("class", "line-box");
  rect.setAttribute("x", b.x0 - 4);
  rect.setAttribute("y", b.y0 - 4);
  rect.setAttribute("width", b.x1 - b.x0 + 8);
  rect.setAttribute("height", b.y1 - b.y0 + 8);
  svg.appendChild(rect);
  // 滚动到该行位置
  const z = (+els.zoomRange.value || 100) / 100;
  els.viewerScroll.scrollTo({
    top: Math.max(0, b.y0 * z - els.viewerScroll.clientHeight / 3),
    behavior: "smooth",
  });
}

/* ---------- 行列表 ---------- */

function linePassesFilter(line) {
  if (state.filter === "unverified") return line.status !== "verified";
  if (state.filter === "low")
    return line.conf != null && line.conf < LOW_CONF && line.status !== "verified";
  return true;
}

function confBadge(line) {
  if (line.manual || line.conf == null)
    return `<span class="conf conf-manual">人工添加</span>`;
  const cls = line.conf >= 80 ? "high" : line.conf >= LOW_CONF ? "mid" : "low";
  return `<span class="conf conf-${cls}">${line.conf}%</span>`;
}

function renderLines() {
  els.linesList.innerHTML = "";
  const img = getActiveImage();
  if (!img) return;
  const lines = img.lines;

  if (lines.length === 0) {
    els.linesList.innerHTML = `<p class="hint" style="padding:20px;text-align:center">本图未识别出文本行，可点击右上角「＋ 添加一行」手工录入</p>`;
    return;
  }

  lines.forEach((line, idx) => {
    if (!linePassesFilter(line)) return;
    els.linesList.appendChild(lineRowEl(line, idx));
  });
}

function lineRowEl(line, idx) {
  const row = document.createElement("div");
  row.className = "line-row";
  row.dataset.line = line.id;
  if (line.status === "verified") row.classList.add("is-verified");
  else if (line.conf != null && line.conf < LOW_CONF) row.classList.add("is-low");

  const verified = line.status === "verified";
  row.innerHTML = `
    <div class="line-top">
      <span class="line-no">#${String(idx + 1).padStart(2, "0")}</span>
      ${confBadge(line)}
      ${line.edited ? '<span class="edited-flag">已修正</span>' : ""}
      ${verified ? '<span class="stamp">已核对</span>' : ""}
    </div>
    <div class="line-text ${verified ? "" : "editable"}">${esc(line.text) || '<span class="hint">（空行，点击编辑录入）</span>'}</div>
    <div class="line-ops">
      ${verified
        ? `<button class="op-btn del" data-op="revoke">撤销核对</button>`
        : `<button class="op-btn edit" data-op="edit">✎ 编辑修正</button>
           <button class="op-btn confirm" data-op="confirm">✓ 确认无误</button>`}
      <button class="op-btn del" data-op="del">删除</button>
    </div>`;

  row.addEventListener("click", (e) => {
    const op = e.target.closest(".op-btn")?.dataset.op;
    if (op === "edit") {
      startEdit(line.id, row);
    } else if (op === "confirm") {
      verifyLine(line.id);
    } else if (op === "revoke") {
      revokeLine(line.id);
    } else if (op === "del") {
      deleteLine(line.id);
    }
  });

  // 点击行文本（未核验态）也可进入编辑
  const textEl = row.querySelector(".line-text");
  textEl?.addEventListener("click", () => {
    if (line.status !== "verified") startEdit(line.id, row);
  });

  // 悬停/点击行 → 图上定位
  row.addEventListener("mouseenter", () => drawOverlay(line));
  row.addEventListener("click", () => {
    $$(".line-row").forEach((r) => r.classList.remove("is-active"));
    row.classList.add("is-active");
    drawOverlay(line);
  });

  return row;
}

function startEdit(lineId, row) {
  const img = getActiveImage();
  const line = img?.lines.find((l) => l.id === lineId);
  if (!line) return;

  const textEl = row.querySelector(".line-text");
  const input = document.createElement("textarea");
  input.className = "line-input";
  input.rows = Math.max(1, Math.ceil(line.text.length / 30));
  input.value = line.text;
  textEl.replaceWith(input);
  input.focus();
  input.setSelectionRange(input.value.length, input.value.length);

  const opsEl = row.querySelector(".line-ops");
  opsEl.innerHTML = `
    <button class="op-btn confirm" data-op="save">保存（Enter）</button>
    <button class="op-btn del" data-op="cancel">取消（Esc）</button>`;
  row.classList.add("is-error-edit");

  const save = () => {
    const v = input.value.replace(/\s+$/g, "");
    if (v !== line.text) {
      line.text = v;
      line.edited = true;
      // 编辑过 → 必须重新确认
      line.status = "unverified";
    }
    refreshReviewUI();
  };
  const cancel = () => refreshReviewUI();

  opsEl.onclick = (e) => {
    const op = e.target.closest(".op-btn")?.dataset.op;
    if (op === "save") save();
    else if (op === "cancel") cancel();
  };
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      save();
      // 快捷：保存后自动盖章并跳到下一个未核对行
      verifyLine(line.id, { silent: true });
      focusNextUnverified(line.id);
    } else if (e.key === "Escape") {
      e.preventDefault();
      cancel();
    }
  });
  input.addEventListener("blur", () => setTimeout(save, 80));
}

function verifyLine(lineId, { silent } = {}) {
  const img = getActiveImage();
  const line = img?.lines.find((l) => l.id === lineId);
  if (!line || !line.text.trim()) {
    if (!silent) toast("内容为空，请先编辑录入文字", "err");
    return;
  }
  line.status = "verified";
  refreshReviewUI();
  if (!silent && allVerified()) toast("全部行已核对完成，可进入导出", "ok");
}

function revokeLine(lineId) {
  const img = getActiveImage();
  const line = img?.lines.find((l) => l.id === lineId);
  if (!line) return;
  line.status = "unverified";
  refreshReviewUI();
}

function deleteLine(lineId) {
  const img = getActiveImage();
  if (!img) return;
  const idx = img.lines.findIndex((l) => l.id === lineId);
  if (idx < 0) return;
  if (!confirm("确定删除这一行吗？")) return;
  img.lines.splice(idx, 1);
  refreshReviewUI();
}

function focusNextUnverified(afterId) {
  const img = getActiveImage();
  if (!img) return;
  const startIdx = img.lines.findIndex((l) => l.id === afterId);
  const next = img.lines.slice(startIdx + 1).find((l) => l.status !== "verified");
  if (!next) return;
  const row = els.linesList.querySelector(`[data-line="${next.id}"]`);
  row?.scrollIntoView({ block: "center", behavior: "smooth" });
  row?.classList.add("is-active");
  drawOverlay(next);
}

function refreshReviewUI() {
  renderLines();
  renderImageStrip();
  updateReviewStats();
  updateExportEntry();
}

function totalStats() {
  let total = 0, verified = 0;
  state.images.forEach((i) => {
    if (i.status !== "done") return;
    i.lines.forEach((l) => {
      total++;
      if (l.status === "verified") verified++;
    });
  });
  return { total, verified };
}

function allVerified() {
  const { total, verified } = totalStats();
  return total > 0 && total === verified;
}

function updateReviewStats() {
  const { total, verified } = totalStats();
  const all = total > 0 && total === verified;
  els.reviewProgress.textContent = `已核对 ${verified} / ${total}`;
  els.reviewProgress.classList.toggle("all-done", all);
  els.btnToExport.disabled = !all;
}

function updateExportEntry() {
  updateReviewStats();
}

els.btnToExport.addEventListener("click", () => {
  if (!allVerified()) return;
  renderExport();
  goStep(4);
});

/* ============================================================
   步骤 4：导出
   ============================================================ */

els.btnBackReview.addEventListener("click", () => goStep(3));

function collectRows() {
  const rows = [["序号", "图片文件名", "行号", "文本内容", "识别置信度(%)", "核对状态", "人工修正"]];
  let no = 0;
  state.images.forEach((img) => {
    if (img.status !== "done") return;
    img.lines.forEach((line, idx) => {
      rows.push([
        ++no,
        img.name,
        idx + 1,
        line.text,
        line.manual || line.conf == null ? "人工录入" : line.conf,
        "已核对 ✓",
        line.edited ? "是" : "否",
      ]);
    });
  });
  return rows;
}

function renderExport() {
  const { total, verified } = totalStats();
  const imgCount = state.images.filter((i) => i.status === "done").length;
  const edited = [];
  state.images.forEach((i) => i.status === "done" && i.lines.forEach((l) => l.edited && edited.push(l)));

  els.exportSummary.innerHTML = `
    <div class="stat"><b>${imgCount}</b><span>图片张数</span></div>
    <div class="stat"><b>${total}</b><span>数据行数</span></div>
    <div class="stat ok"><b>${verified}</b><span>已人工核对</span></div>
    <div class="stat"><b>${edited.length}</b><span>人工修正行</span></div>`;

  const rows = collectRows();
  const shown = rows.slice(0, 101);
  els.previewTable.innerHTML = shown
    .map((r, i) =>
      i === 0
        ? `<tr>${r.map((c) => `<th>${esc(c)}</th>`).join("")}</tr>`
        : `<tr>
            <td class="mono">${r[0]}</td>
            <td>${esc(r[1])}</td>
            <td class="mono">${r[2]}</td>
            <td class="text-cell">${esc(r[3])}</td>
            <td class="mono">${r[4]}</td>
            <td class="v-ok">${r[5]}</td>
            <td class="mono">${r[6]}</td>
          </tr>`
    )
    .join("") + (rows.length > 101 ? `<tr><td colspan="7" class="hint" style="text-align:center;padding:10px">… 其余 ${rows.length - 101} 行将在导出的 Excel 中完整呈现</td></tr>` : "");
}

els.btnExport.addEventListener("click", () => {
  if (!allVerified()) return;
  if (typeof XLSX === "undefined") {
    toast("Excel 组件（SheetJS）未加载，请检查网络后刷新", "err");
    return;
  }
  const rows = collectRows();
  const ws = XLSX.utils.aoa_to_sheet(rows);
  ws["!cols"] = [
    { wch: 6 },
    { wch: 24 },
    { wch: 6 },
    { wch: 60 },
    { wch: 16 },
    { wch: 10 },
    { wch: 10 },
  ];
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "核对数据");
  const d = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  const name = `手写转Excel_${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}_${pad(d.getHours())}${pad(d.getMinutes())}.xlsx`;
  XLSX.writeFile(wb, name);
  toast("Excel 已导出（全部行均经人工核对）", "ok");
});

els.btnRestart.addEventListener("click", () => {
  if (!confirm("确定清空全部图片与核对结果吗？")) return;
  state.images.forEach((i) => URL.revokeObjectURL(i.url));
  state.images = [];
  state.activeImageId = null;
  state.filter = "all";
  renderThumbs();
  renderProgressList();
  goStep(1);
});

/* ---------- 离开提醒 ---------- */

window.addEventListener("beforeunload", (e) => {
  if (state.images.some((i) => i.lines.length > 0)) {
    e.preventDefault();
    e.returnValue = "";
  }
});

/* ---------- HTML 转义 ---------- */

function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/* ---------- 初始化 ---------- */

renderStepper();
renderThumbs();
