import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { InsightsPage } from "../app/InsightsPage";
import type { Paper } from "../app/CatalogExplorer";
import "../app/globals.css";
import catalog from "../data/catalog.json";
import pendingSummary from "../data/pending-summary.json";

const root = document.getElementById("root");

if (!root) {
  throw new Error("Missing #root element");
}

createRoot(root).render(
  <StrictMode>
    <InsightsPage
      papers={catalog.papers as Paper[]}
      reviewedAt={catalog.reviewed_at}
      pendingSummary={pendingSummary}
    />
  </StrictMode>,
);
