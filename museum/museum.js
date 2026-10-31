/* Museum of Petty Curses: curse of the day, curse-a-friend form, certificate page. */
(function () {
  "use strict";
  var curses = window.ROD_CURSES || [];
  if (!curses.length) return;

  var MONTHS = ["January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"];

  function ordinal(n) {
    var s = ["th", "st", "nd", "rd"], v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
  }

  function longDate(d) {
    return "the " + ordinal(d.getDate()) + " day of " + MONTHS[d.getMonth()] + ", " + d.getFullYear();
  }

  // Curse of the Day: same pick for every visitor on the same calendar day.
  var cotd = document.getElementById("cotd");
  if (cotd) {
    var now = new Date();
    var key = now.getFullYear() + "-" + (now.getMonth() + 1) + "-" + now.getDate();
    var idx = ROD.hash("curse-of-the-day|" + key) % curses.length;
    var c = curses[idx];
    document.getElementById("cotd-date").textContent = "Afflicting visitors on " + longDate(now) + " · Exhibit No. " + (idx + 1);
    var title = document.getElementById("cotd-title");
    var link = document.createElement("a");
    link.href = "#no-" + (idx + 1);
    link.textContent = c.title;
    title.appendChild(link);
    document.getElementById("cotd-note").textContent = c.note;
    cotd.hidden = false;
  }

  var randomBtn = document.getElementById("curse-random");
  if (randomBtn) {
    randomBtn.addEventListener("click", function () {
      document.getElementById("curse").value = String(1 + Math.floor(Math.random() * curses.length));
    });
  }

  // Certificate page
  var cert = document.getElementById("certificate");
  if (cert) {
    var p = ROD.params();
    var to = (p.get("to") || "").trim().slice(0, 40) || "Somebody Unnamed";
    var n = parseInt(p.get("curse"), 10);
    if (!(n >= 1 && n <= curses.length)) n = 1 + (ROD.hash(to) % curses.length);
    var curse = curses[n - 1];
    document.getElementById("cert-to").textContent = to;
    document.getElementById("cert-curse").textContent = "Exhibit No. " + n + ": " + curse.title;
    document.getElementById("cert-note").textContent = curse.note;
    document.getElementById("cert-date").textContent = "Issued on " + longDate(new Date()) + ".";
    document.title = to + " has been cursed · Museum of Petty Curses";
  }
})();
