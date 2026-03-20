# 🛡️ ParaPay Guard — AI-Powered Parametric Income Insurance for India's Gig Workers

> **Guidewire DEVTrails 2026 | University Hackathon**
> Protecting the backbone of India's digital economy — one delivery at a time.

---

## 📌 Table of Contents

1. [The Problem](#the-problem)
2. [Our Persona: Food Delivery Partners (Zomato / Swiggy)](#our-persona)
3. [Persona-Based Scenarios](#persona-based-scenarios)
4. [Solution Overview](#solution-overview)
5. [Weekly Premium Model](#weekly-premium-model)
6. [Parametric Triggers](#parametric-triggers)
7. [Application Workflow](#application-workflow)
8. [AI/ML Integration Plan](#aiml-integration-plan)
9. [Tech Stack](#tech-stack)
10. [Architecture](#architecture)
11. [Platform Choice: Mobile App](#platform-choice-mobile-app)
12. [Innovation & Differentiators](#innovation--differentiators)
13. [Development Plan (6 Weeks)](#development-plan-6-weeks)
14. [Coverage Scope & Constraints](#coverage-scope--constraints)
15. [Team](#team)

---

## The Problem

India has over **12 million app-based delivery workers**. Food delivery riders on Zomato and Swiggy work 8–12 hours a day, earn ₹600–₹1,200/day, and have **zero financial protection** when external disruptions make it impossible to work.

When a cyclone hits Chennai, when AQI crosses a danger threshold in Delhi, or when a sudden bandh shuts down a city zone — the rider loses income with no recourse. No insurance, no payout, no safety net.

**The real pain:**
- A Zomato rider in Chennai earns ~₹900/day. A 3-day flood wipes out ₹2,700 — more than 20% of monthly income.
- Riders can't afford traditional insurance premiums (monthly, complex, opaque).
- Claim processes are too slow, too technical, and designed for white-collar workers.

ParaPay Guard exists to fix this.

---

## Our Persona

### 🏍️ Food Delivery Partner — Zomato / Swiggy

**Why this persona?**
- Largest gig worker segment in urban India (~5M active riders)
- Fully dependent on real-time outdoor conditions to earn
- Works in every tier-1 and tier-2 city — high disruption exposure (weather, traffic, curfews)
- Already comfortable with mobile-first UX (uses the Zomato/Swiggy partner app daily)
- Earns and spends on a weekly cycle — perfectly aligned with our weekly premium model

**Rider Profile:**
| Attribute | Typical Value |
|---|---|
| Age | 22–35 years |
| Daily earnings | ₹600 – ₹1,200 |
| Working hours | 8–12 hrs/day, 6–7 days/week |
| Weekly income | ₹4,200 – ₹8,400 |
| Phone | Budget Android (₹8k–₹15k range) |
| Tech comfort | High with apps, low with forms |
| Language | Hindi, Tamil, Telugu, Kannada (multilingual need) |

---

## Persona-Based Scenarios

### Scenario 1 — The Monsoon Wipeout 🌧️
> **Ravi**, a Swiggy rider in Bengaluru, woke up to IMD issuing a Red Alert for heavy rainfall. By 10 AM, water-logging closed 3 major roads. He couldn't complete a single delivery. **Lost: ₹900.**

With ParaPay Guard: The system detects the Red Alert via weather API at 6 AM. Ravi's policy activates automatically. By 11 PM, ₹700 is transferred to his UPI without him filing anything.

---

### Scenario 2 — The Smog Shutdown 🌫️
> **Priya**, a Zomato rider in Delhi, couldn't ride when AQI crossed 400+ for 2 consecutive days. Authorities restricted outdoor movement. She lost 2 days of income (~₹1,800).

With ParaPay Guard: AQI sensor data triggers automatic coverage. Her daily coverage cap pays out within 24 hours.

---

### Scenario 3 — The Bandh Day 🚫
> **Arjun** in Hyderabad lost a full Sunday's income (his highest-earning day, ~₹1,400) due to an unannounced political bandh.

With ParaPay Guard: Zone-level social disruption flag (sourced from local news API + government alerts) triggers a payout automatically. No claim required.

---

## Solution Overview

**ParaPay Guard** is a mobile-first, AI-enabled parametric income insurance platform for food delivery workers.

**Core principle:** *No claims. No paperwork. No waiting. Just protection.*

When a pre-defined disruption event triggers, the payout is automatic. The rider doesn't need to do anything — they just receive money in their UPI wallet at the end of the week.

**Key principles:**
- **Parametric:** Payout is based on verified external event data, not self-reported losses
- **Automated:** Zero-touch claim initiation and payout processing
- **Weekly cadence:** Premiums and payouts aligned to the gig worker's income cycle
- **AI-driven:** Premium is calculated dynamically per rider, per zone, per week
- **Fraud-resistant:** No human claim = no fake claims; anomaly detection for edge cases

---

## Weekly Premium Model

### Philosophy
Gig workers don't think in months. They think in weeks. Our entire financial model is structured on a 7-day cycle.

### How It Works

```
Every Monday:
  → Rider pays weekly premium (auto-deducted or manual UPI)
  → Coverage activates for Mon–Sun
  → Triggers monitored in real time all week
  → Any triggered payout accumulates through the week
  → Net payout (if any) sent every Sunday night via UPI
```

### Premium Tiers

| Plan | Weekly Premium | Max Weekly Payout | Coverage Events |
|---|---|---|---|
| **Basic Shield** | ₹25/week | ₹500 | Extreme rain, Red alerts |
| **Standard Shield** | ₹50/week | ₹1,000 | Weather + AQI + Curfews |
| **Max Shield** | ₹80/week | ₹1,800 | All triggers + extended hours |

### Dynamic Pricing (AI-Adjusted)
The base premium is adjusted weekly by our AI model based on:
- **Rider's home zone** — historically flood-prone? Higher base.
- **Season** — monsoon season = elevated risk multiplier
- **City-level disruption forecast** — next week's predicted AQI, weather outlook
- **Rider's earnings history** — higher earners get higher coverage caps proportionally

Example: A rider in Koramangala (Bengaluru) during peak monsoon might pay ₹62/week on a Standard Shield plan instead of ₹50, with the AI factoring in 3x higher historical disruption frequency for that zone.

### Payout Calculation

```
Daily Payout = min(Average Daily Earnings × Coverage %, Daily Cap)
Weekly Payout = Σ(Daily Payouts for triggered days)
```

Where coverage % is pre-defined by the plan tier (50%–80% income replacement).

---

## Parametric Triggers

All triggers are **objective, verifiable, and data-sourced** — no subjective claim assessment.

| # | Trigger | Data Source | Threshold | Impact |
|---|---|---|---|---|
| 1 | **Heavy Rain / Red Alert** | IMD API / OpenWeatherMap | >64.5mm rain in 24hr OR IMD Red Alert | Full day coverage |
| 2 | **Extreme Heat** | OpenWeatherMap | Heat Index > 47°C for >4hrs | Partial day coverage |
| 3 | **Severe Air Pollution** | CPCB AQI API | AQI > 350 (Very Poor / Severe) | Full day coverage |
| 4 | **Flood / Waterlogging** | IMD Flood Alerts + local civic APIs | Official flood advisory issued | Full day coverage |
| 5 | **Curfew / Bandh / Section 144** | Government alert feeds + news APIs | Official notification in rider's zone | Full day coverage |

> **Note:** All triggers are zone-specific — a Red Alert in North Chennai doesn't trigger coverage for a rider operating in South Chennai unless their GPS confirms they work in the affected zone.

---

## Application Workflow

```
┌─────────────────────────────────────────────────────────┐
│                     RIDER JOURNEY                       │
├─────────────────────────────────────────────────────────┤
│  1. ONBOARDING (< 3 minutes)                            │
│     → Mobile number + OTP                               │
│     → Aadhaar-lite verification (last 4 digits)         │
│     → Link delivery platform (Zomato/Swiggy partner ID) │
│     → Select home zone (map picker)                     │
│     → AI generates risk profile → suggests plan         │
│                                                         │
│  2. WEEKLY ACTIVATION                                   │
│     → Every Sunday night: app notification              │
│     → "Your coverage for next week: ₹50"                │
│     → Tap to pay via UPI / auto-deduct consent          │
│     → Policy activates Monday 00:00                     │
│                                                         │
│  3. DISRUPTION MONITORING (Silent, Background)          │
│     → Weather/AQI/Alert APIs polled every 30 min        │
│     → If threshold crossed → claim auto-initiated       │
│     → Rider gets push notification: "Disruption         │
│       detected in your zone. Coverage active."          │
│                                                         │
│  4. WEEKLY PAYOUT                                       │
│     → Every Sunday 9 PM: system calculates week total   │
│     → Fraud check runs (anomaly detection)              │
│     → UPI transfer initiated automatically              │
│     → Rider gets: "₹750 credited to your UPI 🎉"       │ 
│                                                         │
│  5. DASHBOARD (Always Visible)                          │
│     → "You've saved ₹3,200 this month with ParaPay Guard"   │
│     → Weekly coverage history                           │
│     → Active disruptions near you                       │
│     → Streak bonuses (loyalty rewards)                  │
└─────────────────────────────────────────────────────────┘
```

---

## AI/ML Integration Plan

### 1. Dynamic Premium Calculation (Risk Pricing Engine)

**Model:** Gradient Boosted Trees (XGBoost) + rules-based override layer

**Features fed into model:**
- Rider's operating zone (lat/long cluster)
- Historical disruption frequency for that zone (last 12 months)
- Seasonal risk index (monsoon, summer, winter)
- 7-day weather forecast for rider's city
- City-level AQI trend
- Rider's earnings tier (derived from platform data or self-declared)

**Output:** Personalized weekly premium with coverage cap

**Training data:** Historical IMD weather events, CPCB AQI data, historical claim data (simulated for MVP, real post-launch)

---

### 2. Fraud Detection (Anomaly Detection Layer)

Even though ParaPay Guard is parametric (no self-reported claims), fraud vectors still exist:

| Fraud Vector | Detection Method |
|---|---|
| GPS spoofing (rider claims to be in disrupted zone but isn't) | GPS trail validation against delivery app activity log |
| Multiple accounts for same rider | Phone + Aadhaar hash deduplication |
| Colluding with delivery platform to fake low-activity days | Cross-reference platform order completion rate vs disruption flag |
| Zone boundary gaming (rider artificially moves to disrupted zone) | Historical zone assignment vs claimed zone at trigger time |

**Model:** Isolation Forest for anomaly detection on payout requests
**Rule Engine:** Hard rules for obvious fraud (e.g., same device, 3 different accounts)

---

### 3. Predictive Risk Alerts (Proactive UX)

Before a disruption hits, ParaPay Guard warns riders so they can make informed decisions.

- "High rain probability tomorrow in your zone. Your coverage is active."
- "Next week looks stormy — consider upgrading to Max Shield."

**Model:** Time-series weather forecasting using publicly available IMD data + OpenWeatherMap 7-day forecast API

---

### 4. Earnings Estimation (For New Riders Without History)

Cold-start problem: new riders have no earnings data to calibrate coverage caps.

**Solution:** Cluster-based estimation — new riders in the same zone + platform + city-tier are assigned the median coverage of similar riders in that cluster. Updated after 4 weeks of activity.

---

## Tech Stack

### Mobile App (Primary Interface)
| Layer | Technology | Reason |
|---|---|---|
| Framework | React Native (Expo) | Cross-platform iOS + Android, fast iteration |
| State Management | Zustand | Lightweight, minimal boilerplate |
| UI Components | NativeBase + custom components | Accessible, mobile-optimized |
| Animations | React Native Reanimated | Smooth micro-interactions for UX |
| Languages | English + Hindi (i18n via i18next) | Accessibility for non-English riders |

### Backend / API
| Layer | Technology | Reason |
|---|---|---|
| Runtime | Node.js + Express | Fast REST API development |
| Database | PostgreSQL (Supabase) | Relational data for policies, payouts, riders |
| Cache / Queue | Redis | Fast trigger event processing |
| Auth | Firebase Auth (OTP) | Phone-number OTP — no password needed |
| Background Jobs | Bull (Node.js queue) | Scheduled weekly premium deductions, payout processing |

### AI/ML
| Component | Technology |
|---|---|
| Premium model | Python + XGBoost (served via FastAPI microservice) |
| Fraud detection | Scikit-learn Isolation Forest |
| Weather forecasting | Pre-trained time-series model on IMD historical data |
| Serving | FastAPI on Railway/Render (free tier) |

### External APIs
| API | Purpose | Type |
|---|---|---|
| OpenWeatherMap | Real-time weather + forecasts | Free tier (real) |
| IMD Open Data | Red alerts, flood warnings | Public / mock |
| CPCB AQI API | Real-time air quality | Public (real) |
| Razorpay Test Mode | Premium collection simulation | Sandbox |
| UPI Mock (Razorpay) | Payout simulation | Sandbox |
| Mapbox / Google Maps | Zone mapping, GPS validation | Free tier |

### Infrastructure
| Component | Tool |
|---|---|
| Hosting | Railway (backend) + Expo EAS (mobile) |
| CI/CD | GitHub Actions |
| Monitoring | Sentry (error tracking) |
| Analytics | Mixpanel (free tier) |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        MOBILE APP                            │
│           (React Native — Rider & Admin views)               │
└─────────────────────┬────────────────────────────────────────┘
                      │ REST API
┌─────────────────────▼────────────────────────────────────────┐
│                    API GATEWAY (Express)                     │
│   /auth  /policy  /triggers  /payouts  /dashboard            │
└──────┬─────────────┬──────────────────────┬──────────────────┘
       │             │                      │
┌──────▼──────┐ ┌────▼──────────┐  ┌───────▼────────────────────┐
│  PostgreSQL │ │  Redis Queue  │  │   AI Microservice (FastAPI)│
│  (Supabase) │ │  (Triggers +  │  │   - Premium Calculator     │
│  Riders,    │ │   Payouts)    │  │   - Fraud Detector         │
│  Policies,  │ └────┬──────────┘  │   - Risk Profiler          │
│  Claims,    │      │             └────────────────────────────┘
│  Payouts    │ ┌────▼──────────┐
└─────────────┘ │ External APIs │
                │ OpenWeatherMap│
                │ IMD / CPCB    │
                │ Razorpay Mock │
                └───────────────┘
```

---

## Platform Choice: Mobile App

**We chose Mobile (React Native) over Web. Here's why:**

1. **Riders are always on their phone** — they use Zomato/Swiggy partner apps all day. A mobile-native experience fits naturally into their existing workflow.

2. **UPI integration is mobile-native** — India's payment infrastructure is phone-first. Seamless UPI payout via mobile is significantly better UX than a browser flow.

3. **Push notifications are critical** — riders need real-time alerts when a disruption is detected in their zone. Push notifications on mobile are far more reliable and immediate than browser notifications.

4. **GPS access** — fraud detection requires GPS validation. Mobile apps provide native, reliable location access.

5. **Offline resilience** — riders in low-connectivity areas can still view their policy status, cached history, and payout records even without internet.

6. **Accessibility** — a mobile app can be built with vernacular language support, larger fonts, and voice-readable labels — essential for a non-technical audience.

> We will also build a lightweight **Admin Web Dashboard** (React) for the insurer side — loss ratios, disruption analytics, and payout management. But the primary rider interface is mobile.

---

## Innovation & Differentiators

### 🚀 Beyond the Brief: What Makes ParaPay Guard Different

**1. Zero-Claim Insurance**
No other insurance product in India is truly zero-touch for this segment. The moment a parametric trigger fires, the system processes coverage autonomously. The rider never opens the app to "file a claim."

**2. GigScore — Loyalty & Trust Engine**
Riders who maintain continuous weekly coverage build a "GigScore." Higher scores unlock:
- Reduced premiums (up to 20% off after 12 consecutive weeks)
- Higher payout caps
- Priority processing during mass disruption events

This reduces churn and rewards loyalty — solving the biggest problem in microinsurance: lapse rates.

**3. Disruption Forecast Widget**
A home-screen widget (Android) showing next 48-hour risk level for the rider's zone. Color-coded: 🟢 Safe / 🟡 Watch / 🔴 High Risk. Helps riders make daily decisions (should I go out early today?).

**4. Hyperlocal Zone Intelligence**
Most weather APIs operate at city level. We map disruptions at the **zone/ward level** using polygon-based geo-fencing. A flood in one part of Chennai shouldn't trigger payouts for riders in a dry zone — and vice versa.

**5. Platform-Agnostic Onboarding**
Riders from Zomato, Swiggy, Zepto, Amazon, Dunzo can all onboard. The platform affiliation is optional context for better earnings calibration — not a gating factor.

**6. Rainy Day Fund Mode**
Riders can optionally roll over small payouts (< ₹200) into a ParaPay Guard Rainy Day Fund instead of immediate transfer. Accumulated over months, this creates an emergency buffer — teaching financial discipline alongside protection.

---

## Development Plan (6 Weeks)

### Phase 1: Ideation & Foundation (March 4–20)
**Theme: "Know Your Rider"**

- [x] Problem research: rider interviews (simulated personas), market sizing
- [x] Persona finalization: Food delivery (Zomato/Swiggy)
- [x] Weekly premium model design
- [x] Parametric trigger framework
- [x] Tech stack selection & repo setup
- [ ] Wireframes for mobile app (Figma)
- [ ] Basic React Native project scaffolding
- [ ] FastAPI skeleton for AI service
- [ ] README finalized ← *you are here*

**Deliverable:** This README + 2-min strategy video + GitHub repo

---

### Phase 2: Core MVP (March 21–April 4)
**Theme: "Protect Your Worker"**

- [ ] Rider onboarding flow (OTP, zone selection, plan selection)
- [ ] Policy creation & management module
- [ ] Weekly premium calculation (static + AI-dynamic hybrid)
- [ ] OpenWeatherMap + CPCB AQI integration (real APIs)
- [ ] 3–5 parametric triggers wired to backend
- [ ] Auto-claim initiation on trigger detection
- [ ] Mock UPI payout simulation (Razorpay test mode)
- [ ] Basic rider dashboard (earnings protected, active policy)

**Deliverable:** Executable code + 2-min demo video

---

### Phase 3: Advanced Features (April 5–17)
**Theme: "Perfect for Your Worker"**

- [ ] Fraud detection layer (GPS validation, Isolation Forest, deduplication)
- [ ] Full AI premium model (XGBoost trained on synthetic + historical data)
- [ ] GigScore loyalty engine
- [ ] Admin insurer dashboard (loss ratios, disruption heatmap, payout analytics)
- [ ] Hyperlocal zone-level trigger mapping
- [ ] Disruption forecast widget
- [ ] Razorpay sandbox full integration (instant payout simulation)
- [ ] Multilingual support (Hindi + English)
- [ ] Performance testing + bug fixes

**Deliverable:** Full platform + 5-min demo video + Final pitch deck (PDF)

---

## Coverage Scope & Constraints

### ✅ Covered
- Income lost due to **extreme weather** (heavy rain, floods, extreme heat)
- Income lost due to **severe air pollution** (AQI > 350)
- Income lost due to **curfews, bandhs, zone closures** (social disruptions)
- **Weekly income replacement** up to plan cap

### ❌ Strictly Excluded (as per contest rules)
- Health insurance
- Life insurance
- Accident coverage
- Vehicle repair costs
- Any physical damage claims
- Any self-reported claims (all triggers must be objective + data-verified)

---

## Team

> *Add your team members here*

| Name | Role |
|---|---|
| Aryan Singh | Full Stack Lead |
| Rishit Srivastava | Backend Developer |
| Harmandeep Singh | Mobile Developer |
| Dhyey Shah | AI/ML Engineer |
| Stuti Kashyap | UI/UX + Product |

---

## Repository Structure

```
ParaPay Guard/
├── mobile/              # React Native app (Expo)
│   ├── src/
│   │   ├── screens/     # Onboarding, Dashboard, Policy, Payouts
│   │   ├── components/  # Reusable UI components
│   │   ├── services/    # API calls, auth, notifications
│   │   └── store/       # Zustand state management
├── backend/             # Node.js + Express API
│   ├── routes/          # auth, policy, triggers, payouts
│   ├── jobs/            # Bull queues (trigger monitor, payout processor)
│   └── db/              # Supabase schema + migrations
├── ai-service/          # Python FastAPI
│   ├── models/          # XGBoost premium model, Isolation Forest
│   ├── training/        # Training scripts + datasets
│   └── api/             # Endpoints: /price, /fraud-check, /risk-profile
├── admin-dashboard/     # React web app (insurer view)
└── docs/                # Architecture diagrams, API docs
```

---

> **ParaPay Guard** — Because every delivery matters, and every rider deserves a safety net.

*Built for Guidewire DEVTrails 2026 | Team thugLife.js*
