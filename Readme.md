# Log File Analyzer

## How to Run:
- Install Python with version >= 3.9 (http://python.org/downloads/)
- Clone the repository into an environment
- Execute `main_code.py`

## Assumptions:
- Default Format is Used  
- Protocol Numbers in log are in IANA decimals  
- Version 2 Logging is Used  
- Log lines are separated by newline and in ASCII text  
- Lookup table, protocol table are stored in CSV files

## Tests Done:
None 😳. Living life on the edge

## Analysis:
Has time complexity of O(N^2) where N = log_file_size. Each dict operation is O(N) at worst so we may spend O(N) per log line
