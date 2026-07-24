# Self-Hosting Journey: Portfolio + GreatEFB Data Server

## The Problem

Wanted to host a portfolio website privately — shareable with friends, family, and approved employers, but not publicly indexed. Required password protection without buying a domain or dealing with complex setup.

## Services Explored & Lessons Learned

### Cloudflare Pages + Access/Workers
**Summary:** Attractive UI, but walls everywhere.

**What went wrong:**
- Pages deployed successfully (free tier works great for static sites)
- Access (password protection) requires credit card even for free tier
- Password protection only works with custom domains, not free `*.pages.dev` subdomain
- Worker password-protection had same domain limitation
- Account deletion UI intentionally obscured — required payment method on file to delete Teams Free product
- GitHub authorization persisted even after project deletion

**Cost:** Credit card required, frustration unlimited

**Lesson:** Cloudflare optimizes for enterprise customers. Free tier has hidden paywalls and UX is deliberately hostile to leaving.

### Netlify
**Summary:** Simpler than Cloudflare, but same paywall on password protection.

**What went wrong:**
- Free tier does NOT include password protection (claimed otherwise)
- Basic password protection requires Pro plan (~$19/month)
- No credit card required for free tier (good), but defeats purpose

**Lesson:** Read the fine print. "No domain needed" doesn't mean "free password protection."

### GitHub Pages
**Summary:** Pure static hosting, no auth options.

**What works:**
- Free, reliable, simple
- Public by default
- Can make repo private and invite collaborators, but they need GitHub accounts

**Lesson:** GitHub Pages is for public content or sharing with other developers. Not suitable for password-protected portfolios.

### The Pattern
Every mainstream service either:
1. Required buying a domain
2. Charged for password protection
3. Had confusing UX and hostile account management
4. Made leaving the platform deliberately hard

---

## The Solution: Self-Hosting on Raspberry Pi

After exploring $0-$20/month hosting options, decided to buy hardware instead (~$75 one-time) and self-host.

### Hardware

**Recommended Setup:**
- **Raspberry Pi 4 Model B** (~$60-75)
  - Fast enough for data processing + serving
  - 2GB RAM is adequate for Nginx + Python scripts
  - Widely available, good community support

**Alternative (Budget):**
- **Raspberry Pi Zero 2 W** (~$15-20)
  - Smaller, lower power draw
  - Adequate for serving (not processing) but slower

**Storage:**
- **64GB microSD card** (~$12)
  - Holds portfolio (347KB) + GreatEFB data (up to 10GB worst-case)
  - Can add USB external drive for larger datasets

**Total Hardware Cost:** ~$75-90 (one-time)  
**Operating Cost:** ~$5-10/year electricity  
**Hosting Cost:** $0

### Software Stack

- **Nginx** (~3MB) — lightweight, fast web server
- **Python** — existing data processing scripts already written
- **Cron** — automate data pipeline runs every 28 days
- **SQLite** — lightweight database for subscriptions (future use)
- **Let's Encrypt** — free HTTPS certificates

### Architecture

```
┌─────────────────────────────────────────────┐
│        Raspberry Pi 4 (64GB microSD)         │
├─────────────────────────────────────────────┤
│                                              │
│  Nginx (reverse proxy + static file server)  │
│  ├─ Serves portfolio (347KB)                │
│  └─ Serves GreatEFB data (10GB)             │
│                                              │
│  Python environment                          │
│  ├─ FAA data downloader                     │
│  ├─ Chart Generator (GDAL)                  │
│  ├─ Elevation Baker                        │
│  ├─ Airspace Builder                       │
│  └─ AIS Builder                            │
│                                              │
│  Cron scheduler                              │
│  └─ Monthly data pipeline (28-day cycle)    │
│                                              │
│  Registration/subscription API (future)      │
│  ├─ Key validation                          │
│  └─ SQLite subscription database            │
│                                              │
└─────────────────────────────────────────────┘
         ↕ (100 Mbps home internet)
┌─────────────────────────────────────────────┐
│           Domain + DNS                       │
│  (optional, ~$15/year for permanent URL)    │
└─────────────────────────────────────────────┘
```

