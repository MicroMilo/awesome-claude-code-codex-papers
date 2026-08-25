import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import {
  CatalogExplorer,
  type CensusSummary,
  type Paper,
} from "../app/CatalogExplorer";
import "../app/globals.css";
import catalog from "../data/catalog.json";
import censusSummary from "../data/census-summary.json";

const root = document.getElementById("root");

if (!root) {
  throw new Error("Missing #root element");
}

createRoot(root).render(
  <StrictMode>
    <CatalogExplorer
      papers={catalog.papers as Paper[]}
      reviewedAt={catalog.reviewed_at}
      censusSummary={censusSummary as CensusSummary}
    />
  </StrictMode>,
);
