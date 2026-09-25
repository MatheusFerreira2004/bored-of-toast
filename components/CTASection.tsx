// Secondary CTA per the Brief: Proposed, based on supplied traffic sources
// (Pinterest and Facebook). Links are placeholders — update hrefs once real
// social profile URLs are available.
export default function CTASection() {
  return (
    <section id="follow" className="mx-auto max-w-6xl px-6 py-16 text-center">
      <h2 className="text-2xl font-extrabold text-gray-900">
        Come back for more from where you found this
      </h2>
      <p className="mx-auto mt-2 max-w-xl text-sm text-gray-600">
        Follow along on the channels you already use for new recipes and
        tips.
      </p>
      <div className="mt-6 flex flex-wrap justify-center gap-3">
        <a
          href="#"
          className="rounded-md border border-brand-blue px-5 py-2.5 text-sm font-bold text-brand-blue hover:bg-brand-blue hover:text-white"
        >
          Follow us on Pinterest
        </a>
        <a
          href="#"
          className="rounded-md border border-brand-blue px-5 py-2.5 text-sm font-bold text-brand-blue hover:bg-brand-blue hover:text-white"
        >
          Follow us on Facebook
        </a>
      </div>
    </section>
  );
}
