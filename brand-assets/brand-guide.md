# The Marker Group Brand Guide

## Brand Overview

The Marker Group is a higher education go-to-market consultancy. The brand should feel established, direct, and calm: more trusted advisor than startup hype.

## Logo System

The current identity is built around a refined golf-flag mark paired with a classic editorial wordmark. The flag keeps the brand tied to the "marker" idea without feeling sporty or novelty-driven, and it gives you a compact mark for favicon, social, and avatar use while the full wordmark carries best in website headers, decks, and documents.

### Core Logo Files

| File | Best Use |
|------|----------|
| `logos/marker-group-logo-dark.png` | Primary full logo on navy or dark backgrounds |
| `logos/marker-group-logo-light.png` | Full logo on white or light backgrounds |
| `logos/marker-group-logo-transparent.png` | Full logo when you need transparency |
| `logos/marker-group-stacked-dark.png` | Vertical layouts on dark backgrounds |
| `logos/marker-group-stacked-light.png` | Vertical layouts on light backgrounds |
| `logos/icon-navy.png` | Golf-flag icon on navy background |
| `logos/icon-white.png` | Golf-flag icon on white background |
| `logos/icon-transparent.png` | Transparent golf-flag icon |

### Web and Social Assets

| File | Best Use |
|------|----------|
| `logos/favicon.png` | Browser favicon |
| `logos/apple-touch-icon.png` | iOS home screen icon |
| `logos/social-profile.png` | Square social avatar |
| `logos/og-image.png` | Social share / Open Graph image |
| `logos/email-signature.png` | Compact mark for signatures or profile blocks |
| `logos/brand-palette.png` | Visual reference card for colors and typography |

### Usage Rules

- Keep clear space around the logo equal to the flag-mark height.
- Prefer the full wordmark for the website, proposals, and client-facing documents.
- Use the icon-only mark for favicons, profile images, and small-format placements.
- Do not stretch, recolor, rotate, outline, or add effects to the logo.
- Minimum width for the full logo: `120px`.
- Minimum width for the icon-only mark: `24px`.

## Color Palette

### Primary Colors

| Token | Hex | Usage |
|-------|-----|-------|
| Navy | `#0B1D35` | Primary background, main dark surface |
| Navy Mid | `#132B4D` | Secondary panels, cards, footer |
| Navy Light | `#1A3A5C` | Hover states, supporting dark surfaces |
| Copper | `#C19A6B` | Accent color, highlights, key dividers |
| Copper Light | `#D4B48E` | Softer accent and highlighted emphasis |
| Copper Dark | `#A67C52` | Active state on light surfaces |
| Off-White | `#F5F3EE` | Light sections and neutral background |
| Warm Gray | `#F2F0EB` | Subtle supporting surfaces |

### Text Colors

| Token | Value | Usage |
|-------|-------|-------|
| Text Dark | `#1C1C1C` | Headlines on light backgrounds |
| Text Body | `#3D3D3D` | Body copy on light backgrounds |
| Text Muted | `#6B7280` | Supporting copy on light backgrounds |
| Text on Dark | `rgba(255,255,255,0.75)` | Body copy on dark backgrounds |
| Text on Dark Muted | `rgba(255,255,255,0.45)` | Secondary copy on dark backgrounds |

## Typography

### Fonts

| Font | Usage |
|------|-------|
| `Lora` | Headlines, wordmark treatment, editorial emphasis |
| `Poppins` | Body text, navigation, buttons, labels |

### Website Scale

| Element | Font | Weight | Typical Size |
|---------|------|--------|--------------|
| H1 | Lora | 600 | `3.2rem` |
| H2 | Lora | 600 | `2.2rem` |
| H3 | Lora | 600 | `1.35rem` |
| Body | Poppins | 400 | `1rem` |
| Labels | Poppins | 600 | `0.75rem` uppercase |
| Buttons | Poppins | 600 | `0.95rem` |

### Font Files In Repo

- `fonts/Lora-Regular.ttf`
- `fonts/Lora-Italic.ttf`
- `fonts/Poppins-Light.ttf`
- `fonts/Poppins-Regular.ttf`
- `fonts/Poppins-Medium.ttf`
- `fonts/Poppins-SemiBold.ttf`
- `fonts/Poppins-Bold.ttf`

## Brand Voice

- Authoritative, but never stiff.
- Warm, without sounding casual or trendy.
- Specific and credible instead of over-claimed.
- Clear enough for founders, operators, and institutional buyers.

## Asset Workflow

- Edit `generate-logos.py` if the identity system evolves.
- Re-run the script to regenerate the website logo files in `/images` and the master files in `/brand-assets/logos`.
- Treat `/images` as website runtime assets and `/brand-assets` as the source-of-truth library.
