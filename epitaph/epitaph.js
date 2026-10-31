/* The Epitaph Generator. Same name + weaknesses + reroll = same stone, so links are shareable. */
(function () {
  "use strict";
  var SVGNS = "http://www.w3.org/2000/svg";

  var GENERAL = [
    "{n} said “it's probably fine.” It wasn't.",
    "Finally got some rest.",
    "Read the terms and conditions. All of them.",
    "I told you I was ill.",
    "Gone to find the other sock.",
    "Didn't read the instructions. Still won't.",
    "Back in five minutes.",
    "Always wanted a little place in the country. Here it is.",
    "Out of office. Permanently.",
    "Was going to start on Monday.",
    "Finally found a quiet place to read.",
    "Do not disturb. Seriously.",
    "{n} has left the chat.",
    "Picked the mushrooms personally. Was not a mushroom expert.",
    "Agreed to “just one more.”",
    "Loved by many. Tolerated by most.",
    "Said the vampire's name three times. At midnight. For a laugh.",
    "Pressed the big red button. Just to see.",
    "Never once replied on time. Isn't starting now.",
    "Petted the wrong dog.",
    "Went to check on the noise in the basement.",
    "Thought the ice was thick enough.",
    "Ordered the “extra spicy.”",
    "Dearly departed. Mildly missed.",
    "Couldn't stay. Had a thing.",
    "Gone, but still owes us twenty euros.",
    "Here rests {n}. Please don't make it weird.",
    "Taller in spirit.",
    "Asked to speak to the manager. Was sent upstairs.",
    "Wanted to be cremated. Lost the argument.",
    "Assembled the furniture without the leftover screws.",
    "Said “what's the worst that could happen?”"
  ];

  var TAGGED = {
    coffee: ["Ran out of coffee. Then out of everything.", "Last words: “One more espresso can't hurt.”"],
    cats: ["Knocked off the shelf by the cat, like everything else.", "Survived by four cats, who have not yet noticed."],
    beer: ["Last words: “Hold my beer.”", "Someone held the beer. Nobody held {n}."],
    gym: ["Skipped leg day. The legs took revenge.", "Never missed a workout. Should have missed that one."],
    plants: ["Finally joined the houseplants.", "Overwatered, like everything else they loved."],
    tv: ["Are you still watching? No.", "“Just one more episode.” It was the finale."],
    work: ["Per my last email: I'm dead.", "Circled back. Never returned."],
    phone: ["Died at 1%, just like the phone.", "Looked up from the phone once. Didn't like what it saw."]
  };

  var DATES = [
    "BORN: YES · DIED: EVENTUALLY",
    "ARRIVED LATE · LEFT EARLY",
    "BORN: A MONDAY · DIED: ALSO A MONDAY",
    "CAME · SAW · LEFT",
    "STARTED STRONG · ENDED ABRUPTLY",
    "BORN: ONCE · DIED: ALSO ONCE"
  ];

  var form = document.getElementById("epitaph-form");
  var svg = document.getElementById("stone-svg");
  var nameInput = document.getElementById("name");
  var rerollBtn = document.getElementById("reroll");
  var downloadBtn = document.getElementById("download");
  var shareBtn = document.getElementById("share");
  var shareOut = document.getElementById("share-out");
  var state = null; // { name, tags, r }

  function selectedTags() {
    return Array.prototype.filter.call(form.querySelectorAll("input[name=tags]"), function (c) { return c.checked; })
      .map(function (c) { return c.value; });
  }

  function compose(s) {
    var rand = ROD.rng(ROD.hash(s.name.toLowerCase() + "|" + s.tags.join(",")) + s.r * 7919);
    var tagged = [];
    s.tags.forEach(function (t) { tagged = tagged.concat(TAGGED[t] || []); });
    var pool = tagged.length && rand() < 0.6 ? tagged : GENERAL;
    return {
      text: ROD.pick(pool, rand).replace(/\{n\}/g, s.name),
      dates: ROD.pick(DATES, rand)
    };
  }

  function wrap(text, max) {
    var words = text.split(/\s+/), lines = [], line = "";
    words.forEach(function (w) {
      if ((line + " " + w).trim().length > max && line) { lines.push(line); line = w; }
      else { line = (line + " " + w).trim(); }
    });
    if (line) lines.push(line);
    return lines;
  }

  function el(tag, attrs, text) {
    var node = document.createElementNS(SVGNS, tag);
    Object.keys(attrs || {}).forEach(function (k) { node.setAttribute(k, attrs[k]); });
    if (text != null) node.textContent = text;
    return node;
  }

  function draw(s) {
    var c = s ? compose(s) : null;
    while (svg.lastChild && svg.lastChild.nodeName !== "title") svg.removeChild(svg.lastChild);

    var defs = el("defs");
    var g = el("radialGradient", { id: "stoneGrad", cx: "35%", cy: "25%", r: "80%" });
    g.appendChild(el("stop", { offset: "0", "stop-color": "#b0ada8" }));
    g.appendChild(el("stop", { offset: ".5", "stop-color": "#8d8a86" }));
    g.appendChild(el("stop", { offset: "1", "stop-color": "#4f4c49" }));
    defs.appendChild(g);
    svg.appendChild(defs);

    svg.appendChild(el("rect", { x: 0, y: 0, width: 400, height: 480, fill: "#0b0a0c" }));
    svg.appendChild(el("circle", { cx: 330, cy: 70, r: 34, fill: "#e9e2d0", opacity: ".85" }));
    svg.appendChild(el("circle", { cx: 318, cy: 62, r: 30, fill: "#0b0a0c" }));
    svg.appendChild(el("path", { d: "M60 440 V170 A140 140 0 0 1 340 170 V440 Z", fill: "url(#stoneGrad)", stroke: "#2a2826", "stroke-width": 3 }));
    svg.appendChild(el("path", { d: "M20 436 Q200 418 380 436 V480 H20 Z", fill: "#24331a" }));

    var font = "Georgia, 'Times New Roman', serif";
    var ink = "#1b1a19";
    function text(y, size, str, extra) {
      var a = { x: 200, y: y, "text-anchor": "middle", "font-family": font, "font-size": size, fill: ink };
      Object.keys(extra || {}).forEach(function (k) { a[k] = extra[k]; });
      svg.appendChild(el("text", a, str));
    }

    text(108, 34, "R.I.P.", { "font-weight": "bold", "letter-spacing": "4" });
    svg.appendChild(el("path", { d: "M150 124 H250", stroke: ink, "stroke-width": 1.5, opacity: ".6" }));

    if (!c) {
      text(200, 22, "HERE LIES", { "letter-spacing": "3" });
      text(250, 30, "Your Name", { "font-style": "italic", opacity: ".55" });
      text(310, 17, "Enter a name to begin", { opacity: ".55" });
      return;
    }
    text(170, 18, "HERE LIES", { "letter-spacing": "3" });
    var nameSize = s.name.length > 18 ? 24 : s.name.length > 12 ? 30 : 36;
    text(214, nameSize, s.name, { "font-weight": "bold" });
    text(244, c.dates.length > 28 ? 10.5 : 12, c.dates, { "letter-spacing": "1" });
    var lines = wrap(c.text, 22).slice(0, 6);
    var y0 = 290 + (4 - Math.min(lines.length, 4)) * 12;
    lines.forEach(function (ln, i) { text(y0 + i * 27, 21, ln, { "font-style": "italic" }); });
    svg.querySelector("title").textContent = "Tombstone of " + s.name + ": " + c.text;
  }

  function shareUrl(s) {
    var u = new URL(window.location.href);
    u.search = "";
    u.hash = "";
    u.searchParams.set("name", s.name);
    if (s.tags.length) u.searchParams.set("tags", s.tags.join(","));
    if (s.r) u.searchParams.set("r", String(s.r));
    return u.toString();
  }

  function render(s) {
    state = s;
    draw(s);
    [rerollBtn, downloadBtn, shareBtn].forEach(function (b) { b.disabled = false; });
    shareOut.textContent = "";
    try { history.replaceState(null, "", shareUrl(s)); } catch (e) { /* file:// and friends */ }
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var name = nameInput.value.trim().slice(0, 28);
    if (!name) { nameInput.focus(); return; }
    render({ name: name, tags: selectedTags(), r: 0 });
  });

  rerollBtn.addEventListener("click", function () {
    if (state) render({ name: state.name, tags: state.tags, r: state.r + 1 });
  });

  shareBtn.addEventListener("click", function () {
    if (!state) return;
    var url = shareUrl(state);
    var done = function () { shareOut.textContent = "Link copied. Send it to the deceased."; };
    var fail = function () { shareOut.textContent = url; };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, fail);
    else fail();
  });

  downloadBtn.addEventListener("click", function () {
    if (!state) return;
    var clone = svg.cloneNode(true);
    clone.setAttribute("xmlns", SVGNS);
    clone.setAttribute("width", "800");
    clone.setAttribute("height", "960");
    var blob = new Blob([new XMLSerializer().serializeToString(clone)], { type: "image/svg+xml;charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var img = new Image();
    img.onload = function () {
      var canvas = document.createElement("canvas");
      canvas.width = 800; canvas.height = 960;
      canvas.getContext("2d").drawImage(img, 0, 0, 800, 960);
      URL.revokeObjectURL(url);
      canvas.toBlob(function (png) {
        var a = document.createElement("a");
        a.href = URL.createObjectURL(png);
        a.download = "epitaph-" + state.name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") + ".png";
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
      }, "image/png");
    };
    img.onerror = function () { URL.revokeObjectURL(url); shareOut.textContent = "The stonemason dropped his chisel. Try again."; };
    img.src = url;
  });

  // Restore from a shared link
  var p = ROD.params();
  var initialName = (p.get("name") || "").trim().slice(0, 28);
  if (initialName) {
    var tags = (p.get("tags") || "").split(",").filter(function (t) { return TAGGED[t]; });
    nameInput.value = initialName;
    form.querySelectorAll("input[name=tags]").forEach(function (c) { c.checked = tags.indexOf(c.value) !== -1; });
    render({ name: initialName, tags: tags, r: Math.max(0, parseInt(p.get("r"), 10) || 0) });
  } else {
    draw(null);
  }
})();
