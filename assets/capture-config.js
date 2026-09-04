// Email capture provider.
//   buttondown -> forms POST natively to Buttondown's embed endpoint (no CORS, no key).
//                 Buttondown redirects: unconfirmed -> /prompted/guides/check-your-inbox/,
//                 confirmed -> /prompted/guides/confirmed/ (set in Buttondown > Settings > Subscribing).
//   stub       -> no network; shows the "check your inbox" state so the UI can be tested.
// Delivery rule: the PDF is never linked from the form; only the confirmed page links it.
window.PROMPTED_CAPTURE = {
  provider: "buttondown",
  endpoint: "https://buttondown.com/api/emails/embed-subscribe/cooperindustries",
  list: "prompted-fall-shot-list",
  confirmedPage: "/prompted/guides/confirmed/"
};
