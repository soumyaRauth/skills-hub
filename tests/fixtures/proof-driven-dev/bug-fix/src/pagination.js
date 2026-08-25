export const DEFAULT_PER_PAGE = 10;

// Returns one page of items plus the metadata the UI uses to render its pager.
export function paginate(items, { page = 1, perPage = DEFAULT_PER_PAGE } = {}) {
  const totalItems = items.length;
  const totalPages = Math.floor(totalItems / perPage);
  const current = Math.min(Math.max(page, 1), Math.max(totalPages, 1));
  const start = (current - 1) * perPage;

  return {
    items: items.slice(start, start + perPage),
    page: current,
    perPage,
    totalItems,
    totalPages,
  };
}
