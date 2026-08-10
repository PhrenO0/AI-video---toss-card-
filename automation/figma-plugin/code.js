/**
 * TOSS 카드뉴스 생성기 — Figma 플러그인 메인 스레드.
 *
 * `toss-content cardnews` 가 만든 spec(JSON)을 받아 카드 프레임을 실제로 찍어낸다.
 * REST API로는 노드를 만들 수 없어서 이 부분만 플러그인으로 분리돼 있다.
 *
 * 동작 방식은 두 가지.
 *  1) 템플릿 모드 — 파일 안에 `template/cover`, `template/body`, `template/outro`
 *     라는 이름의 프레임(또는 컴포넌트)이 있으면 그것을 복제해서 텍스트만 갈아끼운다.
 *     디자이너가 만든 스타일이 그대로 유지되므로 이쪽을 권장한다.
 *  2) 기본 모드 — 템플릿이 없으면 코드가 최소한의 레이아웃으로 프레임을 만든다.
 *
 * 템플릿 안의 텍스트 레이어는 `#title`, `#body`, `#badge` 로 이름 짓고,
 * 이미지 자리는 `#image` 로 이름 지은 도형을 두면 자동으로 채워진다.
 */

const CANVAS = { width: 1080, height: 1350 };
const GAP = 120;

const SLOT_TITLE = "#title";
const SLOT_BODY = "#body";
const SLOT_BADGE = "#badge";
const SLOT_IMAGE = "#image";

const PALETTE = {
  cover: { bg: { r: 0, g: 0.39, b: 1 }, fg: { r: 1, g: 1, b: 1 }, sub: { r: 0.84, g: 0.91, b: 1 } },
  body: { bg: { r: 1, g: 1, b: 1 }, fg: { r: 0.09, g: 0.11, b: 0.14 }, sub: { r: 0.37, g: 0.41, b: 0.47 } },
  outro: { bg: { r: 0.09, g: 0.11, b: 0.14 }, fg: { r: 1, g: 1, b: 1 }, sub: { r: 0.59, g: 0.75, b: 1 } },
};

figma.showUI(__html__, { width: 460, height: 620 });

figma.ui.onmessage = async (msg) => {
  try {
    if (msg.type === "generate") {
      const spec = typeof msg.spec === "string" ? JSON.parse(msg.spec) : msg.spec;
      const result = await generate(spec);
      figma.ui.postMessage({ type: "done", result });
      figma.notify(`카드 ${result.nodeIds.length}장을 만들었어요.`);
    } else if (msg.type === "inspect") {
      figma.ui.postMessage({ type: "inspect-result", templates: await findTemplateNames() });
    } else if (msg.type === "close") {
      figma.closePlugin();
    }
  } catch (error) {
    figma.ui.postMessage({ type: "error", message: String(error && error.message ? error.message : error) });
    figma.notify(`실패: ${error}`, { error: true });
  }
};

/** spec 한 건을 받아 카드 프레임들을 생성한다. */
async function generate(spec) {
  if (!spec || !Array.isArray(spec.cards) || spec.cards.length === 0) {
    throw new Error("spec.cards 가 비어 있습니다.");
  }

  const page = await ensurePage(spec.pageName || "카드뉴스 자동생성");
  figma.currentPage = page;

  const templates = await loadTemplates();
  await loadFontsFor(templates);

  const container = figma.createFrame();
  container.name = `${spec.slug || "cardnews"} · ${spec.topic || ""}`.trim();
  container.layoutMode = "HORIZONTAL";
  container.itemSpacing = GAP;
  container.paddingTop = GAP;
  container.paddingBottom = GAP;
  container.paddingLeft = GAP;
  container.paddingRight = GAP;
  container.primaryAxisSizingMode = "AUTO";
  container.counterAxisSizingMode = "AUTO";
  container.fills = [{ type: "SOLID", color: { r: 0.96, g: 0.96, b: 0.97 } }];
  page.appendChild(container);

  const nodeIds = [];
  for (const card of spec.cards) {
    const frame = await buildCard(card, templates);
    container.appendChild(frame);
    nodeIds.push(frame.id);
  }

  // 새로 만든 세트를 기존 작업물 옆으로 밀어 겹치지 않게 한다.
  container.x = nextFreeX(page, container);
  container.y = 0;

  figma.currentPage.selection = [container];
  figma.viewport.scrollAndZoomIntoView([container]);

  return { containerId: container.id, nodeIds, pageName: page.name };
}

/** 카드 1장 — 템플릿이 있으면 복제, 없으면 직접 조립. */
async function buildCard(card, templates) {
  const template = templates[card.kind] || templates.body;
  const frame = template ? cloneTemplate(template) : createDefaultFrame(card);
  frame.name = `${String(card.index).padStart(2, "0")}-${card.kind}`;

  await fillSlot(frame, SLOT_TITLE, card.title);
  await fillSlot(frame, SLOT_BODY, card.body);
  await fillSlot(frame, SLOT_BADGE, card.badge);

  if (card.imageUrl || card.image_url) {
    await fillImageSlot(frame, card.imageUrl || card.image_url);
  }
  return frame;
}

