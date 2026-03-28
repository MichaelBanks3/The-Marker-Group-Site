# The Marker Group — Design Overhaul Spec

**Date:** 2026-03-28
**Scope:** Visual/design overhaul only. Content is placeholder — will be replaced later.
**Approach:** B + dark-mode-first from C. Single-page architecture.

---

## 1. Visual System

### Color Hierarchy
- **Primary canvas:** Navy `#0B1D35` — default background for most sections
- **Depth layer:** Navy-mid `#132B4D` — cards, recessed panels, footer, subtle section shifts
- **Contrast sections:** Off-white `#F8F7F4` — used sparingly (trust bar, CTA) as palate cleansers
- **Accent:** Copper `#C19A6B` — thin rules, hover states, highlighted words. NOT button fills on dark backgrounds
- **Copper-light `#D4B48E`** for italicized/emphasized headline words
- **Copper-dark `#A67C52`** for hover states on light backgrounds

### Typography
- **Headings:** Lora serif, 600 weight. Full `#FFFFFF` on dark backgrounds (not 0.85 alpha).
- **Body:** Poppins sans, 300-400 weight. `rgba(255,255,255,0.75)` on dark, `#3D3D3D` on light.
- **Labels:** Poppins, 600 weight, 0.78rem, uppercase, `letter-spacing: 0.12em`, copper color.
- **Scale:** Same clamp-based responsive sizing as current.

### Button System
- **Primary:** White background, navy text. High contrast on dark canvas.
- **Secondary/Ghost:** Transparent, 1px white border, white text.
- **Accent links:** Copper text + arrow, no background. Inline "learn more" style.
- **On light backgrounds:** Primary becomes navy background, white text.

### The Marker Motif
- Thin diagonal line (~2-3 deg) echoing the flag angle in the logo
- Appears as: clip-path on 1-2 section transitions, thin copper decorative rules near headings
- Used sparingly — 2-3 instances total across the page

---

## 2. Page Architecture

**Single page.** Nav becomes anchor links. Core marketing story told as one scroll.

### Section Flow

#### 2.1 Header (fixed)
- Logo left, nav links + CTA right
- Starts transparent over hero
- On scroll (>50px): navy-mid background, backdrop-blur(12px), subtle bottom border
- Desktop nav visible >900px. Hamburger at <=900px.
- CTA button: ghost style (copper border, copper text) — becomes white border on scroll

#### 2.2 Hero — Navy, full viewport
- `min-height: 100vh`, content vertically centered
- Asymmetric grid: `1fr 360px` at desktop
- Left: label, headline, subtitle, two CTA buttons (primary white + ghost)
- Right: 3 stat cards staggered vertically (translateY offsets: 0, 20px, 40px)
- Thin copper diagonal line as decorative element behind stat cards
- Cards: navy-mid background, 1px `rgba(255,255,255,0.08)` border, rounded 10px

#### 2.3 Trust Bar — Off-white
- Angled top edge: `clip-path: polygon(0 20px, 100% 0, 100% 100%, 0 100%)` (subtle 2deg)
- Compact: ~100px padding total
- Scrolling logo carousel, grayscale, hover to color
- Mask gradient on edges for fade effect

#### 2.4 Story — Navy
- Two-column grid: `1fr 1fr`, 5rem gap
- Left: sticky heading with thin copper rule above (the motif)
- Right: narrative paragraphs, lead paragraph slightly larger/bolder
- Padding: 5rem top, 6rem bottom (asymmetric)

#### 2.5 Services — Navy-mid
- Background shifts to navy-mid for depth
- Section header: label + headline, left-aligned, max-width 560px
- 3 service rows: grid `60px 1fr 40px`
- Separated by thin `rgba(255,255,255,0.08)` top borders
- Hover: left copper border appears (3px), arrow slides right, subtle background shift

#### 2.6 Why / Differentiators — Navy
- Back to navy for contrast with navy-mid services
- Section header: label + headline
- 2x2 grid, staggered: left column items have no extra offset, right column items get `margin-top: 3rem` to break the grid
- Each item: large faded number (copper at 0.12 opacity) behind heading, thin top border
- First item gets slightly larger heading (1.3rem vs 1.15rem)

#### 2.7 CTA — Off-white
- Angled top edge matching trust bar angle
- Centered: headline, one line of copy, navy button ("Start a Conversation")
- Below button: email in small muted text
- Tight padding: 5rem top, 4rem bottom

#### 2.8 Footer — Navy-mid
- Thin copper rule across the top
- Single row: logo (reduced opacity) + copyright left, nav links right
- Compact: 3rem padding

---

## 3. Motion & Interactions

### Scroll Reveals
- IntersectionObserver-based, but varied:
  - Headings: fade in + translateY(20px), 0.7s ease
  - Body/cards: fade in + translateY(12px), 0.6s ease
  - Staggered children: 80ms delay increment
  - Stat cards: staggered with 100ms increments
- Threshold: 0.15, rootMargin: `0px 0px -40px 0px`
- Hero stat cards animate on load (short delay, not scroll-triggered) since they're above the fold

### Hover States
- Service rows: left copper border slides in, arrow translateX(4px), background lightens
- Nav links: copper color transition
- CTA button: subtle translateY(-1px) + box-shadow
- Trust logos: grayscale to color, opacity increase
- Footer links: copper color

### Header Transition
- Background: transparent to navy-mid over 0.35s
- Backdrop-filter: none to blur(12px)
- Box-shadow fades in

### Logo Carousel
- CSS keyframes, 40s linear infinite
- Mask gradient on edges
- Duplicated track for seamless loop

---

## 4. Responsive Breakpoints

### Desktop (>900px)
- Full two-column layouts (hero, story, why)
- Desktop nav visible
- Staggered grid in why section
- Clip-path angles at full 2deg

### Tablet (768-900px)
- Columns collapse to single
- Hamburger nav
- Staggered why grid flattens
- Clip-path angles reduce to 1deg

### Mobile (<768px)
- Everything single column
- Stat cards stack vertically
- Min 44px tap targets
- Hero min-height: auto (not 100vh — content determines height)
- Padding scales down proportionally

---

## 5. Files

- `index.html` — single page with all sections
- `style.css` — full rewrite
- `about.html` / `services.html` — removed (or redirect to index.html anchors)
- `images/` — unchanged (logos and brand assets)

---

## 6. What's NOT In Scope
- Content changes (placeholder only)
- New images or illustrations
- Blog/case study pages
- Contact form functionality
- Analytics or tracking
- Deployment/hosting
