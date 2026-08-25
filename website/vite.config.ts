import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import { fileURLToPath } from "node:url";

// macOS Seatbelt blocks FSEvents, so Codex previews need polling for HMR.
const isCodexSeatbeltSandbox = process.env.CODEX_SANDBOX === "seatbelt";

export default defineConfig({
  base: "/awesome-claude-code-codex-papers/",
  plugins: [react()],
  build: {
    rollupOptions: {
      input: {
        catalog: fileURLToPath(new URL("./index.html", import.meta.url)),
        insights: fileURLToPath(
          new URL("./insights/index.html", import.meta.url),
        ),
        methods: fileURLToPath(
          new URL("./methods/index.html", import.meta.url),
        ),
        skill: fileURLToPath(
          new URL("./skill/index.html", import.meta.url),
        ),
      },
    },
  },
  server: isCodexSeatbeltSandbox
    ? { watch: { useFsEvents: false, usePolling: true } }
    : undefined,
});
