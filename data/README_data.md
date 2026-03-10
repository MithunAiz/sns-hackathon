# Data Layer — README

## Purpose

This folder contains **simulated datasets** that represent the fragmented information sources
a personal executive agent must navigate. Each file models a real-world information channel
(email, meeting minutes, guest spreadsheet, event document) for an event planning scenario.

The data is designed to be queried by the tools in the `tools/` layer, which are in turn
called by an AI agent to answer natural language questions like:
- *"What catering vendor did we choose?"*
- *"Who is the keynote speaker?"*
- *"How many guests are confirmed?"*

---

## Files

### `emails.json`
**Format:** JSON array of email objects

**Fields per email:**
| Field | Description |
|-------|-------------|
| `id` | Unique identifier (e.g., `email_001`) |
| `subject` | Email subject line |
| `sender` | Sender email address |
| `to` | Recipient(s) |
| `date` | Date sent (YYYY-MM-DD) |
| `body` | Full email body text |

**Content covers:**
- Catering vendor finalization (GreenLeaf Catering)
- Transport and shuttle arrangements
- Keynote speaker confirmation (Dr. Ananya Krishnan)
- Marketing and promotional campaign
- Venue walkthrough findings

---

### `meeting_notes.txt`
**Format:** Plain text, structured with section headers

**Content covers:**
- Venue confirmation (City Convention Hall)
- Catering vendor selection rationale
- Expected guest count (200) and registration targets
- Logistics responsibilities (transport, setup, emergency)
- Marketing strategy and sponsor details
- Full budget breakdown ($25,000 total)

**Structure:** Each agenda item is separated by a dashed divider with
DECISION, ACTION ITEM, and detail sub-sections.

---

### `guests.csv`
**Format:** CSV with header row

**Columns:**
| Column | Description |
|--------|-------------|
| `Name` | Full name of attendee |
| `Role` | Role at the event (Speaker, Panelist, VIP Guest, etc.) |
| `Organization` | Affiliated organization |
| `Email` | Contact email |
| `RSVP_Status` | Confirmed / Pending / Declined |
| `Dietary_Preference` | Vegetarian / Vegan / Non-Vegetarian |

**Includes:** 10 attendees across speakers, panelists, sponsors, VIPs, and general attendees.

---

### `event_plan.pdf`
**Format:** PDF document (binary — not included in repo)

**Expected content:**
- Official event title and date
- Venue: City Convention Hall, March 15, 2026
- Catering vendor: GreenLeaf Catering
- Guest count: 200 expected
- Transport: Shuttle from Central Metro Station
- Keynote speaker: Dr. Ananya Krishnan
- Schedule overview (9:00 AM – 5:00 PM)
- Sponsor acknowledgements
- Emergency contacts

> **Note:** To generate this file, use any PDF creation tool (e.g., `fpdf2`, `reportlab`,
> or export from a Word/Google Doc). The `pdf_search.py` tool uses `pypdf` to extract
> and search its text content at runtime.

---

## Usage

These files are consumed exclusively by the `tools/` layer. Do not modify the file paths
without updating the corresponding tool functions.
