import pandas as pd
import re
import sys

def extract_doc_number(operation_text):
    """Extract document number from operation description using regex"""
    if pd.isna(operation_text):
        return None
    match = re.search(r'№\s?(\d+)', str(operation_text))
    return match.group(1) if match else None

def to_float(value):
    """Convert string with spaces and commas to float"""
    if pd.isna(value) or value == '':
        return None
    try:
        # Replace spaces and commas
        cleaned = str(value).replace(' ', '').replace(',', '.')
        return float(cleaned)
    except:
        return None

def analyze_tax_transfers(input_file='06.02.2026_16-03-54.csv', output_file='tax_transfers_result.csv'):
    """
    Analyze tax transfers from CSV file
    Finds matching pairs where:
    - Қайтарилган (returned) sum from one tax matches Тўланган (paid) sum of another tax
    - Same operation date
    - Same document number
    """
    
    print(f"Reading file: {input_file}")
    try:
        df = pd.read_csv(input_file, sep=';', encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(input_file, sep=';', encoding='latin-1')
    
    # Strip whitespace from column names
    df.columns = [col.strip() for col in df.columns]
    
    print(f"Loaded {len(df)} rows")
    print(f"Columns: {list(df.columns)}")
    
    # Convert numeric columns
    df['Қайтарилган'] = df['Қайтарилган'].apply(to_float)
    df['Тўланган'] = df['Тўланган'].apply(to_float)
    
    # Extract document numbers
    df['doc_num'] = df['Операция мазмуни'].apply(extract_doc_number)
    
    # Find all rows with returns (Қайтарилган > 0)
    returns = df[(df['Қайтарилган'].notna()) & (df['Қайтарилган'] > 0)].copy()
    
    print(f"\nFound {len(returns)} rows with returns")
    
    transfers = []
    
    # For each return, find matching payment
    for idx, ret_row in returns.iterrows():
        operation_date = ret_row['Операция санаси']
        doc_num = ret_row['doc_num']
        returned_sum = ret_row['Қайтарилган']
        from_tax_code = ret_row['Солиқ коди']
        
        # Find matching payments with same date, doc number, and sum
        matching_payments = df[
            (df['Операция санаси'] == operation_date) &
            (df['doc_num'] == doc_num) &
            (df['Тўланган'] == returned_sum) &
            (df['Тўланган'].notna()) &
            (df['Тўланган'] > 0)
        ]
        
        for _, pay_row in matching_payments.iterrows():
            to_tax_code = pay_row['Солиқ коди']
            
            # Don't record self-transfers
            if from_tax_code != to_tax_code:
                transfers.append({
                    'Дата': operation_date,
                    'Из_налога': from_tax_code,
                    'В_налог': to_tax_code,
                    'Сумма': returned_sum,
                    'Номер_документа': doc_num if doc_num else ''
                })
    
    # Create result dataframe
    result_df = pd.DataFrame(transfers)
    
    if len(result_df) > 0:
        result_df = result_df.drop_duplicates()
        result_df = result_df.sort_values('Дата')
    
    # Save to CSV
    result_df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n✅ РЕЗУЛЬТАТЫ СОХРАНЕНЫ: {output_file}")
    print(f"Найдено перебросок: {len(result_df)}")
    print(f"\n{'Дата':<12} {'Из':<8} {'В':<8} {'Сумма':<15} {'Номер документа':<20}")
    print("-" * 70)
    
    for _, row in result_df.iterrows():
        print(f"{row['Дата']:<12} {row['Из_налога']:<8} {row['В_налог']:<8} {row['Сумма']:<15.2f} {row['Номер_документа']:<20}")
    
    return result_df

if __name__ == '__main__':
    input_file = sys.argv[1] if len(sys.argv) > 1 else '06.02.2026_16-03-54.csv'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'tax_transfers_result.csv'
    
    analyze_tax_transfers(input_file, output_file)
