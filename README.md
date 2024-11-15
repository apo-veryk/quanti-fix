# Retail Product Quantity Converter

This Python script standardizes product quantities from a .csv file to commonly used global metrics, especially focusing on retail product names and quantities in Greek markets. The script identifies and replaces varying units and formats, allowing users to convert quantities (e.g., ml to liters) and customize target columns.

## Project Purpose
The script helps e-commerce businesses and vendors by normalizing product information, ensuring that product quantities in the CSV are consistent across entries. This is particularly useful for markets with non-standard naming conventions or multi-lingual product descriptions, like the Greek retail market.

## Features
- Converts quantities (like ml, g, kg, as well as even cm, mm, ug & many others) to standardized units.
- Recognizes Greek terminology for quantities.
- Allows the option to convert ml quantities to liters.
- Customizable columns for processing.

## Requirements
- Python 3.12.5
- Libraries specified in `requirements.txt`

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/apo-veryk/quanx-convertor.git
   cd quanx-convertor
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Input CSV File**: Specify the path to the .csv file containing product details.
2. **Target Columns**: Set the columns to process (default is ['name']). You can process multiple columns by adjusting the columns_to_process list.
3. **Run the Script**:
   ```bash
   python main.py
   ```
4. **Output CSV**: The processed data is saved to the specified output file path.


## Example of Packaging as a .exe (Optional)
- To make this script an executable (.exe) for easy distribution, you can use PyInstaller:

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```
2. **Run PyInstaller with the following command:**
   ```bash
   pyinstaller --onefile --noconsole main.py
   ```
- The .exe file will appear in the dist folder. This executable will allow users to run the script without needing Python installed.

## License
- This project is licensed under the [MIT License](https://github.com/apo-veryk/quanx-convertor/blob/main/LICENSE).
