import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, relative } from "node:path";
import { describe, expect, it } from "vitest";

const ROOT = process.cwd();
const COMPONENT_DIRS = ["components", "pages"];
const UTILITY_CLASS_PATTERNS = [
  /\bflex-grow\b/,
  /\bitems-center\b/,
  /\bjustify-center\b/,
  /\btext-slate-\d+\b/,
  /\bbg-slate-\d+\b/,
  /\bborder-slate-\d+\b/,
  /\brounded-(?:full|xl|2xl|3xl|lg|md)\b/,
  /\bshadow-(?:sm|lg|xl|2xl)\b/,
  /\bspace-y-\d+\b/,
  /\b(?:p|px|py|pt|pb|pl|pr)-\d+\b/,
  /\b(?:w|h)-\d+\b/,
  /\bfont-(?:bold|semibold|medium|extrabold|mono)\b/,
  /\b(?:hover|disabled|active|focus|sm|md):/,
];

const walk = (dir: string): string[] => {
  return readdirSync(dir).flatMap((entry) => {
    const path = join(dir, entry);
    return statSync(path).isDirectory() ? walk(path) : [path];
  });
};

const publicComponentTsxFiles = (): string[] => {
  return COMPONENT_DIRS.flatMap((dir) => walk(join(ROOT, dir)))
    .filter((path) => path.endsWith(".tsx"))
    .filter((path) => !path.endsWith(".test.tsx"));
};

describe("public UIX styling boundary", () => {
  it("keeps runtime styling in CSS files instead of HTML or JSX inline styles", () => {
    const html = readFileSync(join(ROOT, "index.html"), "utf8");
    expect(html).not.toContain("cdn.tailwindcss.com");
    expect(html).not.toContain("<style");
    expect(html).not.toContain(" class=");

    for (const file of publicComponentTsxFiles()) {
      const source = readFileSync(file, "utf8");
      expect(source, relative(ROOT, file)).not.toContain("style=");
    }
  });

  it("requires each public component and page to own a CSS file", () => {
    for (const file of publicComponentTsxFiles()) {
      const cssFile = file.replace(/\.tsx$/, ".css");
      const source = readFileSync(file, "utf8");
      expect(statSync(cssFile).isFile(), relative(ROOT, cssFile)).toBe(true);
      expect(source, relative(ROOT, file)).toContain(`./${cssFile.split(/[\\/]/).pop()}`);
    }
  });

  it("does not embed Tailwind-style utility classes in JSX className values", () => {
    for (const file of publicComponentTsxFiles()) {
      const source = readFileSync(file, "utf8");
      const classNameValues = source.match(/className=(?:"[^"]*"|\{`[^`]*`\})/g) ?? [];
      for (const value of classNameValues) {
        for (const pattern of UTILITY_CLASS_PATTERNS) {
          expect(value, `${relative(ROOT, file)}: ${value}`).not.toMatch(pattern);
        }
      }
    }
  });
});
