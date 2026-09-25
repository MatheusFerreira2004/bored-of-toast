// Maps to the supplied content model (recipes, do/don't tips, non-predatory ads).
// The digital product is intentionally NOT rendered here — it is still undecided
// per the Landing Page Brief ("Digital product: Unknown / to be decided").
export default function FeatureShowcase() {
  return (
    <section id="recipes" className="bg-white py-16">
      <div className="mx-auto max-w-6xl px-6">
        <div className="grid gap-10 md:grid-cols-3">
          <div>
            <h3 className="text-lg font-bold text-gray-900">
              Full recipe library
            </h3>
            <p className="mt-2 text-sm text-gray-600">
              Browse recipes by category, meal type, or ingredient, structured
              to match the way readers search on Pinterest and Facebook.
            </p>
            <div className="mt-4 h-32 rounded-lg border-2 border-dashed border-gray-200" />
          </div>
          <div id="tips">
            <h3 className="text-lg font-bold text-gray-900">
              Do&apos;s and don&apos;ts for every recipe
            </h3>
            <p className="mt-2 text-sm text-gray-600">
              Each recipe includes a short section on common mistakes and
              technique tips, distinct from the step-by-step instructions.
            </p>
            <div className="mt-4 grid grid-cols-2 gap-2">
              <div className="rounded-lg bg-green-50 p-3 text-xs font-semibold text-green-700">
                Do
              </div>
              <div className="rounded-lg bg-red-50 p-3 text-xs font-semibold text-red-700">
                Don&apos;t
              </div>
            </div>
          </div>
          <div>
            <h3 className="text-lg font-bold text-gray-900">
              A cleaner way to read recipes
            </h3>
            <p className="mt-2 text-sm text-gray-600">
              Ad placements are positioned to support the site financially
              without interrupting the recipe itself.
            </p>
            <div className="mt-4 h-32 rounded-lg border-2 border-dashed border-gray-200" />
          </div>
        </div>
      </div>
    </section>
  );
}
