import catalog from "@/data/catalog.json";
import { CatalogExplorer, type Paper } from "./CatalogExplorer";

export default function Home() {
  return (
    <CatalogExplorer
      papers={catalog.papers as Paper[]}
      reviewedAt={catalog.reviewed_at}
    />
  );
}
