import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { MethodsPage } from "../app/MethodsPage";
import type { Paper } from "../app/CatalogExplorer";
import "../app/globals.css";
import catalog from "../data/catalog.json";

const root = document.getElementById("root");

if (!root) {
  throw new Error("Missing #root element");
}

createRoot(root).render(
  <StrictMode>
    <MethodsPage
      papers={catalog.papers as Paper[]}
      reviewedAt={catalog.reviewed_at}
    />
  </StrictMode>,
);
