# MedQueue — UI Design Spec

Reference document for building the MedQueue hospital/clinic management system.
Re-upload this file in any new conversation so Claude can follow the same design consistently.

---

## 1. Product Overview

MedQueue is a healthcare management SaaS platform for hospitals, clinics, and pharmacies. It has:
- A **public marketing site** (homepage)
- A **multi-role login** (Patient / Doctor / Admin)
- An **internal admin/clinical dashboard** with modules for Patients, Doctors, Appointments, Billing, Pharmacy, Laboratory, Inventory, and Reports

---

## 2. Brand & Visual Identity

- **Logo/name:** MedQueue, with a small rounded-square icon (pulse/heartbeat waveform) in blue
- **Tagline style:** "Precision Healthcare for Everyone" / "Precision Healthcare Management for Modern Facilities"

### Color Palette
| Role | Color | Notes |
|---|---|---|
| Primary | Deep royal blue (`#1E3A8A`–`#2547D0` range) | Buttons, active nav states, headers |
| Accent / Dark navy | Near-black navy (`#0B1B36` range) | Login left panel, sidebar background |
| Success / Green | Emerald green | Doctor stats, positive metrics, "Active" badges |
| Purple | Used for Appointments-related stat icons |
| Amber/Orange | Used for revenue/money stat icons |
| Background | Very light gray-blue (`#F5F7FA` range) | Page backgrounds |
| Card background | White | All cards/panels |
| Text primary | Near-black slate | Headings |
| Text secondary | Mid gray | Subtext, captions |

### Typography
- Clean sans-serif (system UI / Inter-like)
- Bold, large headings (dashboard titles, hero text)
- Regular weight for body/secondary text
- Numbers in stat cards are large and bold for emphasis

---

## 3. Layout Patterns

### Marketing Homepage
- Top nav bar: logo left, links (Solutions, Pricing, Resources, Company) center, Login + "Request Demo" CTA button right
- Hero section: large heading, subheading, two CTAs (primary filled + secondary outline), hero product screenshot mockup
- Stats row (3 columns): big number + label (e.g., "120k+ Active Patients")
- Logo/trust bar for partner institutions
- Feature grid: dark large feature card + smaller light feature cards
- "Tailored Solutions" 3-column card section (Hospitals / Clinics / Pharmacies), each with icon, bullet checklist, CTA button
- Bottom CTA banner: dark blue background, centered heading + two buttons
- Footer: 4-column layout (brand blurb, Product, Resources, Contact) + legal line

### Login Page
- Split-screen layout:
  - **Left panel:** dark navy background, logo top-left, large heading + subheading, 4-stat grid (2x2), copyright footer
  - **Right panel:** light gray background, centered white card with:
    - "Welcome Back" heading + subtext
    - Role selector tabs (Patient / Doctor / Admin) as a segmented control
    - Email/ID field, Password field (with "Forgot Password?" link)
    - "Remember me" checkbox
    - Full-width primary blue submit button
    - Footer links: Support / Terms / Privacy
- Floating help button (bottom-right circular "?" icon)

### Internal App Shell (Dashboard, Patients, Doctors, Appointments, Billing, Pharmacy, Laboratory, Inventory, Reports)
- **Fixed left sidebar** (dark navy):
  - Logo/brand at top
  - Vertical nav list with icon + label; active item highlighted with blue pill background
  - Nav items: Dashboard, Patients, Doctors, Appointments, Billing, Pharmacy, Laboratory, Inventory, Reports
  - User profile block pinned at bottom (avatar, name, role) + Collapse toggle
- **Top header bar** (white): breadcrumb (Module > Page), global search field, notification bell (with red dot badge), action buttons (context-specific, e.g. Screenshot/Export), Sign Out
- **Page body** (light gray-blue background):
  - Page title + short welcome/description line
  - Row of **stat cards** (icon in colored rounded square, label, big number, % change vs. last period with up/down arrow color-coded green/red)
  - Content panels below in a card grid: charts (line/area trend charts, donut charts), tables/lists (e.g., recent activity, audit log, patient list, inventory list)
  - Tables use white rows on white card background with light dividers, status badges (colored pill labels e.g. "Active", "Pending", "Low Stock")
  - Footer bar at the very bottom with legal/compliance links

---

## 4. Reusable Components to Build

- `Sidebar` — collapsible, icon+label nav, active-state highlight, user footer block
- `TopHeader` — breadcrumb, search bar, notifications, action buttons
- `StatCard` — icon, label, big number, trend indicator
- `ChartCard` — wraps line/area/donut charts with a title + time-range filter
- `DataTable` — sortable table with status badges, pagination
- `StatusBadge` — colored pill (green=active/success, amber=warning/pending, red=critical/low stock, blue=info)
- `RoleTabs` — segmented control used on login (Patient/Doctor/Admin)
- `AuthCard` — centered white card used for login/forms
- `PrimaryButton` / `SecondaryButton` — filled blue vs. outlined
- `MarketingHero`, `FeatureCard`, `PricingCTA` — for the public site

---

## 5. Module Notes (from mockups)

- **Dashboard:** Admin overview — total patients, active doctors, today's appointments, monthly revenue; daily appointment trend chart; revenue-by-clinic donut; recent system audit log table
- **Patients:** Patient list/records module, CRUD-style record management implied by homepage copy ("Unified EMR/EHR system with secure, HIPAA-compliant data storage")
- **Doctors:** Doctor directory/management, specialties, status
- **Appointments:** Scheduling view, booking status tracking
- **Billing:** Invoices/payments, revenue tracking
- **Pharmacy:** Automated stock tracking, reordering, prescription fulfillment workflows
- **Laboratory:** Digital results delivery, trend analysis, diagnostic decision support
- **Inventory:** Stock levels, low-stock alerts
- **Reports:** Aggregated analytics/export module

---

## 6. Tone & Compliance Cues

- Copy emphasizes: enterprise-grade, HIPAA-compliant, precision, efficiency, security
- Footer/legal links consistently include: Privacy, Terms, Compliance, Emergency Contact (internal app) / Privacy Policy, Terms of Service, HIPAA Compliance, Security (marketing site)

---

*This spec was generated from the original `UI.zip` mockups (login page, homepage, Dashboard, Patient, Doctor, appointments, billings, pharmacy, Laboratory, Inventory, reports). Keep this file updated if the design evolves.*
