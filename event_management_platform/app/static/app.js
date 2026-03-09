const toast = document.getElementById('toast');

function showToast(message, isError = false) {
  if (!toast) return;
  toast.textContent = message;
  toast.style.display = 'block';
  toast.style.borderLeftColor = isError ? 'var(--danger)' : 'var(--success)';
  setTimeout(() => toast.style.display = 'none', 2400);
}

async function api(url, options = {}) {
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  const contentType = response.headers.get('content-type') || '';
  const data = contentType.includes('application/json') ? await response.json() : {};
  if (!response.ok) throw new Error(data.detail || 'Request failed');
  return data;
}

function formDataToJson(form) {
  const data = Object.fromEntries(new FormData(form).entries());
  Object.keys(data).forEach((key) => {
    if (data[key] === '') data[key] = null;
  });
  ['id', 'capacity', 'trainer_id', 'participant_id', 'event_id'].forEach((key) => {
    if (data[key] !== undefined && data[key] !== null) data[key] = Number(data[key]);
  });
  return data;
}

function cleanEmptyFields(data) {
  const cleaned = {};
  Object.entries(data).forEach(([key, value]) => {
    if (value !== null && value !== '' && !(typeof value === 'number' && Number.isNaN(value))) cleaned[key] = value;
  });
  return cleaned;
}

async function loadDashboardSummary() {
  const data = await api('/api/dashboard-summary');
  const mapping = {
    participantsCount: data.participants,
    trainersCount: data.trainers,
    eventsCount: data.events,
    registrationsCount: data.registrations,
  };
  Object.entries(mapping).forEach(([id, value]) => {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
  });
}

async function loadParticipants() {
  const rows = await api('/api/participants');
  const target = document.getElementById('participantsTable');
  if (!target) return;
  target.innerHTML = rows.map(item => `
    <tr><td>${item.id}</td><td>${item.name}</td><td>${item.email}</td><td>${item.phone || '-'}</td><td>${item.company || '-'}</td></tr>`).join('');
}

async function loadTrainers() {
  const rows = await api('/api/trainers');
  const target = document.getElementById('trainersTable');
  if (!target) return;
  target.innerHTML = rows.map(item => `
    <tr><td>${item.id}</td><td>${item.name}</td><td>${item.email}</td><td>${item.expertise}</td><td>${item.bio || '-'}</td></tr>`).join('');
}

async function loadEvents() {
  const rows = await api('/api/events');
  const target = document.getElementById('eventsTable');
  if (!target) return;
  target.innerHTML = rows.map(item => `
    <tr><td>${item.id}</td><td>${item.title}</td><td>${item.description || '-'}</td><td>${item.date}</td><td>${item.location}</td><td>${item.capacity}</td><td>${item.trainer_id || '-'}</td></tr>`).join('');
}
