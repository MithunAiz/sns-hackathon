from tools.email_search import search_email
from tools.notes_search import search_notes
from tools.csv_search import search_csv
from tools.pdf_search import search_pdf

print("--- Testing email search ---")
print(search_email("catering"))

print("\n--- Testing notes search ---")
print(search_notes("venue"))

print("\n--- Testing csv search ---")
print(search_csv("Guest"))

print("\n--- Testing pdf search ---")
print(search_pdf("shuttle"))
