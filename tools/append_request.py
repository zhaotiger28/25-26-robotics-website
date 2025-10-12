"""
from the contact.html thing add the thing to the thing
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / 'logs' / 'requests.csv'

if len(sys.argv) < 4:
    print('Usage: python tools/append_request.py "Name" "Subject" "Message"')
    sys.exit(1)

name = sys.argv[1]
subject = sys.argv[2]
message = sys.argv[3]

with LOG.open('a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    from datetime import datetime
    writer.writerow([datetime.utcnow().isoformat(), name, subject, message])

print('Appended to', LOG)
