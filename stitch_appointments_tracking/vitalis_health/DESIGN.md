# Design System Specification: The Clinical Atelier

## 1. Overview & Creative North Star

### Creative North Star: "The Ethereal Clinic"
This design system rejects the sterile, rigid boxiness of traditional healthcare portals in favor of a "High-End Editorial" experience. We aim for **The Ethereal Clinic**—a space that feels as professional as a world-class hospital but as calming as a high-end wellness retreat. 

To break the "template" look, we employ **Intentional Asymmetry** and **Tonal Depth**. Instead of centering everything, we use generous, purposeful white space to draw the eye to critical data. We move away from "UI components" and toward "Information Architecture as Art." By overlapping elements (e.g., a high-resolution medical icon bleeding off the edge of a card) and using a dramatic typography scale, we create an interface that feels curated, not just assembled.

---

## 2. Colors & Surface Philosophy

The palette leverages the psychology of trust (Primary Blue) and growth (Secondary Green), but the execution is where we differentiate.

### The "No-Line" Rule
**Borders are a design failure of the past.** In this system, 1px solid strokes are strictly prohibited for sectioning. Structural boundaries must be defined exclusively through:
1.  **Background Color Shifts:** Placing a `surface-container-low` section against a `surface` background.
2.  **Generous Negative Space:** Using the Spacing Scale (e.g., `spacing-12` or `spacing-16`) to create a cognitive break between content blocks.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers—like stacked sheets of fine vellum paper.
- **Base Layer:** `surface` (#f7f9fb)
- **Content Zones:** `surface-container-low` (#f2f4f6)
- **Actionable Cards:** `surface-container-lowest` (#ffffff)
- **Deep Context:** `surface-container-high` (#e6e8ea) for utility sidebars.

### The "Glass & Gradient" Rule
To add "soul" to the clinical environment, use **Glassmorphism** for floating elements (modals, dropdowns). Use a `surface` color at 70% opacity with a `24px` backdrop-blur. 
*Signature Polish:* For primary CTAs, apply a subtle linear gradient from `primary` (#00488d) to `primary_container` (#005fb8) at a 135-degree angle. This adds a tactile, premium depth that flat hex codes cannot replicate.

---

## 3. Typography: Editorial Authority

We pair **Manrope** (Display/Headline) for a modern, architectural feel with **Inter** (Body/Label) for clinical legibility.

| Level | Token | Font | Size | Character |
| :--- | :--- | :--- | :--- | :--- |
| **Display** | `display-lg` | Manrope | 3.5rem | Light (300), -0.02em tracking |
| **Headline** | `headline-md` | Manrope | 1.75rem | Medium (500), Professional |
| **Title** | `title-lg` | Inter | 1.375rem | Semi-bold (600), High-trust |
| **Body** | `body-md` | Inter | 0.875rem | Regular (400), 1.6 line-height |
| **Label** | `label-md` | Inter | 0.75rem | Medium (500), All-caps (0.05em spacing) |

**The Editorial Shift:** Use `display-sm` for patient names or primary health metrics. Do not be afraid of large type; it communicates transparency and confidence.

---

## 4. Elevation & Depth

### Tonal Layering Principle
Avoid the "Shadow-Heavy" look of 2010. Achieve lift by stacking:
*   A `surface-container-lowest` card sitting on a `surface-container-low` background creates a natural, soft lift.

### Ambient Shadows
When a component must "float" (e.g., a vital signs popover):
- **Color:** Use a tinted shadow: `rgba(0, 72, 141, 0.06)` (a 6% opacity version of the Primary Blue).
- **Blur:** `32px` to `64px`. Shadows should feel like ambient light, not a dark drop-shadow.

### The "Ghost Border" Fallback
If accessibility requires a container edge (e.g., high-contrast mode), use a **Ghost Border**: `outline-variant` (#c2c6d4) at **15% opacity**. Never use a 100% opaque border.

---

## 5. Components

### Buttons & Chips
- **Primary Button:** Gradient (`primary` to `primary_container`). `0.5rem` (lg) roundedness. 
- **Action Chips:** Use `secondary_container` (#a1f3d6) with `on_secondary_container` (#18715a) text. The soft green communicates "Health/Proceed" without the aggression of a standard "Success" green.
- **Rounding:** Use `md` (0.375rem) for inputs and `lg` (0.5rem) for buttons. Avoid `full` (pill) shapes unless it is a status indicator.

### Input Fields
- **State:** Default background is `surface_container_highest` (#e0e3e5). 
- **Focus:** Transition background to `surface_container_lowest` (#ffffff) and apply a `2px` ghost border of `primary`.
- **Error:** Use `error_container` (#ffdad6) for the field background to highlight the area without being alarming.

### Cards & Lists (The Divider-Free Rule)
Forbid 1px horizontal dividers.
- **Separation:** Use `spacing-4` (1.4rem) between list items.
- **Alternate:** Use zebra-striping with `surface_container_low` and `surface_container_lowest` to differentiate rows in a patient record.

### Specialized Component: The Vitality Sparkline
For health data, use a simplified line chart. The line should be `secondary` (#0c6b55) with a `4px` stroke and a soft glow effect using an ambient shadow of the same color.

---

## 6. Do’s and Don’ts

### Do
- **Do** use `spacing-16` (5.5rem) for top-level section margins. Breathing room is the ultimate sign of a premium experience.
- **Do** use `tertiary` (#3f4a48) for secondary text (timestamps, metadata). It is softer than pure black and maintains the "Atelier" feel.
- **Do** overlap elements. A patient's profile picture should slightly overlap the header and the content body to break the grid.

### Don't
- **Don't** use standard "Success Green" (#00FF00). Use the `secondary` (#0c6b55) or `secondary_container` (#a1f3d6) tokens to maintain a professional medical tone.
- **Don't** use boxes within boxes with borders. If you have a card inside a section, use color shifts (Tonal Layering) to define them.
- **Don't** use high-contrast black (#000000). Use `on_surface` (#191c1e) for all primary text to reduce eye strain for medical professionals.