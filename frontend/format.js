// Shared formatting helpers so date/currency display stays
// consistent across GigCard, GigDetail, and anywhere else that
// needs it, instead of repeating the same logic in each component.

export function formatDate(dateString, options = { day: "numeric", month: "short" }) {
  return new Date(dateString).toLocaleDateString("en-IN", options);
}

export function formatCurrency(amount) {
  return `₹${Number(amount).toLocaleString("en-IN")}`;
}