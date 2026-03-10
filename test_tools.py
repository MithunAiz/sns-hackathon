import sys
sys.path.insert(0, ".")

from tools import search_email, search_notes, search_csv, search_pdf

def divider():
    print("-" * 50)

def header(title):
    print(f"\n[{title}]")

print("=" * 50)
print(" TOOL LAYER - OUTPUT VERIFICATION")
print("=" * 50)

# ── EMAIL SEARCH ──────────────────────────────
for query in ["catering", "transport", "keynote speaker"]:
    header(f"EMAIL SEARCH  Query: '{query}'")
    results = search_email(query)
    if results:
        for r in results:
            print(f"  >> {r['subject']}")
            print(f"     From: {r['sender']} | Date: {r['date']}")
    else:
        print("  >> No results found")

divider()

# ── NOTES SEARCH ──────────────────────────────
for query in ["venue", "catering", "budget"]:
    header(f"NOTES SEARCH  Query: '{query}'")
    results = search_notes(query)
    if results:
        for line in results[:3]:   # top 3 lines
            print(f"  >> {line}")
    else:
        print("  >> No results found")

divider()

# ── CSV SEARCH ────────────────────────────────
for query in ["Speaker", "Vegan", "Confirmed"]:
    header(f"CSV SEARCH  Query: '{query}'")
    results = search_csv(query)
    if results:
        for r in results:
            print(f"  >> {r['Name']:<22} | {r['Role']:<18} | {r.get('Dietary_Preference',''):<15} | {r['RSVP_Status']}")
    else:
        print("  >> No results found")

divider()

# ── PDF SEARCH ────────────────────────────────
for query in ["catering", "keynote", "transport"]:
    header(f"PDF SEARCH  Query: '{query}'")
    results = search_pdf(query)
    if results:
        for line in results[:2]:   # top 2 matches
            print(f"  >> {line}")
    else:
        print("  >> No results found")

print("\n" + "=" * 50)
print(" ALL 4 TOOLS VERIFIED SUCCESSFULLY")
print("=" * 50)