import { useEffect, useRef, useState } from "react";

export const SITE_URL =
  "https://micromilo.github.io/awesome-claude-code-codex-papers/";

export function siteUrl(path = "") {
  return new URL(path.replace(/^\//, ""), SITE_URL).toString();
}

export async function copyText(value: string) {
  if (navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(value);
      return;
    } catch {
      // Browser extensions and embedded previews may deny the async clipboard API.
    }
  }

  const textarea = document.createElement("textarea");
  textarea.value = value;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.left = "0";
  textarea.style.top = "0";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.focus();
  textarea.select();
  textarea.setSelectionRange(0, textarea.value.length);
  const copied = document.execCommand("copy");
  textarea.remove();
  if (!copied) throw new Error("Clipboard write was rejected");
}

type Props = {
  path: string;
  label: string;
  copiedLabel: string;
  className?: string;
};

export function ShareButton({ path, label, copiedLabel, className }: Props) {
  const [copied, setCopied] = useState(false);
  const resetTimer = useRef<number | undefined>(undefined);

  useEffect(
    () => () => {
      if (resetTimer.current) window.clearTimeout(resetTimer.current);
    },
    [],
  );

  const handleCopy = async () => {
    await copyText(siteUrl(path));
    setCopied(true);
    if (resetTimer.current) window.clearTimeout(resetTimer.current);
    resetTimer.current = window.setTimeout(() => setCopied(false), 1800);
  };

  return (
    <button
      className={className ? `share-button ${className}` : "share-button"}
      type="button"
      onClick={handleCopy}
      aria-live="polite"
    >
      {copied ? copiedLabel : label}
    </button>
  );
}
