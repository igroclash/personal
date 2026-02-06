import pandas as pd
import re

# Load the CSV file
input_file = 'tax_transfers.csv'
output_file = 'tax_transfer_analysis.csv'

data = pd.read_csv(input_file)

# Prepare a DataFrame to store results
results = []

# Iterate through the DataFrame to find matching records
for index, row in data.iterrows():
    if row['Қайтарилган'] == row['Тўланган']:
        # Regex to extract document number from the operation description
        match = re.search(r'Н./([0-9]+)', row['Операция мазмуни'])
        document_number = match.group(1) if match else 'Не найдено'
        results.append({
            'Дата': row['Операция санаси'],
            'Из_налога': row['Солиқ коди'],
            'В_налог': row['Солиқ номи'],
            'Сумма': row['Тўлган'],
            'Номер_документа': document_number
        })

# Create a DataFrame from results and save to a new CSV file
results_df = pd.DataFrame(results)
results_df.to_csv(output_file, index=False, encoding='utf-8-sig')
print('Analysis completed and output saved to', output_file)