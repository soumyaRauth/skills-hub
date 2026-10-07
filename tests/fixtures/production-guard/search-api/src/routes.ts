import { search, show } from "./products/searchController.js";
import { importImage } from "./products/imageImport.js";

interface Router {
  get(path: string, handler: Function): void;
  post(path: string, handler: Function): void;
  group(middleware: string, register: (r: Router) => void): void;
}

export function register(router: Router): void {
  // Public catalogue: anyone can browse.
  router.get("/products/search", search);
  router.get("/products/:id", show);

  router.group("auth", (r) => {
    // Any signed-in seller can attach an image to their listing.
    r.post("/products/:id/image", importImage);
  });
}