### Access Methods

**Local Network:**
- Share Pi's IP address (192.168.x.x) with people on your WiFi
- No authentication needed for local network

**External Access (Private):**
- **ngrok** (free) — temporary public URL, simple
  - Downside: URL changes, temporary
- **Port forwarding** + dynamic DNS — permanent setup
- **Custom domain** (~$15/year) + port forwarding — most professional

**External Access (Public):**
- Buy domain (~$15/year)
- Point to Pi's public IP or use CNAME
- Serve publicly or add HTTP Basic Auth

### Bandwidth

At 100 Mbps home internet:
- 10GB download: ~13 minutes
- 2GB monthly update: ~2.5 minutes transfer time
- Easily handles 28-day update cycle

---

## GreatEFB Data Distribution

### Current State

**Data folder size:** 4.1GB (working files)
- Charts: 3.2GB
- Airspace data: 437MB
- Elevation tiles: 322MB
- AIS data: 109MB
- FAA NASR files: 33MB

**Estimated worst-case download:** ~10GB (full CONUS + all categories)

### Autonomous Pipeline

Monthly cron job:
1. Download new FAA data (28-day NASR cycle)
2. Run Python processing pipeline (Chart Generator, Airspace Builder, Elevation Baker, AIS Builder)
3. Generate MBTiles and elevation tiles
4. Replace old data in serving directory
5. Nginx serves fresh data to users

**No manual intervention needed.**

---

## Future Possibilities

### Subscription/Registration Keys

Pi can handle registration key validation:
- Use Stripe/Lemonsqueezy for payment processing
- Pi backend validates keys via simple Python API
- SQLite stores active subscriptions
- App queries: `Is ABC123 valid?` → Pi responds yes/no

**Setup:** 1-2 days of work, no additional infrastructure cost

### Redundancy & High Availability

Multiple Pis for backup:
- **Option 1:** DNS round-robin (3 Pis, requests spread, auto-failover)
- **Option 2:** Primary + standby (1 active, 1-2 backups sync data nightly)
- **Option 3:** Shared database (multiple Pis read from central store)

**Cost for 3-Pi setup:** ~$225 hardware + $15-20/year electricity

---

## Lessons Learned

1. **Cloud hosting has hidden costs** — Free tiers almost always have paywalls for useful features
2. **Small hardware is cheap now** — A Pi costs less than a year of mid-tier hosting
3. **Self-hosting is simple for static content** — Nginx + Python handles portfolio + data distribution easily
4. **Redundancy is affordable** — Multiple Pis for backup costs less than annual SaaS subscription
5. **Avoid Cloudflare** — Confusing UI, hostile account management, broken deletion flow

---

## Next Steps

1. Order Raspberry Pi 4 + 64GB microSD
2. Install Raspberry Pi OS + Nginx + Python environment
3. Deploy portfolio files to Pi
4. Test serving locally
5. Buy domain (~$15/year) or use ngrok for sharing
6. Set up cron job for monthly GreatEFB data pipeline
7. Share Pi URL with friends/family/employers

---

## References

- **Raspberry Pi:** https://www.raspberrypi.com/
- **Nginx:** https://nginx.org/
- **Let's Encrypt:** https://letsencrypt.org/ (free HTTPS)
- **ngrok:** https://ngrok.com/ (free tunneling)
- **Dynamic DNS:** https://www.noip.com/ (free dynamic DNS)
- **Stripe:** https://stripe.com/ (payment processing)
- **Lemonsqueezy:** https://www.lemonsqueezy.com/ (SaaS licensing)

---

**Date:** July 24, 2026  
**Portfolio Size:** 347 KB  
**GreatEFB Data (worst-case):** 10 GB  
**Total Cost:** ~$75-90 (hardware) + $15/year (domain) + $5-10/year (electricity)
