"""Reference chart data, one module per chart.

Each module in this package exposes a module-level PAGE dict and a SLUG
string. postbuild_reference.discover() picks them up automatically, so a
new chart is a new file here and nothing else changes: no edit to an
existing module, no new script, no change to vercel.json.

The dict shape is the one reference_content.body() already renders:

    title, h1, dek, description   strings
    intro                         list of paragraphs
    rule                          dict(eyebrow, items, example)
    tables                        list of dict(heading, note, caption,
                                  headers, highlight, rows)
    exceptions                    list of (heading, [paragraphs])
    safety                        dict or None
    sources                       list of (title, publisher, url, note)
    related                       list of (url, label)

Every factual claim in a chart needs a source in that last list. Values
that cannot be sourced do not go in the table.
"""
