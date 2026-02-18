import pandas as pd

def inspect_excel():
    file_path = 'HMCTS Demo Setup (1).xlsx'
    try:
        # Load the excel file without header first to see raw structure
        df = pd.read_excel(file_path, header=None)
        print("Shape:", df.shape)
        print("First 20 rows:")
        print(df.head(20))
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    inspect_excel()