function cloneTemplate(template) {
  const clone = template.type === "COMPONENT" ? template.createInstance() : template.clone();
  // 인스턴스는 텍스트 오버라이드가 막힐 수 있어 분리한다.
  return clone.type === "INSTANCE" ? clone.detachInstance() : clone;
}

function createDefaultFrame(card) {
  const colors = PALETTE[card.kind] || PALETTE.body;
  const frame = figma.createFrame();
  frame.resize(CANVAS.width, CANVAS.height);
  frame.fills = [{ type: "SOLID", color: colors.bg }];
  frame.layoutMode = "VERTICAL";
  frame.paddingTop = 90;
  frame.paddingBottom = 90;
  frame.paddingLeft = 90;
  frame.paddingRight = 90;
  frame.itemSpacing = 28;
  frame.primaryAxisSizingMode = "FIXED";
  frame.counterAxisSizingMode = "FIXED";

  frame.appendChild(makeText(SLOT_BADGE, 28, colors.sub));
  frame.appendChild(makeText(SLOT_TITLE, card.kind === "cover" ? 84 : 64, colors.fg));
  frame.appendChild(makeText(SLOT_BODY, 40, colors.sub));
  return frame;
}

function makeText(name, size, color) {
  const node = figma.createText();
  node.name = name;
  node.fontName = { family: "Inter", style: "Bold" };
  node.fontSize = size;
  node.fills = [{ type: "SOLID", color }];
  node.layoutSizingHorizontal = "FILL";
  node.textAutoResize = "HEIGHT";
  return node;
}

/** 이름이 일치하는 텍스트 레이어를 찾아 내용을 채운다. 없으면 조용히 넘어간다. */
async function fillSlot(frame, slotName, value) {
  const nodes = frame.findAll((n) => n.type === "TEXT" && n.name === slotName);
  for (const node of nodes) {
    if (!value) {
      node.visible = false;
      continue;
    }
    await figma.loadFontAsync(node.fontName === figma.mixed ? { family: "Inter", style: "Regular" } : node.fontName);
    node.characters = value;
    node.visible = true;
  }
}

/** `#image` 도형에 원격 이미지를 채운다. 실패해도 카드 생성은 계속된다. */
async function fillImageSlot(frame, url) {
  const targets = frame.findAll((n) => n.name === SLOT_IMAGE && "fills" in n);
  if (targets.length === 0) return;
  try {
    const response = await fetch(url);
    const bytes = new Uint8Array(await response.arrayBuffer());
    const image = figma.createImage(bytes);
    for (const node of targets) {
      node.fills = [{ type: "IMAGE", scaleMode: "FILL", imageHash: image.hash }];
    }
  } catch (error) {
    console.warn("이미지 삽입 실패:", url, error);
  }
}

/** 파일 안의 `template/*` 프레임을 수집. */
async function loadTemplates() {
  const templates = {};
  for (const page of figma.root.children) {
    await page.loadAsync();
    for (const node of page.children) {
      if (node.type !== "FRAME" && node.type !== "COMPONENT") continue;
      const match = /^template\/(cover|body|outro)$/i.exec(node.name.trim());
      if (match) templates[match[1].toLowerCase()] = node;
    }
  }
  return templates;
}

async function findTemplateNames() {
  const templates = await loadTemplates();
  return Object.keys(templates);
}

/** 템플릿에 쓰인 폰트를 미리 로드 (안 하면 텍스트 수정이 실패한다). */
async function loadFontsFor(templates) {
  const fonts = new Map();
  for (const key of Object.keys(templates)) {
    for (const node of templates[key].findAll((n) => n.type === "TEXT")) {
      if (node.fontName === figma.mixed) continue;
      fonts.set(`${node.fontName.family}::${node.fontName.style}`, node.fontName);
    }
  }
  // 기본 모드에서 쓰는 폰트도 확보해 둔다.
  fonts.set("Inter::Bold", { family: "Inter", style: "Bold" });
  fonts.set("Inter::Regular", { family: "Inter", style: "Regular" });

  for (const font of fonts.values()) {
    try {
      await figma.loadFontAsync(font);
    } catch (error) {
      console.warn("폰트 로드 실패:", font, error);
    }
  }
}

async function ensurePage(name) {
  for (const page of figma.root.children) {
    if (page.name === name) {
      await page.loadAsync();
      return page;
    }
  }
  const page = figma.createPage();
  page.name = name;
  return page;
}

/** 페이지에 이미 있는 노드들 오른쪽 빈 자리를 찾는다. */
function nextFreeX(page, exclude) {
  let maxX = 0;
  for (const node of page.children) {
    if (node.id === exclude.id) continue;
    maxX = Math.max(maxX, node.x + node.width);
  }
  return maxX === 0 ? 0 : maxX + GAP * 2;
}
