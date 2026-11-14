// Carries a visit's utm_source / utm_campaign into the App Store campaign
// token (ct) on every Prompted App Store link, so App Store Connect
// (Analytics → Acquisition → Campaigns) can split installs by where the
// visitor came from: e.g. a Pinterest text pin landing on a guide becomes
// ct=pin-text-g-golden-hour-prompts. The static href already carries pt=
// and the page's own ct, so links still attribute with JS off.
// Source survives navigation within the site via sessionStorage.
(function () {
  var KEY = "prompted-utm";
  var SHORT = { pinterest: "pin", reels: "reel", producthunt: "ph", instagram: "ig", facebook: "fb", threads: "th" };
  function clean(s) { return (s || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""); }
  var q = new URLSearchParams(location.search);
  var src = clean(q.get("utm_source")), camp = clean(q.get("utm_campaign"));
  try {
    if (src) sessionStorage.setItem(KEY, JSON.stringify([src, camp]));
    else { var saved = JSON.parse(sessionStorage.getItem(KEY) || "null"); if (saved) { src = saved[0]; camp = saved[1]; } }
  } catch (e) {}
  if (!src) return;
  var prefix = (SHORT[src] || src.slice(0, 8)) + (camp && camp !== src ? "-" + camp.slice(0, 10) : "");
  document.querySelectorAll('a[href*="apps.apple.com/"][href*="id6807112342"]').forEach(function (a) {
    try {
      var u = new URL(a.href);
      var ct = u.searchParams.get("ct");
      u.searchParams.set("ct", (prefix + (ct ? "-" + ct : "")).slice(0, 40).replace(/-$/, ""));
      a.href = u.toString();
    } catch (e) {}
  });
})();
