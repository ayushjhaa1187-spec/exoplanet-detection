# Task Board

## Phase 1-4: ML Pipeline & Scientific Refinement [DONE]
- [x] Preprocessing, Training, Inference, Vetting, Transit Fitting, and Architecture design completed.

## Phase 5: Dashboard & Final Presentation (Days 11-15)

### Day 11: Data Contract & App Initialization [DONE]
- [x] Define Types: `web/lib/types.ts`
- [x] Mock Data Contract: `metrics.json`, `candidates.json`, `candidate_[id].json`
- [x] Initialize Next.js, Tailwind, TypeScript in `web/`

### Day 12: Layout & Homepage (Next Task)
#### Current State
Empty Next.js boilerplate. Data contract exists in `public/data/`.
#### Proposed Changes
Build global navigation, dark theme layout, and the main hero/dashboard view explaining the 5-stage pipeline.
#### Files to Edit
`web/app/layout.tsx`, `web/app/page.tsx`, `web/components/layout/Sidebar.tsx`, `web/components/dashboard/StatsCard.tsx`, `web/components/dashboard/PipelineFlow.tsx`
#### Verification
`npm run dev` displays a dark-themed space dashboard with pipeline overview.

### Day 13: Candidate List & Details [DONE]
- [x] Create a sortable list of candidates and a detailed view showing the 5-stage vetting results.

### Day 14: Metrics, Reports & About Pages [DONE]
- [x] Visualize training metrics, list generated PDF reports, and explain project architecture.
- [x] Files Edit: `web/app/metrics/page.tsx`, `web/app/reports/page.tsx`, `web/app/about/page.tsx`

### Day 15: Polish & Submission [DONE]
- [x] Final visual QA, responsive design check, README updates.
- [x] Project successfully completed.
