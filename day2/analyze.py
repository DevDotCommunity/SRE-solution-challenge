import json
from datetime import datetime, timedelta

# Load the JSON file
with open('buckets.json') as f:
    data = json.load(f)

buckets = data['buckets']
deletion_queue = []
archive_candidates = []

# Helper function to calculate days since creation
def days_since_creation(created_on):
    created_date = datetime.strptime(created_on, "%Y-%m-%d")
    return (datetime.now() - created_date).days

# Summary of buckets
print("Bucket Summary:")
for bucket in buckets:
    print(f"Name: {bucket['name']}, Region: {bucket['region']}, Size: {bucket['sizeGB']} GB, Versioning: {bucket['versioning']}")

# Identify buckets > 80 GB and unused for 90+ days
print("\nBuckets > 80 GB and unused for 90+ days:")
for bucket in buckets:
    if bucket['sizeGB'] > 80 and days_since_creation(bucket['createdOn']) > 90:
        print(f"  - {bucket['name']} in {bucket['region']} (Size: {bucket['sizeGB']} GB)")

# Generate cost report and prepare deletion/archival queues
cost_report = {}
print("\nCost Report:")
for bucket in buckets:
    region = bucket['region']
    department = bucket['tags'].get('team', 'unknown')
    size = bucket['sizeGB']
    days_unused = days_since_creation(bucket['createdOn'])
    
    # Add cost to the report
    cost_report.setdefault(region, {}).setdefault(department, 0)
    cost_report[region][department] += size * 0.0125  # Assuming $0.0125/GB

    # Recommendations based on size
    if size > 50:
        print(f"  - Recommend cleanup: {bucket['name']} in {region} (Size: {size} GB)")
    if size > 100 and days_unused > 20:
        deletion_queue.append(bucket)
    elif size > 50 and days_unused > 90:
        archive_candidates.append(bucket)

# Print cost report
for region, departments in cost_report.items():
    print(f"Region: {region}")
    for dept, cost in departments.items():
        print(f"  Department: {dept}, Total Cost: ${cost:.2f}")

# Final deletion list
print("\nBuckets to delete:")
for bucket in deletion_queue:
    print(f"  - {bucket['name']} (Region: {bucket['region']}, Size: {bucket['sizeGB']} GB)")

# Archive candidates
print("\nBuckets to archive to Glacier:")
for bucket in archive_candidates:
    print(f"  - {bucket['name']} (Region: {bucket['region']}, Size: {bucket['sizeGB']} GB)")

# Save results to files
with open('deletion_queue.json', 'w') as dq_file:
    json.dump([b['name'] for b in deletion_queue], dq_file, indent=2)

with open('archive_candidates.json', 'w') as ac_file:
    json.dump([b['name'] for b in archive_candidates], ac_file, indent=2)
