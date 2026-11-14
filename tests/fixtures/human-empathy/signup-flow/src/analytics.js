export function track(event, props = {}) {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event, ...props });
}
