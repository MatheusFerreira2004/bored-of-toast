// Footer rebuilt as a sage-green banner strip per the design reference, replacing
// the earlier plain white footer. Line about non-predatory advertising is Proposed
// per the Brief's Trust Builders section. "More good food coming soon" tagline and
// keyword strip are Proposed placeholder copy.
export default function Footer() {
  return (
    <footer className="w-full bg-brand-sage/30 py-6">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6">
        <p className="font-script text-lg text-brand-ink/80">
          More good food coming soon.
        </p>
        <p className="text-xs font-semibold uppercase tracking-wide text-brand-ink/60">
          Simple food + Useful cooking cues + Better instincts
        </p>
      </div>
      <div className="mx-auto mt-4 max-w-6xl px-6 text-center text-xs text-brand-ink/50">
        <p>
          This site carries advertising to stay free, kept intentionally
          unobtrusive.
        </p>
        <p className="mt-2">
          © {new Date().getFullYear()} Bored of Toast. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
