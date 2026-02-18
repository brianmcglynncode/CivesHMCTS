import pandas as pd
import json
import os

def extract_demo_data():
    file_path = 'MH 4.xlsx'
    output_js_path = 'webapp/data.js'
    
    print(f"Reading {file_path}...")
    try:
        # Read the file
        df = pd.read_excel(file_path, header=None)
        
        # Data starts at Row 3 (index 3)
        # Col 3 (D): Category (step)
        # Col 4 (E): Description (action/features) - Comma separated
        # Col 6 (G): Location (actor)

        extracted_data = []
        
        # Start iterating from row index 3
        for index, row in df.iloc[3:].iterrows():
            def get_col(r, idx):
                if idx < len(r):
                    val = r.iloc[idx]
                    return str(val).strip() if not pd.isna(val) else ""
                return ""

            category = get_col(row, 3)
            description = get_col(row, 4)
            location = get_col(row, 6)
            
            # Clean up text
            category = category.replace('\u200b', '').strip()
            description = description.replace('\u200b', '').strip()
            location = location.replace('\u200b', '').strip()
            
            # Skip if no description
            if not description:
                continue

            # Use "HMCTS" as default actor if location is missing
            actor = location if location else "HMCTS"
            
            # Treat the entire description as one action, do not split by comma
            # as per user request to match row count (16 rows = 16 cards)
            
            # Just clean up newlines if any
            action_text = description.strip()
            
            extracted_data.append({
                "id": len(extracted_data) + 1,
                "step": category,
                "actor": actor,
                "action": action_text
            })

        print(f"Extracted {len(extracted_data)} items.")
        
        # Write to webapp/data.js
        js_content = f"window.demoData = {json.dumps(extracted_data, indent=4)};"
        
        with open(output_js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
            
        print(f"Successfully wrote data to {output_js_path}")
        
        # Also save as JSON for reference
        with open('webapp/data.json', 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=4)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_demo_data()
