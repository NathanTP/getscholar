Generates a custom bibtex entry from a user's Google scholar profile using the
scholarly python package. This is intended to generate inputs to the
webfscholar python utility, the resulting references.bib may not be appropriate
for general use (e.g. the entry type and journal titles are not really
appropriate for a formal paper references section).

**Warning: Feel free to clone this and customize to your needs, but be warned
that it is highly tuned for my specific use-case and will be significantly less
useful to other people unless they modify it.**

# Usage
Build the webpage with:

  python sch.py "USER NAME"
  webfscholar

You can then do whatever you want with index.html (e.g. embed it in your
homepage).
