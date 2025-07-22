// content.js
(function() {
  // Try JSON-LD first
  const scripts = document.querySelectorAll('script[type="application/ld+json"]');
  let jobData = null;

  scripts.forEach(script => {
    try {
      const data = JSON.parse(script.textContent);
      if (data["@type"] === "JobPosting") {
        jobData = data;
      }
    } catch (e) {}
  });

  // Fallback: Jora DOM extraction
  if (!jobData) {
    const jobPage = document.querySelector('.job-details-page');
    if (jobPage) {
      // Example selectors - adjust as needed based on Jora's HTML
      const url = window.location.href;
      const title = jobPage.querySelector('.job-title')?.innerText || '';
      const company = jobPage.querySelector('.company')?.innerText || '';
      const location = jobPage.querySelector('.location')?.innerText || '';
      const description = jobPage.querySelector('#job-description-container')?.innerText || '';
      const posted_date = jobPage.querySelector('.listed-date')?.innerText || '';

      jobData = {
        source: "jora",
        url, 
        title,
        company,
        location,
        description,
        posted_date
      };
    }
  }

  if (jobData) {
    chrome.runtime.sendMessage({ type: "JOB_DATA", data: jobData });
  }
})(); 