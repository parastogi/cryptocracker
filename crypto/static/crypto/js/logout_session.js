var redirectTimeoutId = window.setTimeout(redirectToHomepage, 1800000)
function redirectToHomepage() {
  alert("No action for some time, loggin out");
  location.reload();
}
window.addEventListener('click keypress mousemove', function() {
  window.clearTimeout(redirectTimeoutId)
}, true)
