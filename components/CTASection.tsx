// Secondary CTA per the Brief: Proposed, based on supplied traffic sources
// (Pinterest and Facebook). Links are placeholders — update hrefs once real
// social profile URLs are available. Visual styling updated to match design reference.
export default function CTASection() {
  return (
    <section id="follow" className="mx-auto max-w-6xl px-6 py-16 text-center">
      <h2 className="font-serif text-2xl font-semibold text-brand-ink">
        Come back for more from where you found this
      </h2>
      <p className="mx-auto mt-2 max-w-xl text-sm text-brand-ink/70">
        Follow along on the channels you already use for new recipes and
        tips.
      </p>
      <div className="mt-6 flex flex-wrap justify-center gap-3">
        <a
          href="#"
          className="rounded-md border border-brand-ink/20 px-5 py-2.5 text-sm font-bold text-brand-ink hover:bg-brand-ink hover:text-brand-cream"
        >
          Follow us on Pinterest
        </a>
        <a
          href="#"
          className="rounded-md border border-brand-ink/20 px-5 py-2.5 text-sm font-bold text-brand-ink hover:bg-brand-ink hover:text-brand-cream"
        >
          Follow us on Facebook
        </a>
      </div>
    </section>
  );
}
