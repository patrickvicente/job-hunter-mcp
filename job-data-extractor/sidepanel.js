
let excitement = 0;

function renderStars() {
  const stars = document.getElementById('stars');
  if (!stars) return;
  stars.innerHTML = '';
  for (let i = 1; i <= 5; i++) {
    const star = document.createElement('span');
    star.textContent = '\u2605';
    star.className = 'star' + (i <= excitement ? ' selected' : '');
    star.onclick = () => { excitement = i; renderStars(); };
    stars.appendChild(star);
  }
}
renderStars();

chrome.runtime.sendMessage({ type: "GET_JOB_DATA" }, (response) => {
  if (response && response.data) {
    const data = response.data;
    document.getElementById('jobUrl').value = data.url || '';
    document.getElementById('jobTitle').value = data.title || '';
    document.getElementById('jobDescription').value = data.description || '';
    document.getElementById('jobCompany').value = data.company || '';
    document.getElementById('jobLocation').value = data.location || '';
    document.getElementById('jobWorkMode').value = data.work_mode || 'onsite';
    document.getElementById('jobType').value = data.job_type || 'full-time';
    document.getElementById('jobExperienceLevel').value = data.experience_level || 'entry';
    document.getElementById('jobCategory').value = data.job_category || '';
    document.getElementById('jobSalaryMin').value = data.salary_min || '';
    document.getElementById('jobSalaryMax').value = data.salary_max || '';
    document.getElementById('jobCurrency').value = data.currency || 'AUD';
    document.getElementById('jobVisaSponsorship').checked = !!data.visa_sponsorship;
    document.getElementById('jobSource').value = data.source || 'other';
    document.getElementById('jobTechStack').value = Array.isArray(data.tech_stack) ? data.tech_stack.join(', ') : (data.tech_stack || '');
    // Application fields (if present)
    document.getElementById('applicationStatus').value = data.status || 'pending';
    document.getElementById('applicationNotes').value = data.notes || '';
  }
});

document.getElementById('jobForm').onsubmit = async (e) => {
  e.preventDefault();
  const job = {
    url: document.getElementById('jobUrl').value,
    title: document.getElementById('jobTitle').value,
    description: document.getElementById('jobDescription').value,
    company: document.getElementById('jobCompany').value,
    location: document.getElementById('jobLocation').value,
    work_mode: document.getElementById('jobWorkMode').value,
    job_type: document.getElementById('jobType').value,
    experience_level: document.getElementById('jobExperienceLevel').value,
    job_category: document.getElementById('jobCategory').value,
    salary_min: document.getElementById('jobSalaryMin').value ? parseInt(document.getElementById('jobSalaryMin').value) : null,
    salary_max: document.getElementById('jobSalaryMax').value ? parseInt(document.getElementById('jobSalaryMax').value) : null,
    currency: document.getElementById('jobCurrency').value,
    visa_sponsorship: document.getElementById('jobVisaSponsorship').checked,
    source: document.getElementById('jobSource').value,
    tech_stack: document.getElementById('jobTechStack').value.split(',').map(s => s.trim()).filter(Boolean),
  };
  const application = {
    status: document.getElementById('applicationStatus').value,
    notes: document.getElementById('applicationNotes').value
  };
  // Send to backend (adjust endpoint and payload as needed)
  const res = await fetch('https://your-backend.com/api/jobs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...job, ...application })
  });
  document.getElementById('status').textContent = res.ok ? 'Saved!' : 'Error saving job';
}; 