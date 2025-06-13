# Gemini 2.5 Pro code  
# Extract header data, Age, Sex, Diagnostic (1 or more numbers)

### Do a global replace .txt to .hea, txt_files to hea_files.  
### Change Dx to list of 1 or more items.  
### Save to csv file

import pandas as pd
import os



def extract_ecg_data(file_path):
    """
    Extracts Age, Sex, and Dx from a single ECG text file.

    Args:
        file_path (str): The full path to the input text file.

    Returns:
        dict: A dictionary containing the extracted data, or None if
              the required fields aren't found.
    """
    # Initialize a dictionary to hold the data from one file
    record = {
        'filename': os.path.basename(file_path),
        'Age': None,
        'Sex': None,
        'Dx': None
    }
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                # We strip leading/trailing whitespace from the line
                clean_line = line.strip()
                if clean_line.startswith('# Age:'):
                    # Split the line at the colon and take the second part
                    record['Age'] = clean_line.split(':', 1)[1].strip()
                elif clean_line.startswith('# Sex:'):
                    record['Sex'] = clean_line.split(':', 1)[1].strip()
                elif clean_line.startswith('# Dx:'):
                    record['Dx'] = clean_line.split(':', 1)[1].strip()

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")
        return None
        
    return record

def process_directory(directory_path):
    """
    Processes all .txt files in a given directory to extract ECG data.

    Args:
        directory_path (str): The path to the directory containing the .txt files.

    Returns:
        pandas.DataFrame: A DataFrame containing the data from all files.
    """
    all_records = []
    # List all files in the directory
    try:
        files = os.listdir(directory_path)
    except FileNotFoundError:
        print(f"Error: Directory not found at {directory_path}")
        return pd.DataFrame() # Return an empty DataFrame

    # Filter for .txt files
    txt_files = [f for f in files if f.endswith('.txt')]
    
    if not txt_files:
        print(f"No .txt files found in {directory_path}")
        return pd.DataFrame()

    print(f"Found {len(txt_files)} .txt files to process...")

    for filename in txt_files:
        file_path = os.path.join(directory_path, filename)
        # Extract data from one file
        record = extract_ecg_data(file_path)
        if record:
            all_records.append(record)
            
    # Convert the list of dictionaries into a Pandas DataFrame
    df = pd.DataFrame(all_records)
    return df

# --- Example Usage ---

# 1. Create a dummy directory and some sample files for demonstration
if not os.path.exists('ecg_data'):
    os.makedirs('ecg_data')

# Create sample file 1 (based on your uploaded file)
with open('ecg_data/HR00001.txt', 'w') as f:
    f.write("""HR00001 12 500 5000
HR00001.mat 16x1+24 1000.0(0)/mv 16 0 -115 13047 0 I
# Age: 56
# Sex: Female
# Dx: 251146004,426783006
# Rx: Unknown
""")

# Create sample file 2
with open('ecg_data/HR00002.txt', 'w') as f:
    f.write("""HR00002 12 500 5000
HR00002.mat 16x1+24 1000.0(0)/mv 16 0 -115 13047 0 I
# Age: 72
# Sex: Male
# Dx: 429622005
# Rx: Aspirin
""")

# Create sample file 3
with open('ecg_data/HR00003.txt', 'w') as f:
    f.write("""HR00003 12 500 5000
# Comment: No patient data available
# Age: Unknown
# Sex: Unknown
# Dx: Unknown
""")
    
# 2. Specify the directory containing your files
data_directory = 'ecg_data' # <-- IMPORTANT: Change this to your directory path

# 3. Process the directory and create the DataFrame
final_df = process_directory(data_directory)

# 4. Display the resulting DataFrame
print("\n--- Extracted Data ---")
print(final_df)
