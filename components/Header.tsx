// Rebuilt per user-supplied design reference: serif wordmark + script tagline,
// centered nav with active-item underline, search field, and social icons (Pinterest/Facebook/Instagram).
// Nav links, search behavior, and social URLs are Proposed placeholders — no real
// recipe/category routes or social profile URLs were supplied yet.
export default function Header() {
  return (
    <header className="w-full border-b border-brand-tag bg-brand-cream">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6 py-5">
        <div>
          <div className="font-serif text-2xl font-semibold leading-tight text-brand-ink">
            Bored
            <br />
            of Toast
          </div>
          <div className="font-script text-lg text-brand-ink/70">
            Good food. Better instincts.
          </div>
        </div>

        <nav className="flex gap-6 text-sm font-medium text-brand-ink/80">
          <a href="#" className="hover:text-brand-ink">
            Home
          </a>
          <a
            href="#recipes"
            className="border-b-2 border-brand-mustard pb-1 text-brand-ink"
          >
            Recipes
          </a>
          <a href="#tips" className="hover:text-brand-ink">
            Kitchen Notes
          </a>
          <a href="#about" className="hover:text-brand-ink">
            About
          </a>
        </nav>

        <div className="flex items-center gap-4">
          {/* Proposed placeholder search — not wired to real search functionality yet. */}
          <div className="hidden items-center rounded-full border border-brand-ink/15 bg-white px-4 py-2 text-sm text-brand-ink/50 sm:flex">
            Search recipes...
          </div>
          <div className="flex gap-3 text-brand-ink/70">
            {/* Proposed placeholder social links — update hrefs once real profile URLs exist. */}
            <a href="#" aria-label="Pinterest" className="hover:text-brand-ink">
              P
            </a>
            <a href="#" aria-label="Facebook" className="hover:text-brand-ink">
              F
            </a>
            <a href="#" aria-label="Instagram" className="hover:text-brand-ink">
              I
            </a>
          </div>
        </div>
      </div>
    </header>
  );
}
