async function renderMemory() {
  const content = document.getElementById('pageContent');
  content.innerHTML = `
    <div class="page-header">
      <div class="page-header-left">
        <h1 class="page-title">Memory</h1>
        <p class="page-subtitle">Shared brain context across all agents</p>
      </div>
    </div>
    <div class="tabs" id="memoryTabs">
      <button class="tab active" data-view="files" onclick="switchMemoryView('files')">📄 Files</button>
      <button class="tab" data-view="graph" onclick="switchMemoryView('graph')">🕸 Knowledge Graph</button>
    </div>
    <div id="memoryList"><div class="loading"><div class="loading-spinner"></div></div></div>
  `;

  window._memoryView = 'files';
  await loadMemoryFiles();
}

function switchMemoryView(view) {
  window._memoryView = view;
  document.querySelectorAll('#memoryTabs .tab').forEach(t => t.classList.toggle('active', t.dataset.view === view));
  if (view === 'graph') loadMemoryGraph();
  else loadMemoryFiles();
}

async function loadMemoryFiles() {
  const container = document.getElementById('memoryList');
  if (!container) return;

  try {
    const brain = await api.getBrain();
    const files = Object.entries(brain);

    if (files.length === 0) {
      container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">🧠</div><div class="empty-state-title">No memory files</div></div>';
      return;
    }

    container.innerHTML = `<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,420px),1fr));gap:12px;min-width:0">${files.map(([name, content]) => {
      const preview = content ? content.slice(0, 200) : '';
      const safeName = escapeHtml(name.replace('.md', '').replace(/-/g, ' '));
      return `<div class="card" style="cursor:pointer;min-width:0" onclick="editMemory('${encodeURIComponent(name)}')">
        <div class="flex items-center justify-between mb-2">
          <div><span class="card-title">${safeName}</span></div>
          <span class="badge badge-info">${content ? content.split('\n').length : 0} lines</span>
        </div>
        <pre style="max-height:80px;overflow:hidden;font-size:11px;color:var(--text-muted);white-space:pre-wrap;word-break:break-word">${escapeHtml(preview)}${preview.length >= 200 ? '...' : ''}</pre>
      </div>`;
    }).join('')}</div>`;
  } catch (err) {
    container.innerHTML = `<div class="empty-state"><div class="empty-state-icon">⚠</div><div class="empty-state-title">${escapeHtml(err.message)}</div></div>`;
  }
}

async function loadMemoryGraph() {
  const container = document.getElementById('memoryList');
  if (!container) return;
  container.innerHTML = `<div class="loading"><div class="loading-spinner"></div><span>Building graph...</span></div>`;

  try {
    const graph = await api.getMemoryGraph();
    const nodes = graph.nodes || [];
    const edges = graph.edges || [];

    if (nodes.length === 0) {
      container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">🕸</div><div class="empty-state-title">No graph data</div><div class="empty-state-desc">Run a memory reindex or chat with agents to build connections.</div></div>';
      return;
    }

    const stats = graph.stats || {};
    container.innerHTML = `
      <div class="card" style="margin-bottom:16px">
        <div style="display:flex;gap:16px;flex-wrap:wrap">
          <span class="badge badge-info">📄 ${stats.nodes || 0} nodes</span>
          <span class="badge badge-accent">🔗 ${stats.edges || 0} edges</span>
          <span class="badge badge-success">${nodes.filter(n => (n.type || '').startsWith('entity')).length} entities</span>
        </div>
      </div>
      <div class="card">
        <canvas id="memoryGraphCanvas" style="width:100%;height:480px"></canvas>
      </div>
      <div style="margin-top:12px;font-size:12px;color:var(--text-muted)">Click a node to open the associated file. Drag to pan, scroll to zoom.</div>
    `;
    drawMemoryGraph(graph);
  } catch (err) {
    container.innerHTML = `<div class="empty-state"><div class="empty-state-icon">⚠</div><div class="empty-state-title">${escapeHtml(err.message)}</div></div>`;
  }
}

