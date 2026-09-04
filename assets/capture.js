(function () {
  var cfg = window.PROMPTED_CAPTURE || { provider: "stub" };
  document.querySelectorAll("form.capture-form").forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var email = form.querySelector("input[type=email]");
      var hp = form.querySelector("input[name=website]");
      var ok = form.parentNode.querySelector(".ok");
      var btn = form.querySelector("button");
      if (hp && hp.value) return;
      if (!email.checkValidity()) { email.reportValidity(); return; }
      btn.disabled = true;
      var payload = { email: email.value, source: form.dataset.source || location.pathname, list: cfg.list };
      var done = function () {
        form.hidden = true;
        ok.hidden = false;
        ok.textContent = "Check your inbox and tap the confirmation link. The PDF is on the other side of it.";
      };
      var fail = function () {
        btn.disabled = false;
        ok.hidden = false;
        ok.textContent = "That didn't go through. Try again in a moment, or email support@cooperindustries.cc.";
      };
      if (cfg.provider === "endpoint" && cfg.endpoint) {
        fetch(cfg.endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
          .then(function (r) { r.ok ? done() : fail(); }).catch(fail);
      } else {
        setTimeout(done, 300); // stub
      }
    });
  });
})();
