# Multi-omics and (bio)Imaging Metadata Model Browser

Browse the consolidated **Multi-omics and (bio)Imaging Metadata (MIM)** LinkML model classes, attributes, inherited mixins, and profile extensions below.

<style>
.mim-browser-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  font-family: var(--md-text-font, system-ui, -apple-system, sans-serif);
}

.mim-controls {
  display: flex;
  gap: 12px;
  background: var(--md-code-bg-color, #f5f5f5);
  padding: 12px;
  border-radius: 6px;
  align-items: center;
}

.mim-input, .mim-select {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9em;
}

.mim-input { flex-grow: 1; }

.mim-layout {
  display: flex;
  gap: 20px;
  min-height: 550px;
}

.mim-tree-panel {
  width: 50%;
  max-height: 650px;
  overflow-y: auto;
  border: 1px solid var(--md-default-border-color, #e0e0e0);
  border-radius: 6px;
  padding: 12px;
}

.mim-details-panel {
  width: 50%;
  border: 1px solid var(--md-default-border-color, #e0e0e0);
  border-radius: 6px;
  padding: 16px;
  background: var(--md-code-bg-color, #fafafa);
  overflow-y: auto;
  max-height: 650px;
}

.mim-class-node {
  margin-bottom: 8px;
}

.mim-class-summary {
  cursor: pointer;
  font-weight: 600;
  padding: 4px 6px;
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.03);
}

.mim-class-summary:hover {
  background: rgba(0, 0, 0, 0.07);
}

.mim-attr-list {
  list-style: none;
  padding-left: 18px;
  margin: 6px 0;
}

.mim-attr-item {
  cursor: pointer;
  padding: 3px 6px;
  border-radius: 3px;
  font-size: 0.88em;
  display: flex;
  align-items: center;
  gap: 6px;
}

.mim-attr-item:hover {
  background: rgba(25, 118, 210, 0.1);
}

.badge {
  font-size: 0.72em;
  padding: 1px 5px;
  border-radius: 3px;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-req { background: #ffebee; color: #c62828; }
.badge-opt { background: #e8f5e9; color: #2e7d32; }
.badge-multi { background: #e3f2fd; color: #1565c0; }
.badge-abstract { background: #fff3e0; color: #ef6c00; }
.badge-range { background: #f3e5f5; color: #6a1b9a; }
</style>

<div class="mim-browser-container">
  <div class="mim-controls">
    <input type="text" id="mim-search" class="mim-input" placeholder="Search paths, fields, or descriptions (e.g. MIMAgent, email)...">
    <select id="mim-profile-filter" class="mim-select">
      <option value="all">All Profiles</option>
      <option value="foundation">Foundation</option>
      <option value="bioimaging">Bioimaging</option>
      <option value="genomics">Genomics</option>
    </select>
    <label style="font-size: 0.85em; cursor: pointer;">
      <input type="checkbox" id="mim-show-abstract"> Include Abstract Classes
    </label>
  </div>

  <div class="mim-layout">
    <!-- Left Tree View -->
    <div id="mim-tree" class="mim-tree-panel">
      <em>Loading metadata model...</em>
    </div>

    <!-- Right Inspector Panel -->
    <div id="mim-details" class="mim-details-panel">
      <h3 style="margin-top:0;">Attribute Inspector</h3>
      <p style="color: #666;">Click any attribute path on the left tree to inspect its URI, constraints, description, and enum ranges.</p>
    </div>
  </div>
</div>

<script>
let modelData = [];
let detailsData = {};

async function loadModel() {
  try {
    const [modelRes, detailsRes] = await Promise.all([
      fetch('../data/model.json'),
      fetch('../data/details.json')
    ]);
    const modelJson = await modelRes.json();
    modelData = modelJson.classes;
    detailsData = await detailsRes.json();
    renderTree();
  } catch (err) {
    document.getElementById('mim-tree').innerHTML = '<span style="color:red;">Error loading schema JSON files. Ensure scripts/build_docs_data.py has run.</span>';
  }
}

function renderTree() {
  const filterText = document.getElementById('mim-search').value.toLowerCase();
  const selectedProfile = document.getElementById('mim-profile-filter').value;
  const showAbstract = document.getElementById('mim-show-abstract').checked;
  const treeContainer = document.getElementById('mim-tree');

  treeContainer.innerHTML = '';

  modelData.forEach(cls => {
    if (!showAbstract && cls.abstract) return;
    if (selectedProfile !== 'all' && cls.profile !== selectedProfile) return;

    const classMatches = cls.class.toLowerCase().includes(filterText) || 
                         (cls.description && cls.description.toLowerCase().includes(filterText));

    const matchingFields = cls.fields.filter(f => 
      f.path.toLowerCase().includes(filterText) || 
      f.name.toLowerCase().includes(filterText) ||
      classMatches
    );

    if (filterText && !classMatches && matchingFields.length === 0) return;

    const detailsNode = document.createElement('details');
    detailsNode.className = 'mim-class-node';
    if (filterText) detailsNode.open = true;

    const summary = document.createElement('summary');
    summary.className = 'mim-class-summary';
    
    let abstractBadge = cls.abstract ? ' <span class="badge badge-abstract">abstract</span>' : '';
    summary.innerHTML = `<strong>${cls.class}</strong> <small style="color:#666;">(${cls.module})</small>${abstractBadge}`;
    detailsNode.appendChild(summary);

    const ul = document.createElement('ul');
    ul.className = 'mim-attr-list';

    matchingFields.forEach(field => {
      const li = document.createElement('li');
      li.className = 'mim-attr-item';

      let reqBadge = field.required 
        ? '<span class="badge badge-req">required</span>' 
        : '<span class="badge badge-opt">optional</span>';
      
      let multiBadge = field.multivalued ? '<span class="badge badge-multi">list</span>' : '';
      let rangeBadge = `<span class="badge badge-range">${field.range}</span>`;

      li.innerHTML = `<code>${field.name}</code> ${rangeBadge} ${reqBadge} ${multiBadge}`;
      li.onclick = (e) => {
        e.stopPropagation();
        showInspector(field.path);
      };
      ul.appendChild(li);
    });

    detailsNode.appendChild(ul);
    treeContainer.appendChild(detailsNode);
  });
}

function showInspector(path) {
  const item = detailsData[path];
  const container = document.getElementById('mim-details');

  if (!item) {
    container.innerHTML = `<p>No details found for <code>${path}</code></p>`;
    return;
  }

  let enumHtml = '';
  if (item.is_enum && item.enum_values && item.enum_values.length > 0) {
    enumHtml = `
      <div style="margin-top:10px;">
        <strong>Permissible Values (${item.enum_values.length}):</strong>
        <div style="max-height:150px; overflow-y:auto; background:#fff; border:1px solid #ddd; padding:6px; margin-top:4px; font-size:0.85em;">
          <code>${item.enum_values.join('</code>, <code>')}</code>
        </div>
      </div>
    `;
  }

  container.innerHTML = `
    <h3 style="margin-top:0; color:#1976d2;"><code>${path}</code></h3>
    <p><strong>Description:</strong> ${item.description || '<em>No description provided.</em>'}</p>
    <hr style="border:0; border-top:1px solid #ddd; margin: 12px 0;">
    <table style="width:100%; font-size:0.88em; border-collapse:collapse;">
      <tr><td><strong>Declared In Class:</strong></td><td><code>${item.declared_in}</code></td></tr>
      <tr><td><strong>Range:</strong></td><td><code>${item.range}</code></td></tr>
      <tr><td><strong>Required:</strong></td><td>${item.required ? 'Yes' : 'No'}</td></tr>
      <tr><td><strong>Multivalued:</strong></td><td>${item.multivalued ? 'Yes' : 'No'}</td></tr>
      ${item.pattern ? `<tr><td><strong>Pattern:</strong></td><td><code>${item.pattern}</code></td></tr>` : ''}
      ${item.slot_uri ? `<tr><td><strong>Slot URI:</strong></td><td><code>${item.slot_uri}</code></td></tr>` : ''}
    </table>
    ${enumHtml}
  `;
}

document.getElementById('mim-search').addEventListener('input', renderTree);
document.getElementById('mim-profile-filter').addEventListener('change', renderTree);
document.getElementById('mim-show-abstract').addEventListener('change', renderTree);

loadModel();
</script>