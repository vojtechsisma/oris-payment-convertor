import csv
from datetime import datetime
import argparse

def load_bank_config(config_file):
    bank_config = {}
    with open(config_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            bank_config[row['banka']] = {
                'datum': row['datum'],
                'vs': row['vs'],
                'castka': row['castka']
            }
    return bank_config

def convert(input_file, output_file, bank_name, encoding='utf-8'):
    bank_config = load_bank_config('bank_def.csv')
    bank = bank_config.get(bank_name)
    if not bank:
        print(f"Banka '{bank_name}' nenalezena v konfig. souboru.")
        return
    
    with open(input_file, 'r', encoding=encoding) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        
        with open(output_file, 'w', newline='', encoding='utf-8') as output:
            writer = csv.writer(output, delimiter=';')
            
            for row in reader:
                date = datetime.strptime(row[bank['datum']], '%d.%m.%Y').strftime('%Y-%m-%d')
                variable_symbol = row[bank['vs']].lstrip('0')
                amount = row[bank['castka']]

                writer.writerow([date, variable_symbol, amount, '', ''])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Csv konvertor plateb do oris formatu.')
    parser.add_argument('--input', help='Vstupni soubor, default input.csv', default='input.csv')
    parser.add_argument('--output', help='Vystupni soubor, default output.csv', default='output.csv')
    parser.add_argument('--bank', help='Nazev banky v bank_def.csv', default='csob')
    parser.add_argument('--encoding', help='Kodovani vstupniho souboru, default utf-8', default='utf-8')
    args = parser.parse_args()

    convert(input_file=args.input, output_file=args.output, bank_name=args.bank, encoding=args.encoding)
