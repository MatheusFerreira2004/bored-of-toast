// Content pillars (recipes; do/don't tips) are Supplied. Specific phrasing below
// is Proposed and should be validated once real reader feedback is available.
const valueProps = [
  {
    title: "Recipes that actually work",
    body: "Every recipe is written the way you'd want a friend to explain it, with no filler before the ingredients list.",
  },
  {
    title: "Know what to skip, not just what to do",
    body: "Alongside each recipe, get the specific mistakes and shortcuts to avoid, not just a generic method.",
  },
  {
    title: "Find it fast, no scrolling past your life story",
    body: "Recipes are structured so the content you saved on Pinterest or Facebook is easy to locate and use immediately.",
  },
  {
    title: "Ads that don't get in your way",
    body: "The site carries advertising to stay free, but it's designed to avoid predatory or disruptive ad placements.",
  },
];

export default function ValueProps() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-16">
      <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
        {valueProps.map((item) => (
          <div key={item.title} className="rounded-xl bg-white p-6 shadow-sm">
            <div className="mb-4 h-10 w-10 rounded-md bg-brand-mustard/20" />
            <h3 className="mb-2 text-base font-bold text-gray-900">
              {item.title}
            </h3>
            <p className="text-sm text-gray-600">{item.body}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
