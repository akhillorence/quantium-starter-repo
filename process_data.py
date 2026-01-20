import pandas as pd
import os

print("Starting data processing...")

data_folder = "data"
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

print(f"Found {len(csv_files)} CSV files: {csv_files}")

all_data = []

for file_name in csv_files:
    print(f"\nProcessing {file_name}...")
    
    file_path = os.path.join(data_folder, file_name)
    df = pd.read_csv(file_path)
    
    # DEBUG: Show what's in this file
    print(f"  Total rows in file: {len(df)}")
    print(f"  Unique products: {df['product'].unique()[:5]}...")  # Show first 5 only
    
    # Filter for Pink Morsel
    pink_morsel = df[df['product'].str.lower() == 'pink morsel'].copy()  # Use .copy() to avoid SettingWithCopyWarning
    
    print(f"  Found {len(pink_morsel)} Pink Morsel rows")
    
    if len(pink_morsel) > 0:
        # Convert price from string to float (remove $ sign)
        pink_morsel['price'] = pink_morsel['price'].str.replace('$', '', regex=False).astype(float)
        
        # Calculate sales (price * quantity)
        pink_morsel['sales'] = pink_morsel['quantity'] * pink_morsel['price']
        
        # Keep only needed columns
        final_data = pink_morsel[['sales', 'date', 'region']]
        
        # Add to collection
        all_data.append(final_data)
    else:
        print(f"  WARNING: No Pink Morsels found in {file_name}!")

# Combine all data
if all_data:
    combined_data = pd.concat(all_data, ignore_index=True)
    
    print(f"\n{'='*50}")
    print(f"✅ SUCCESS!")
    print(f"Total Pink Morsel rows: {len(combined_data)}")
    print(f"Date range: {combined_data['date'].min()} to {combined_data['date'].max()}")
    print(f"Regions: {combined_data['region'].unique()}")
    
    # Show summary statistics
    print(f"\nSales Summary:")
    print(f"Total sales: ${combined_data['sales'].sum():,.2f}")
    print(f"Average sales per transaction: ${combined_data['sales'].mean():.2f}")
    print(f"Maximum sale: ${combined_data['sales'].max():.2f}")
    print(f"Minimum sale: ${combined_data['sales'].min():.2f}")
    print(f"{'='*50}")
    
    # Save to file
    output_file = "formatted_sales_data.csv"
    combined_data.to_csv(output_file, index=False)
    
    print(f"\nFirst 5 rows of cleaned data:")
    print(combined_data.head())
    print(f"\nLast 5 rows of cleaned data:")
    print(combined_data.tail())
    print(f"\nSaved to: {output_file}")
    
else:
    print("\n❌ ERROR: No Pink Morsel data found in any file!")
    print("Check the product names in your CSV files.")

print("\nDone!")