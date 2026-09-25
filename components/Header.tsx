// Proposed nav structure. No page/route decisions were supplied, so links below
// are placeholders anchored to in-page sections until real recipe/category pages exist.
export default function Header() {
  return (
    <header className="w-full border-b border-gray-100">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-2">
          {/*
            Proposed placeholder mark — replace with the real "Bored of Toast" logo asset
            (bread-slice mascot wordmark) once the image file is added to /public.
          */}
          <span className="flex h-9 w-9 items-center justify-center rounded-md bg-brand-blue text-lg font-extrabold text-white">
            B
          </span>
          <span className="text-lg font-extrabold text-brand-blue">
            Bored of Toast
          </span>
        </div>
        <nav className="hidden gap-6 text-sm font-semibold text-gray-700 sm:flex">
          <a href="#recipes" className="hover:text-brand-blue">
            Recipes
          </a>
          <a href="#tips" className="hover:text-brand-blue">
            Do&apos;s &amp; Don&apos;ts
          </a>
          <a href="#follow" className="hover:text-brand-blue">
            Follow
          </a>
        </nav>
      </div>
    </header>
  );
}
