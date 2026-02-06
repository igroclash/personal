import pandas as pd

# Function to analyze tax transfers

def analyze_tax_transfers(csv_file):
    # Load the CSV file
    data = pd.read_csv(csv_file)

    # Extracting document numbers from operation descriptions
    data['Document_Number'] = data['Operation_Description'].str.extract(r'(\d{1,10}\b)')

    # Convert date columns to datetime
    data['Date'] = pd.to_datetime(data['Date'])
    data['Returned_Date'] = pd.to_datetime(data['Returned_Date'])

    # Merging returned and paid amounts on the same date and document number
    merged_data = pd.merge(data[['Date', 'Document_Number', 'Returned_Amount']],
                            data[['Returned_Date', 'Document_Number', 'Paid_Amount']],
                            left_on=['Date', 'Document_Number'],
                            right_on=['Returned_Date', 'Document_Number'],
                            how='inner')

    # Creating a comprehensive result table
    result_table = merged_data[['Document_Number', 'Returned_Amount', 'Paid_Amount']].copy()

    # Analyzing results
    result_table['Difference'] = result_table['Paid_Amount'] - result_table['Returned_Amount']
    result_table['Status'] = result_table['Difference'].apply(lambda x: 'Matched' if x == 0 else 'Mismatch')

    return result_table

# Example usage
# result = analyze_tax_transfers('path/to/your/file.csv')
# print(result)