function drawMemoryGraph(graph) {
  const canvas = document.getElementById('memoryGraphCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const width = canvas.clientWidth || 800;
  const height = canvas.clientHeight || 480;
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  ctx.scale(dpr, dpr);

  const nodes = graph.nodes || [];
  const edges = graph.edges || [];
  const typeColors = {
    brain: '#6c5ce7', skill: '#00b894', journal: '#fdcb6e', general: '#74b9ff',
  };
  const colorFor = (t) => {
    if (t.startsWith('entity:')) return '#fd79a8';
    return typeColors[t] || '#74b9ff';
  };

  // Simple layout: entities on left, docs spread on right (force-ish radial fallback)
  const entityNodes = nodes.filter(n => (n.type || '').startsWith('entity:'));
  const docNodes = nodes.filter(n => !(n.type || '').startsWith('entity:'));
  const positions = {};
  const cx = width / 2, cy = height / 2;
  docNodes.forEach((n, i) => {
    const angle = (i / Math.max(docNodes.length, 1)) * Math.PI * 2 - Math.PI / 2;
    positions[n.id] = { x: cx + Math.cos(angle) * Math.min(width * 0.3, 200), y: cy + Math.sin(angle) * Math.min(height * 0.35, 180) };
  });
  entityNodes.forEach((n, i) => {
    const angle = (i / Math.max(entityNodes.length, 1)) * Math.PI * 2 - Math.PI / 2;
    positions[n.id] = { x: cx + Math.cos(angle) * Math.min(width * 0.38, 260), y: cy + Math.sin(angle) * Math.min(height * 0.42, 220) };
  });

  ctx.clearRect(0, 0, width, height);
  ctx.lineWidth = 1;
  ctx.strokeStyle = 'rgba(148,163,184,0.4)';
  edges.forEach(e => {
    const a = positions[e.source], b = positions[e.target];
    if (!a || !b) return;
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.stroke();
  });

  nodes.forEach(n => {
    const p = positions[n.id];
    if (!p) return;
    const color = colorFor(n.type);
    const isEntity = (n.type || '').startsWith('entity:');
    const radius = isEntity ? 6 : 10;
    ctx.beginPath();
    ctx.arc(p.x, p.y, radius, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 1.5;
    ctx.stroke();
    const label = (n.label || '').slice(0, 18);
    ctx.fillStyle = 'var(--text-secondary, #cbd5e1)';
    ctx.font = '10px Inter, sans-serif';
    ctx.fillText(label, p.x + radius + 4, p.y + 4);
  });

  // Click-to-open: store layout for hit testing
  window._graphLayout = { positions, nodes, docById: {} };
  nodes.forEach(n => { window._graphLayout.docById[n.id] = n; });
  canvas.onclick = (ev) => {
    const rect = canvas.getBoundingClientRect();
    const mx = ev.clientX - rect.left, my = ev.clientY - rect.top;
    for (const [id, p] of Object.entries(positions)) {
      if (Math.hypot(mx - p.x, my - p.y) < 14) {
        const n = window._graphLayout.docById[id];
        if (n && n.path && n.path.endsWith('.md') && !(n.type || '').startsWith('entity:')) {
          editMemory(encodeURIComponent(n.path.split('/').pop()));
        }
        return;
      }
    }
  };
}

async function editMemory(encodedName) {
  const name = decodeURIComponent(encodedName);
  const display = escapeHtml(name.replace('.md', '').replace(/-/g, ' '));
  let content = '';
  try {
    const r = await api.getBrainFile(name);
    content = r.content || '';
  } catch {}

  showModal(`Edit: ${display}`, `
    <div class="form-group">
      <label class="form-label">Content</label>
      <textarea id="memContent" class="form-textarea" style="min-height:300px;font-size:12px">${escapeHtml(content)}</textarea>
    </div>
  `, `
    <button class="btn btn-ghost" onclick="closeModal()">Cancel</button>
    <button class="btn btn-primary" onclick="saveMemory('${encodeURIComponent(name)}')">💾 Save</button>
  `);
}

async function saveMemory(encodedName) {
  const name = decodeURIComponent(encodedName);
  const content = document.getElementById('memContent').value;
  try {
    await api.updateBrainFile(name, content);
    closeModal();
    showToast('Memory updated', 'success');
    renderMemory();
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  }
}
