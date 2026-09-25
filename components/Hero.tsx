// Hero copy and layout remain Proposed in the Landing Page Brief, pending a confirmed
// Conversion Goal. Visual styling updated to match the new cream/ink/mustard design reference.
export default function Hero() {
  return (
    <section className="mx-auto grid max-w-6xl gap-10 px-6 py-16 sm:py-24 md:grid-cols-2 md:items-center">
      <div>
        <h1 className="font-serif text-4xl font-semibold leading-tight text-brand-ink sm:text-5xl">
          Recipes worth leaving toast for
        </h1>
        <p className="mt-4 font-script text-2xl text-brand-ink/70">
          Real recipes, honest tips, and the do&apos;s and don&apos;ts nobody
          tells you — pulled straight from the pins and posts you save.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          {/* Proposed CTA — pending confirmed Conversion Goal (browse vs. email capture vs. product). */}
          <a
            href="#recipes"
            className="inline-flex items-center gap-2 rounded-md bg-brand-mustard px-6 py-3 text-sm font-bold text-brand-ink shadow-sm hover:opacity-90"
          >
            Browse recipes →
          </a>
        </div>
      </div>
      <div className="flex items-center justify-center">
        {/*
          Proposed hero visual placeholder — replace with a lifestyle photo of a
          featured finished dish once recipe photography is available (see design
          reference for target photo style: warm, close-up, editorial food photography).
        */}
        <div className="flex h-64 w-full max-w-md items-center justify-center rounded-2xl border-2 border-dashed border-brand-mustard bg-white text-center text-sm font-semibold text-brand-ink/40 sm:h-80">
          Featured recipe photo
          <br />
          (placeholder — add real photography)
        </div>
      </div>
    </section>
  );
}
