import pandas as pd
import re

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).strip()
    # Remove zero-width spaces and other invisible characters
    text = text.replace('\u200b', '')
    return text

def process_demo_setup():
    input_file = 'Demo Setup.xlsx'
    output_file = 'Demo_Setup_Professional.xlsx'

    # Read the excel file
    # Based on previous analysis, data seems to start around row 3 (0-indexed) or so, 
    # but let's read without header and inspect to be robust
    df = pd.read_excel(input_file, header=None)

    # The data we saw:
    # Col 3 (D): Categories (e.g., "1. Introduction")
    # Col 4 (E): Features (e.g., "Overview of Cives")
    # Col 5 (F): Notes (e.g., "Slides")
    
    # Let's extract these 3 columns
    df_extracted = df.iloc[:, [3, 4, 5]].copy()
    df_extracted.columns = ["Category", "Feature", "Notes"]

    structured_data = []
    current_category = None

    for index, row in df_extracted.iterrows():
        cat = clean_text(row['Category'])
        feat = clean_text(row['Feature'])
        note = clean_text(row['Notes'])

        # Skip completely empty rows
        if not cat and not feat and not note:
            continue

        # Identify if this is a category header
        # It seems categories are numbered strings in the first column
        if cat and (not feat) and (not note):
             # It's a category header
             current_category = cat
             continue
        
        # If it has a feature, use the current category
        if feat:
            # If category is also present on this row (rare in this format but possible), use it
            if cat:
                current_category = cat
            
            entry = {
                "Category": current_category if current_category else "General",
                "Feature / Pain Point": feat,
                "Notes / Equipment": note
            }
            structured_data.append(entry)
        elif cat and not feat:
             # Case where it might be a category switch
             current_category = cat

    # Create new DataFrame
    df_clean = pd.DataFrame(structured_data)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df_clean.to_excel(writer, sheet_name='Demo Script', index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['Demo Script']

    # Add some cell formats.
    header_fmt = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#4F81BD',
        'font_color': '#FFFFFF',
        'border': 1
    })
    
    body_fmt = workbook.add_format({
        'text_wrap': True,
        'valign': 'top',
        'border': 1
    })

    # Set column widths
    worksheet.set_column('A:A', 30) # Category
    worksheet.set_column('B:B', 50) # Feature
    worksheet.set_column('C:C', 40) # Notes

    # Apply formats to header
    for col_num, value in enumerate(df_clean.columns.values):
        worksheet.write(0, col_num, value, header_fmt)
        
    # Apply formats to body
    # We can just overwrite the data with format
    for row_num, row_data in enumerate(df_clean.values):
        for col_num, value in enumerate(row_data):
            worksheet.write(row_num + 1, col_num, value, body_fmt)

    # Close the Pandas Excel writer and output the Excel file.
    writer.close()
    print(f"Successfully created {output_file}")

if __name__ == "__main__":
    process_demo_setup()
