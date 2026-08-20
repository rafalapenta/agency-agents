async function renderScheduler() {
  const content = document.getElementById('pageContent');
  content.innerHTML = `
    <div class="page-header">
      <div class="page-header-left">
        <h1 class="page-title">Scheduler</h1>
        <p class="page-subtitle">Automated workflow scheduling</p>
      </div>
      <button class="btn btn-primary" onclick="showAddJob()">+ Add Job</button>
    </div>
    <div id="jobList"><div class="loading"><div class="loading-spinner"></div></div></div>
  `;

  try {
    const jobs = await api.getJobs();
    const container = document.getElementById('jobList');

    if (jobs.length === 0) {
      container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">⏱</div><div class="empty-state-title">No scheduled jobs</div><div class="empty-state-desc">Create your first scheduled job to automate workflows</div><button class="btn btn-primary mt-3" onclick="showAddJob()">+ Add Job</button></div>';
      return;
    }

    container.innerHTML = `
      <div class="table-wrapper">
        <table>
          <thead><tr><th>Name</th><th>Skill</th><th>Cron</th><th>Status</th><th>Last Run</th><th></th></tr></thead>
          <tbody>
            ${jobs.map(j => `
              <tr>
                <td><strong>${j.name}</strong></td>
                <td><span class="badge badge-accent">${j.skill}</span></td>
                <td><code>${j.cron}</code></td>
                <td><span class="badge ${j.enabled ? 'badge-success' : 'badge-warning'}">${j.enabled ? 'Active' : 'Paused'}</span></td>
                <td style="font-size:12px;color:var(--text-muted)">${j.last_run ? formatDate(j.last_run) : 'Never'}</td>
                <td><button class="btn btn-sm btn-danger" onclick="deleteJob('${j.id}')">Delete</button></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
      <div style="font-size:12px;color:var(--text-muted);text-align:right;margin-top:8px">${jobs.length} job${jobs.length !== 1 ? 's' : ''}</div>
    `;
  } catch (err) {
    document.getElementById('jobList').innerHTML = `<div class="empty-state"><div class="empty-state-icon">⚠</div><div class="empty-state-title">${escapeHtml(err.message)}</div></div>`;
  }
}

async function showAddJob() {
  let skills = [];
  try { const s = await api.getSkills(); skills = s; } catch {}

  showModal('Add Scheduled Job', `
    <div class="form-group">
      <label class="form-label">Job Name</label>
      <input id="jobName" class="form-input" placeholder="e.g., Nightly Backup">
    </div>
    <div class="form-group">
      <label class="form-label">Skill</label>
      <select id="jobSkill" class="form-select">
        <option value="">Select a skill...</option>
        ${skills.map(s => `<option value="${s.name}">${s.name.replace(/-/g, ' ')}</option>`).join('')}
      </select>
    </div>
    <div class="form-group">
      <label class="form-label">Cron Expression</label>
      <input id="jobCron" class="form-input" placeholder="e.g., 0 2 * * *" value="0 0 * * *">
      <div class="form-hint">Format: minute hour day month weekday</div>
    </div>
  `, `
    <button class="btn btn-ghost" onclick="closeModal()">Cancel</button>
    <button class="btn btn-primary" onclick="createJob()">Create Job</button>
  `);
}

async function createJob() {
  const name = document.getElementById('jobName').value.trim();
  const skill = document.getElementById('jobSkill').value;
  const cron = document.getElementById('jobCron').value.trim();
  if (!name || !skill || !cron) { showToast('All fields required', 'warning'); return; }
  try {
    await api.createJob({ name, skill, cron });
    closeModal();
    showToast('Job created', 'success');
    renderScheduler();
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  }
}

async function deleteJob(id) {
  if (!confirm('Delete this scheduled job?')) return;
  try {
    await api.deleteJob(id);
    showToast('Job deleted', 'success');
    renderScheduler();
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  }
}
