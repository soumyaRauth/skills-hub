import i18next from "./i18n.js";

export function renderCart(cart, user) {
  const t = i18next.t;

  return [
    t("greeting", { name: user.firstName }),
    t("checkout:itemsInCart", { count: cart.items.length }),
    t("checkout:tax", { rate: cart.taxRate }),
    t("checkout:total", { amount: "$" + cart.total.toFixed(2) }),
    t("common:lastSeen", { date: new Date(user.lastSeenAt).toLocaleDateString("en-US") }),
  ];
}

export function stockLabel(product) {
  // rendered under the "Add to cart" button
  return i18next.t("checkout:left", { count: product.stock });
}
