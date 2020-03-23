# Coursework Documentation

## Setup:
- make sure pip is fully up to date with the cmd:
    - **python -m pip install -U pip**

- Install anytree python module with:
    - **python -m pip install -U anytree**

- install graphviz with:
    - visit: https://graphviz.gitlab.io/_pages/Download/Download_windows.html
    - choose to download graphviz.msi
    - follow installation process when opening the .msi file
    - add the folder, that graphwiz is installed to, to the PATH

## Usage:
- To use the parsing script, **parser.py**, on the console you must be in the same folder as the script and the input file must be in the same.folder also
- to use the script simply call **python parser.py example.txt** , where in this case the input file is called **example.txt**.
- **The script expects there to always be spaces inbetween terminal symbols in the formula, expect for around the symbols '(' ,  ')' or ','**

## Outputs
- The outputs of calling this command on a valid input will be that:
    - Firstly, the grammar will be written to a file called **grammar.txt**.
    - Then the script will parse the formula and attempt to make a parse tree, the output of which will be saved to **parseTree.png**.
    - Printed to the console along this will be updates to say what has just happened.
    - Every time the script is called a log file will be made or appended to with information about the process. The file's name is **parser.log**.

- If at any stage there is an error, **ERROR: see log file** will be printed to the console.
- In the log file there will be appropriate information for the error encountered.
- A parseTree will only be `saved to **parseTree.png** if the formula is valid.