# Privacy Guardrails: User Data Protection & Compliance

## Core Principle

User data is personal and sensitive. The graphic should never collect, retain, or analyze user data without explicit opt-in and clear explanation of what data is used for.

## Privacy by Design

### Heatmaps: Client-Side Only

**Data:** Champion positioning over time (derived from replays)

**Flow:**
1. Player enables "Positioning Heatmap" feature (opt-in)
2. Client fetches replay file from local cache
3. Client runs CV heatmap analysis locally (no network transmission)
4. Result (heatmap image, metrics) stays on player's device
5. No data sent to servers unless player explicitly shares the graphic

**Guarantees:**
- Riot's servers never see raw heatmap data
- No training on player data without consent
- Player can delete heatmaps anytime (delete button in UI)

### Match Analytics: Aggregated Only

**Data:** Kills, deaths, gold, CS, etc. (public match data via API)

**Flow:**
1. Fetch match data from official Riot API
2. Compute metrics locally
3. Metrics displayed to player
4. Send **only aggregated statistics** to cloud for percentile rankings (OPTIONAL cloud sync)

**Guarantees:**
- Individual match details never stored on servers
- Cloud storage is aggregated (50+ games per bucket minimum)
- Player names and IDs are hashed one-way
- No reverse-identification possible

### Pro Play Comparisons: Anonymized

**Data:** "Your game mirrors Faker's Ahri game"

**Flow:**
1. Your match stats (anonymized) are compared to pro-play database
2. Matches found in database display pro player's name + context
3. No data about you is sent to pro players or broadcasters

**Guarantees:**
- Pro players don't know they were used for comparison
- You don't see other players' individual stats (only aggregates)
- All comparisons are read-only (no data exchange)

## Data Retention Policy

### Match Graphics

**What:** Generated graphic (images, metrics, narrative text)

**Retention:**
- Stored locally on player's device: Indefinite (until deleted by player)
- Cloud backup (optional): 30 days
- Auto-delete: Never (unless player requests)

**Deletion:**
- Player can delete any graphic via "Delete" button in UI
- Requesting deletion removes all associated data within 24 hours
- Bulk deletion: "Delete all graphics older than 30 days" option

### Aggregated Analytics

**What:** Rolled-up stats (average KP%, damage share%, etc.)

**Retention:**
- Current season: Granular (updated daily)
- Previous season: Monthly aggregates only
- Older than 2 years: Deleted

**Use:** Percentile rankings, role-normalization benchmarks

### Processing Logs

**What:** System logs (errors, performance metrics, etc.)

**Retention:** 30 days  
**Content:** No player data; only system diagnostics  
**Access:** Engineering team only (for troubleshooting)

## Opt-In Features

### Feature: Cloud Sync Graphics

**What:** Backup graphics to cloud; access from any device

**Opt-In Flow:**
1. User clicks "Enable Cloud Backup"
2. Dialog explains: "Graphics will be stored on Riot's servers for 30 days"
3. User confirms understanding and consents
4. Graphics synced to cloud

**Data Minimization:** Only graphic images and metadata (not raw stats)

**User Controls:**
- Toggle cloud sync on/off anytime
- Auto-delete cloud graphics after 30 days
- Manual delete button for each graphic

### Feature: Competitive Benchmark

**What:** Compare your stats to ranked players in your tier

**Opt-In Flow:**
1. User clicks "Enable Competitive Benchmark"
2. Dialog explains: "Your aggregated stats will be included in percentile rankings"
3. Confirmation: "This is anonymized; you won't be identified"
4. User consents

**Data Sent:** Only aggregate stats (average KP, CS, etc.), no identifying info

**User Controls:**
- Opt-out anytime; previous data removed within 24 hours
- "Keep me anonymous" checkbox (defaults to ON)

### Feature: Pro Play Comparisons

**What:** Enable "Shadow Match" comparisons

**Opt-In Flow:**
1. User clicks "Enable Pro Comparisons"
2. Dialog explains: "Your match will be compared to professional games"
3. Confirmation: "Pro players won't see your stats"
4. User consents

**Data Minimization:** Only comparison results shown to user (no raw data retention)

## GDPR & Regional Compliance

### GDPR (EU Users)

**User Rights:**

| Right | Implementation |
|-------|-----------------|
| Right to Access | User can download all graphics and data (ZIP export) |
| Right to Deletion | "Delete All Data" button removes everything within 24 hours |
| Right to Portability | Export graphics as PDF, CSV (for percentiles) |
| Right to Rectification | User can update profile info (summoner name, tier) |
| Right to Object | Opt-out of analytics; previous data removed |

**Data Processing:**
- Legitimate interest: Improving user experience
- Consent-based: Cloud features, benchmarks
- Legal obligation: Match outcome (sport integrity)

**Data Processor:** Riot Games (legitimate processor under DPA)

### CCPA (California Users)

**User Rights:**

| Right | Implementation |
|-------|-----------------|
| Right to Know | Privacy policy available in-client |
| Right to Delete | Delete account data anytime |
| Right to Opt-Out of Sale | Graphics/data never sold; opt-out of analytics |
| Right to Non-Discrimination | Deleting data doesn't affect service quality |

**Applicable:** If user is California resident (auto-detected by IP)

### Other Regions

**Default:** Apply GDPR-equivalent standards globally (most restrictive)

**Regional Customization:** 
- China: Comply with local data laws (server in-region)
- Russia: Respect data localization requirements
- Brazil: LGPD compliance (similar to GDPR)

## Security Measures

**Data in Transit:**
- All API calls over HTTPS (TLS 1.3+)
- Replay file processing: Local-only (zero network exposure)

**Data at Rest:**
- Cloud data encrypted with AES-256
- Database access restricted to backend services (no direct human access)
- Regular security audits (quarterly)

**Access Control:**
- Graphics accessible only by authenticated user
- Engineering team has read-only access to logs (for debugging)
- No "master access" keys for individual user data

**Incident Response:**
- Data breach: Notify affected users within 72 hours
- Investigation: Internal + independent security firm
- Remediation: Patch + user notification + compensation (if applicable)

## Transparency & Communication

### In-App Privacy Notices

**Header Notice (Graphic Generation):**
"Processing your match data. This includes optional CV analysis of replay files (client-side only)."

**Footer:** Link to full privacy policy + settings (where user can manage data)

### Privacy Settings Menu

**User Controls:**
```
Privacy & Data
├─ Cloud Backup ............................ [TOGGLE ON/OFF]
├─ Competitive Benchmark .................. [TOGGLE ON/OFF]
├─ Pro Comparisons ........................ [TOGGLE ON/OFF]
├─ Analytics & Logs ....................... [TOGGLE ON/OFF]
├─ Delete All Data ........................ [BUTTON - DELETE]
├─ Download My Data ....................... [BUTTON - EXPORT ZIP]
└─ Privacy Policy ......................... [LINK]
```

### Annual Privacy Report

**Transparency:** Publish annually:
- Data stored (aggregate counts, not individual data)
- Access requests received (anonymized)
- Security incidents (if any)
- Regulatory compliance summary

## Boundaries

**Assumes from All Packages:**
- No package transmits user data without user consent
- All metrics are computed locally or from public APIs

**Provides to All Packages:**
- Clear opt-in/opt-out mechanisms
- Data retention policies
- Security guarantees
- Compliance certifications
