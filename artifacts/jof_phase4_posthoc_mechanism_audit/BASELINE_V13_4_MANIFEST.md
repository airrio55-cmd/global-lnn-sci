# JoF v13.4 editorial baseline manifest (document binaries stored in conversation ZIP)

This commit freezes the editorial baseline metadata after a manual clean-up of v13.3, preserving its empirical conclusions. This GitHub commit **does not contain the DOCX binary files**; their byte-exact versions are provided to the user as `JOF_v13_4_BASELINE.zip` and can be checked by SHA-256 below. No preregistered confirmation experiment was run at this step.

- Manuscript: `JOF_v13_4_MANUSCRIPT_BASELINE.docx` — SHA-256 `b29afa7b4bf677f6a6b437902a8b2aad557663c4599f503f2070d60fbc4d6468` (1,295,957 bytes).
- SI: `JOF_v13_4_SI_BASELINE.docx` — SHA-256 `113d3dfbcd214f8d527520a9a467e286166f582e433763a583b824b526207a53` (124,826 bytes).
- Cover letter: `JOF_v13_4_COVER_BASELINE.docx` — SHA-256 `76697932241e986cb137695c587115ef6d7fbd8722dc3d3445f462afde956284` (38,527 bytes).

Manual changes: correct Supporting Information S12, S13, S14, S15 malformed phase-name substitutions; S18 title and interpretive note no longer cite internal v11; manuscript sections 3.7 and 3.10 remove lingering internal phase references; combine duplicated 4.5 / 4.6 dependence sections into 4.5 and renumber secondary diagnostics to 4.6. Retain S9 historical Phase 1/2 descriptions as historical context. Figure 1 graphics and caption are unchanged at this baseline; new main figure may be developed separately once justified. Cover letter remains date-of-submission placeholder.

Protocol-lock analytical results remain at original frozen commits including `88f1acbc5dff7067966478f6c80c82ae9f2a00e2`. Later preregistered confirmatory experiments must be added as a distinct protocol and commit; they do not retroactively change this baseline.
