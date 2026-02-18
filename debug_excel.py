import pandas as pd

def debug_excel():
    file_path = 'MH.xlsx'
    try:
        df = pd.read_excel(file_path, header=None)
        print("Shape:", df.shape)
        # Write head to file to avoid console encoding issues
        with open('debug_head.txt', 'w', encoding='utf-8') as f:
            f.write(df.head(25).to_string())
        print("Wrote debug_head.txt")
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    debug_excel()
