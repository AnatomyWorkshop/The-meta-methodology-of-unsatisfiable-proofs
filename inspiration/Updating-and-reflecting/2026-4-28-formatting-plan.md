# Formatting Plan for 2026-4-28-full-paper.md

> Date: 2026-04-28
> Status: COMPLETE

## Changes made

1. ✅ Removed all draft metadata blockquotes (Status/Role/Design principle) from all seven chapters.
2. ✅ Fixed heading levels: all `####` converted to `###` throughout the file.
3. ✅ Removed per-chapter "Notes and References" sections; replaced with one-line pointer to consolidated References.
4. ✅ Added consolidated References section at end of file (alphabetical by first author, 20 entries).
5. ✅ Excess `---` separators within subsections: reviewed — none were present between sub-steps after the heading level fix; separators between major sections retained.
6. ✅ Fixed title block: split into `# Title` and `## Subtitle` with separator.

## Result

The file now reads as a single paper rather than a collection of chapter drafts. Heading hierarchy is consistent throughout (## chapters, ### sections, no ####). All references are in one place at the end.

> Date: 2026-04-28
> Goal: Make the combined draft look like a single coherent paper, not a collection of chapter files.

---

## Changes to make

### 1. Remove all draft metadata headers

Every chapter currently opens with a blockquote block like:

> Status: First draft
> Role: ...
> Design principle: ...

These are working notes, not paper content. Remove all of them.

### 2. Fix heading levels

Currently the file uses `##` for chapter titles and `###` for section headings. This is correct. But the sub-steps inside chapters (e.g. "Step 1", "Step 2") use `####` — one level too deep for a flat paper. Flatten these to `###` to match the other section headings.

Affected sections:
- Ch. 3 §3.3: "#### Step 1/2/3/4" → "### Step 1/2/3/4"  
- Ch. 4 §4.3: same
- Ch. 5 §5.3: "#### Step 1/2/3/4" → "### Step 1/2/3/4"
- Ch. 6 §6.2: "#### The Three Laws..." → "### The Three Laws..."
- Ch. 6 §6.3: "#### 6.3.1/6.3.2/..." → "### 6.3.1/6.3.2/..."
- Ch. 6 §6.5: "#### 6.5.1/6.5.2/6.5.3" → "### 6.5.1/6.5.2/6.5.3"
- Ch. 6 §6.7: "#### 6.7.1/..." → "### 6.7.1/..."

### 3. Consolidate all "Notes and References" into a single References section at the end

Currently each chapter ends with its own "### Notes and References" block. For a paper, these should be a single consolidated reference list at the end.

Collect all references from:
- Ch. 2 Notes and References
- Ch. 3 Notes and References
- Ch. 4 Notes and References
- Ch. 5 Notes and References
- Ch. 6 Notes and References

Deduplicate, sort alphabetically by author, and place as a single "## References" section after Chapter 7.

Remove the per-chapter "Notes and References" sections (or replace with a one-line pointer: "See References.").

### 4. Remove the double `---` separators between minor subsections

Inside chapters, many subsections are separated by `---` even when they are just consecutive numbered steps. This creates visual clutter. Keep `---` only between top-level sections (between chapters, and between major numbered sections like §3.3 and §3.4). Remove `---` between sub-steps within a section.

### 5. Add a title block at the top

Replace the current bare `# Title` line with a proper title block:

```
# A Meta-Methodology of Unsatisfiable Proofs
## Self-Referential Safety and the Structure of Lower Bounds

---
```

### 6. Minor: remove trailing blank lines and double blank lines throughout

---

## Consolidated reference list (draft)

Sorted alphabetically by first author:

- Aaronson, S. and Wigderson, A. (2009). "Algebrization: A new barrier in complexity theory." *ACM Transactions on Computation Theory* 1(1).
- Arora, S. and Barak, B. (2009). *Computational Complexity: A Modern Approach*. Cambridge University Press.
- Baker, T., Gill, J., and Solovay, R. (1975). "Relativizations of the P =? NP question." *SIAM Journal on Computing* 4(4).
- Boolos, G. (1993). *The Logic of Provability*. Cambridge University Press.
- Boolos, G. and Jeffrey, R. (1989). *Computability and Logic*. Cambridge University Press.
- Chaitin, G. (1974). "Information-theoretic limitations of formal systems." *Journal of the ACM* 21(3).
- Feferman, S. (1962). "Transfinite recursive progressions of axiomatic theories." *Journal of Symbolic Logic* 27(3).
- Furst, M., Saxe, J. B., and Sipser, M. (1984). "Parity, circuits, and the polynomial-time hierarchy." *Mathematical Systems Theory* 17(1).
- Gödel, K. (1931). "Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I." *Monatshefte für Mathematik und Physik* 38.
- Håstad, J. (1986). *Computational Limitations of Small-Depth Circuits*. PhD thesis, MIT.
- Impagliazzo, R. and Wigderson, A. (1997). "P = BPP if E requires exponential circuits: Derandomizing the XOR lemma." *Proceedings of STOC 1997*.
- Krajíček, J. (2019). *Proof Complexity*. Cambridge University Press.
- Kumar, M. and Saraf, S. (2016). "Shattering Randomness with the Sum of Squares Hierarchy." *Proceedings of STOC 2016*. *(Note: verify exact citation for the depth-4 lower bound paper.)*
- Lakatos, I. (1976). *Proofs and Refutations*. Cambridge University Press.
- Mulmuley, K. and Sohoni, M. (2001). "Geometric complexity theory I." *SIAM Journal on Computing* 31(2).
- Razborov, A. A. (1985). "Lower bounds for the monotone complexity of some Boolean functions." *Soviet Mathematics Doklady* 31.
- Razborov, A. A. and Rudich, S. (1994). "Natural proofs." *Journal of Computer and System Sciences* 55(1).
- Shapiro, S. (1991). *Foundations without Foundationalism*. Oxford University Press.
- Smullyan, R. (1992). *Gödel's Incompleteness Theorems*. Oxford University Press.
- Tao, T. (2007). "Soft analysis, hard analysis, and the finite convergence principle." Essay, available at terrytao.wordpress.com.

---

## Order of operations

1. Remove draft metadata blockquotes (all chapters)
2. Fix heading levels (#### → ### where needed)
3. Remove per-chapter Notes and References sections; replace with pointer line
4. Add consolidated References section at end
5. Remove excess `---` separators within subsections
6. Fix title block

I can execute these in order. Each step is mechanical and reversible.
