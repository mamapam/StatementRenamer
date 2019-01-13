# StatementRenamer
This program will traverse a list of downloaded CIBC Bank statements for both Chequing accounts and VISA Credit accounts and using the path specified in where you want it saved will rename the statement and save it with the correct name.

## Getting Started
The following steps will explain how to setup the script to rename downloaded statements.

### Prequisites
This script requires python 3 and the PyPDF2 module to run. 

```
pip3 install PyPDF2
```

### Steps to Run
Ensure the statements to rename are downloaded in the same directory. Update the script with this directory.
```
pathToFiles = r"path/to/directory"
```

Run the script.
```
python3 StatementRenamer.py
```
