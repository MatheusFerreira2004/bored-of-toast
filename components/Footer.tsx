// Footer line reflects the supplied commitment that advertising will be
// non-predatory. Framing text is Proposed per the Brief's Trust Builders section.
export default function Footer() {
  return (
    <footer className="border-t border-gray-100 bg-white py-10">
      <div className="mx-auto max-w-6xl px-6 text-center text-xs text-gray-500">
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
