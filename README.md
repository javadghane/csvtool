# csvtool

A command-line tool for working with CSV files with enhanced pipe support.


## Installation

### From Git (Recommended)
```bash
pip3 install git+https://github.com/maroofi/csvtool.git
```

### From PyPI
```bash
pip3 install csvtool
```

### From Source
```bash
git clone https://github.com/maroofi/csvtool.git
cd csvtool
python3 setup.py install --user
```

**Note**: To use it independently as a command-line tool, make sure you have `~/.local/bin` in your `$PATH` variable.

```bash
# Add to your ~/.bashrc
export PATH=~/.local/bin/:$PATH
source ~/.bashrc
```

## Usage

### Quick Start - Default Readable Mode
```bash
# Instantly view CSV in readable format
cat data.csv | csvtool
curl -s "https://example.com/data.csv" | csvtool
```

### Command Line Options

#### Show Help
```bash
csvtool -h
csvtool --help
```

#### Readable Format
```bash
# From file
csvtool readable data.csv

# From stdin (both work the same now!)
cat data.csv | csvtool
cat data.csv | csvtool readable -
```

#### Select Columns
```bash
# Select columns 1, 2, and 5
csvtool select -c 1,2,5 data.csv

# Select by column names
csvtool select -c "Year,Make,Price" data.csv

# From pipe
cat data.csv | csvtool select -c 1,3
```

#### Search in Columns
```bash
# Search for pattern in column 2
csvtool search -c 2 -s "Chevy" data.csv

# Search with regex
csvtool search -c 2 -s "^Chevy$" data.csv

# Search by column name
csvtool search -c "Make" -s "Ford" data.csv
```

#### Replace Values
```bash
# Replace values in column 2
csvtool replace -c 2 -o "Chevy" -n "Chevrolet" data.csv

# Replace in specific column by name
csvtool replace -c "Make" -o "Ford" -n "Ford Motor Co." data.csv
```

#### Global Options
```bash
# Treat first row as data (no header)
csvtool --no-header readable data.csv

# Custom delimiter
csvtool --delimiter ";" readable data.csv
```

## Example Data

Sample `test.csv` file:
```csv
Year,Make,Model,Description,Price
1997,Ford,E350,"ac, abs, moon",3000.00
1999,Chevy,"Venture ""Extended Edition""","",4900.00
1999,Chevy,"Venture ""Extended Edition, Very Large""",5000.00,
1996,Jeep,Grand Cherokee,"MUST SELL! air, moon roof, loaded",4799.00
```

## Examples

### Example 1: Quick CSV Preview (New!)
```bash
cat test.csv | csvtool
```
Output:
```
Year | Make  | Model                                      | Description                        | Price  
-----|-------|--------------------------------------------|------------------------------------|--------
1997 | Ford  | E350                                       | ac, abs, moon                      | 3000.00
1999 | Chevy | Venture "Extended Edition"                 |                                    | 4900.00
1999 | Chevy | Venture "Extended Edition, Very Large"     | 5000.00                           |        
1996 | Jeep  | Grand Cherokee                             | MUST SELL! air, moon roof, loaded | 4799.00
```

### Example 2: Select Chevy Cars and Show Specific Columns
```bash
csvtool search -c 2 -s '^Chevy$' test.csv | csvtool select -c 1,5,3 --no-header
```
Output:
```csv
Year,Price,Model
1999,4900.00,"Venture ""Extended Edition"""
1999,5000.00,"Venture ""Extended Edition, Very Large"""
```

### Example 3: Chain Operations
```bash
# Select columns, then search, then format
cat test.csv | csvtool select -c 1,2,5 | csvtool search -c 2 -s "Ford|Jeep" | csvtool
```

### Example 4: Data Processing Pipeline
```bash
# Download, filter, and display
curl -s "https://example.com/cars.csv" | csvtool search -c "Status" -s "Available" | csvtool
```

## Features

- ✅ **Default readable mode for piped input** - Just pipe CSV and view!
- ✅ **Column selection** by index or name
- ✅ **Pattern searching** with regex support  
- ✅ **Value replacement** in specific columns
- ✅ **Header handling** (with/without headers)
- ✅ **Custom delimiter support**
- ✅ **Pipe-friendly** design for Unix workflows
- ✅ **Readable formatting** with proper alignment
- ✅ **Stdin/stdout support** for command chaining

## Version History

### v1.3.0 (Latest)
- 🎉 **NEW**: Default readable mode for piped input (`command | csvtool`)
- Enhanced pipe detection and handling
- Improved error handling for broken pipes
- Better command-line interface

### v1.2.0
- Column selection and search functionality
- Replace command
- Header/no-header options

### v1.1.0
- Basic CSV reading and writing
- Command-line interface

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Author

Sourena MAROOFI

---

**Tip**: The new default behavior makes csvtool perfect for quick CSV inspection in data pipelines and shell scripts!
