// Email capture provider. Switch `provider` once one is chosen; nothing else changes.
//   stub      -> no network; shows the "check your inbox" state so the UI can be tested
//   endpoint  -> POST JSON {email, source, list} to `endpoint`; expect 2xx
// Delivery rule: the PDF is never linked from the form. The provider's confirmation
// email must link to /prompted/guides/confirmed/ which is the only page that links the file.
window.PROMPTED_CAPTURE = {
  provider: "stub",
  endpoint: "",
  list: "prompted-fall-shot-list",
  confirmedPage: "/prompted/guides/confirmed/"
};
