import pandas as pd

def analyze_tax_transfers(csv_file):
    # Load the CSV report into a DataFrame
    df = pd.read_csv(csv_file)

    # Analyzing tax transfers
    summary = {
        'total_transfers': len(df),
        'total_amount': df['amount'].sum(),
        'average_amount': df['amount'].mean(),
        'min_amount': df['amount'].min(),
        'max_amount': df['amount'].max()
    }

    return summary

if __name__ == '__main__':
    # Example usage
    csv_file_path = 'path/to/your/report.csv'
    result = analyze_tax_transfers(csv_file_path)
    print(result)