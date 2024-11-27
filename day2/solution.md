# S3 Bucket Analysis and Cost Management Script

## Overview
This script analyzes AWS S3 buckets to manage costs, identify candidates for deletion or archival, and generate cost reports. It processes bucket information from a JSON file and makes recommendations based on size and usage patterns.

## Dependencies
- python 3.12
- json
- datetime

## Input
- `buckets.json`: JSON file containing bucket information with the following structure:
    ```json
    {
        "buckets": [
            {
                "name": "string",
                "region": "string",
                "sizeGB": number,
                "versioning": boolean,
                "createdOn": "YYYY-MM-DD",
                "tags": {
                    "team": "string"
                }
            }
        ]
    }
    ```

## Key Features
1. **Bucket Summary**: Displays basic information for each bucket including name, region, size, and versioning status
2. **Large Bucket Detection**: Identifies buckets larger than 80GB that haven't been used for 90+ days
3. **Cost Analysis**: Generates cost reports by region and department using $0.0125/GB rate
4. **Storage Management**:
     - Flags buckets > 50GB for cleanup
     - Marks buckets > 100GB unused for 20+ days for deletion
     - Identifies buckets > 50GB unused for 90+ days for archival

## Output Files
- `deletion_queue.json`: List of bucket names marked for deletion
- `archive_candidates.json`: List of bucket names recommended for archival to Glacier

## Usage
Run the script with a valid `buckets.json` file in the same directory. The script will:
1. Print bucket summaries to console
2. Display cost reports
3. Show deletion and archival recommendations
4. Generate output JSON files

## Business Rules
- Deletion criteria: size > 100GB AND unused for 20+ days
- Archive criteria: size > 50GB AND unused for 90+ days
- Cleanup recommendation: size > 50GB
- Cost calculation: $0.0125 per GB