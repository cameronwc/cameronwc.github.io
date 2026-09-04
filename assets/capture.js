(function () {
  var cfg = window.PROMPTED_CAPTURE || { provider: "stub" };
  document.querySelectorAll("form.capture-form").forEach(function (form) {
    var source = form.dataset.source || location.pathname;
    if (cfg.provider === "buttondown" && cfg.endpoint) {
      // Native POST: Buttondown handles double opt-in and both redirects.
      form.action = cfg.endpoint;
      form.method = "post";
      var add = function (name, value) {
        var i = document.createElement("input"); i.type = "hidden"; i.name = name; i.value = value; form.appendChild(i);
      };
      add("embed", "1");
      add("tag", source);          // where they signed up, as a subscriber tag
      add("tag", cfg.list);        // the lead magnet
    }
    form.addEventListener("submit", function (ev) {
      var email = form.querySelector("input[type=email]");
      var hp = form.querySelector("input[name=website]");
      var ok = form.parentNode.querySelector(".ok");
      var btn = form.querySelector("button");
      if (hp && hp.value) { ev.preventDefault(); return; }
      if (!email.checkValidity()) { ev.preventDefault(); email.reportValidity(); return; }
      if (cfg.provider === "buttondown" && cfg.endpoint) { btn.disabled = true; return; } // let it submit
      ev.preventDefault();
      btn.disabled = true;
      form.hidden = true; ok.hidden = false;
      ok.textContent = "Check your inbox and tap the confirmation link. The PDF is on the other side of it.";
    });
  });
})();
