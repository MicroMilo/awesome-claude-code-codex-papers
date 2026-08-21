import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { headers } from "next/headers";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const title = "Awesome Claude Code & Codex Papers";
const description =
  "A readable, evidence-first index of methods that evaluate, analyze, or outperform production coding agents.";

export async function generateMetadata(): Promise<Metadata> {
  const requestHeaders = await headers();
  const forwardedHost = requestHeaders.get("x-forwarded-host")?.split(",")[0];
  const host = forwardedHost ?? requestHeaders.get("host") ?? "localhost:3000";
  const forwardedProtocol = requestHeaders.get("x-forwarded-proto")?.split(",")[0];
  const protocol = forwardedProtocol ?? (host.startsWith("localhost") ? "http" : "https");
  const origin = `${protocol}://${host}`;
  const socialImage = new URL("/og.png", origin).toString();

  return {
    metadataBase: new URL(origin),
    applicationName: "Agent Papers",
    title,
    description,
    keywords: [
      "Claude Code",
      "Codex CLI",
      "coding agents",
      "software engineering research",
      "LLM agents",
    ],
    creator: "Awesome Claude Code & Codex Papers contributors",
    publisher: "Awesome Claude Code & Codex Papers",
    category: "research",
    manifest: "/manifest.webmanifest",
    icons: { icon: "/icon.svg" },
    robots: { index: true, follow: true },
    alternates: { canonical: origin },
    openGraph: {
      title,
      description,
      type: "website",
      siteName: "Agent Papers",
      images: [{ url: socialImage, width: 1731, height: 909, alt: title }],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [socialImage],
    },
  };
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        {children}
      </body>
    </html>
  );
}
