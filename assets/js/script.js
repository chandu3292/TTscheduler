document.addEventListener('DOMContentLoaded', function () {
  const genButton = document.getElementById('genButton');
  let genIntervalId = null;

  function startPolling() {
    if (genIntervalId !== null) return; // already running
    genIntervalId = setInterval(async function () {
      try {
        const resp = await fetch('/api/genNum/');
        if (!resp.ok) throw new Error('Network response was not ok');
        const data = await resp.json();
        // update all elements with class loaderClassValue
        document.querySelectorAll('.loaderClassValue').forEach(el => {
          el.textContent = data.genNum;
        });
      } catch (err) {
        // keep console logs for debugging
        console.error('Error fetching genNum:', err);
      }
    }, 1000);
  }

  if (genButton) {
    genButton.addEventListener('click', function (e) {
      // start polling and ensure we don't start multiple timers
      startPolling();
      // show loader if exists
      document.querySelectorAll('#loaderClass').forEach(el => el.style.display = 'inline-block');
    });
  }
});