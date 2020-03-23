import sys
from pathlib import Path
from anytree import Node
from anytree.exporter import UniqueDotExporter


def main():
    # the lists we'll need
    VARIABLES = []  # 0
    CONSTANTS = []  # 1
    PREDICATES = []  # 2
    equality = []  # 3
    CONNECTIVES = []  # 4
    QUANTIFIERS = []  # 5
    formula = []  # 6
    F = []  # 7
    A = []  # 8
    lists = [VARIABLES, CONSTANTS, PREDICATES, equality, CONNECTIVES, QUANTIFIERS, formula, F, A]

    # read in input file given
    inputFileName = sys.argv[1]
    check = readInFile(inputFileName, lists)
    if check[0] == 0:
        status = "'Input Error'"
        msg = check[1]
        log(inputFileName, status, msg)
        print("ERROR: see log file")
        return

    # make corresponding grammar
    check = makeGraamar(lists)
    if check[0] == 0:
        status = "'Input Error'"
        msg = check[1]
        log(inputFileName, status, msg)
        print("ERROR: see log file")
        return
    terminal_symbols = check[2]
    terminal_symbols = sorted(terminal_symbols, key=len)
    terminal_symbols.reverse()
    non_terminal_symbols = check[3]

    ######### format the formula #########
    # formula is empty -> error
    if len(lists[6]) == 0:
        status = "'Input Error'"
        msg = "No formula given"
        log(inputFileName, status, msg)
        print("ERROR: see log file")
        return
    # split each symbol apart in the formula
    formula_temp = []
    for i in lists[6]:
        checker = False
        for j in terminal_symbols:
            # are they the same
            if i == j:
                checker = True
                formula_temp.append(i)
                break
        #  else are there matching symbols in there
        if not checker:
            keys = []
            # check for (
            for a in range(len(i)):
                if i[a] == '(':
                    keys.append(a)
            # check for )
            for a in range(len(i)):
                if i[a] == ')':
                    keys.append(a)
            # check for ','
            for a in range(len(i)):
                if i[a] == ',':
                    keys.append(a)

            if len(keys) > 0:
                checker = True
                keys.sort()
                for j in range(len(keys)):
                    if j == 0:
                        if keys[j] == 0:
                            formula_temp.append(i[keys[j]])
                            if len(keys) == 1:
                                formula_temp.append(i[keys[j]+1:len(i)])
                        else:
                            formula_temp.append(i[0:keys[j]])
                            formula_temp.append(i[keys[j]])
                    else:
                        formula_temp.append(i[keys[j-1]+1:keys[j]])
                        formula_temp.append(i[keys[j]])
                        if j == (len(keys)-1):
                            if keys[j] != len(i)-1:
                                formula_temp.append(i[keys[j]+1:len(i)])
        if not checker:
            status = "Error"
            msg = f"Unspecified symbol '{i}' used in formula"
            log(inputFileName, status, msg)
            print("ERROR: see log file")
            return
    # remove all empty elements
    for i in formula_temp:
        if i == "":
            formula_temp.remove("")
    lists[6] = formula_temp
    # check no invalid symbol is in  the formula
    counter = 0
    for i in lists[6]:
        c = True
        for j in terminal_symbols:
            if str(i) == str(j):
                c = False
                break
        if c:
            status = "'Formula Syntax Error'"
            msg = f"Unspecified symbol '{i}' used in formula at position {counter}"
            log(inputFileName, status, msg)
            print("ERROR: see log file")
            return
        counter += 1
    ######################################

    # start the parsing of the formula
    check = parser(lists, terminal_symbols, non_terminal_symbols)
    if check[0] == 0:
        status = "'Formula Syntax Error'"
        msg = check[1] + "\n\t\tCross refernce with the productions in 'grammar.txt' and the input formula for further clarifaction of the syntax error."
        log(inputFileName, status, msg)
        print("ERROR: see log file")
        print()
        return

    ######### show succes at document end #########
    status = "Success"
    msg = "None"
    log(inputFileName, status, msg)


def readInFile(inputFileName, lists):
    file = open(Path(Path.cwd()) / inputFileName, "r")

    # keep track of what current list we're in
    placeholder = 0

    info = file.read().splitlines()
    # search line by line and fill in the relevant list
    for x in info:
        temp = x.split(' ')
        # remove the left over empty spaces
        i = 0
        while i < len(temp):
            if temp[i] == "":
                temp.remove("")
                i -= 1
            i += 1

        if "variables:" in temp[0]:
            placeholder = 0
            for i in range(1, len(temp)):
                lists[0].append(temp[i])
        elif "constants:" in temp[0]:
            placeholder = 1
            for i in range(1, len(temp)):
                lists[1].append(temp[i])
        elif "predicates:" in temp[0]:
            placeholder = 2
            for i in range(1, len(temp)):
                lists[2].append(temp[i])
        elif "equality:" in temp[0]:
            placeholder = 3
            for i in range(1, len(temp)):
                lists[3].append(temp[i])
        elif "connectives:" in temp[0]:
            placeholder = 4
            for i in range(1, len(temp)):
                lists[4].append(temp[i])
        elif "quantifiers:" in temp[0]:
            placeholder = 5
            for i in range(1, len(temp)):
                lists[5].append(temp[i])
        elif "formula:" in temp[0]:
            placeholder = 6
            for i in range(1, len(temp)):
                lists[6].append(temp[i])
        else:
            for i in temp:
                lists[placeholder].append(i)

    # error check there are spaces around all the quantifiers
    # i is the formula piece
    for i in lists[6]:
        # j is the quan piece
        for j in lists[5]:
            if j in i:
                if i == j:
                    continue
                else:
                    checker = False
                    for z in range(0, 6):
                        for x in lists[z]:
                            if i == x:
                                checker = True
                                break
                    if not checker:
                        return (0, f"Space needed around quantifier '{j}' in formula.")

    if len(lists[0]) == 0 and len(lists[1]) == 0:
        return (0, "No variables or constants defined.")
    elif len(lists[0]) == 0 and len(lists[2]) != 0:
        return (0, "Predicates can only be assigned if there are more than 0 variables defined.")
    elif len(lists[3]) != 1:
        return (0, "Incorrect number of Equality symbols.")
    elif len(lists[4]) != 5:
        return (0, "Incorrect number of Connective symbols.")
    elif len(lists[5]) != 2:
        return (0, "Incorrect number of Quantifier symbols.")

    return (1, "None")
# reads in data and stores them in lists


def makeGraamar(lists):
    # check symbols haven't been used twice
    # check each row on itself
    for i in range(6):
        for j in range(0, len(lists[i])):
            for z in range(j+1, len(lists[i])):
                if lists[i][z] == lists[i][j]:
                    return (0, f"Symbol '{lists[i][j]}'' is used to refer to more than one thing, on line {i}.")
    # check every other row
    for i in range(6):
        for j in lists[i]:
            for z in range(i+1, 6):
                for x in lists[z]:
                    if j == x:
                        return (0, f"Symbol '{x}'' is used to refer to more than one thing, on lines {i+1} and {z+1}.")

    Terminals = []
    # add all var symbols to terminals
    for i in lists[0]:
        Terminals.append(i)
    # and all constant symbols to terminals
    for i in lists[1]:
        Terminals.append(i)

    # PRED
    PRED_TEMP = []
    for i in lists[2]:
        string = i[0:i.index('[')]

        # add the symbol for the predicate into the terminals as we go
        Terminals.append(string)

        int_used = int(i[i.index('[')+1:i.index(']')])
        if int_used < 1:
            return (0, "Number less than 1 used in predicate definition.")
        string += ' ( '
        for j in range(int_used):
            if int_used == 1:
                string += "@VAR"
            elif j == int_used-1:
                string += "@VAR"
            else:
                string += "@VAR , "
        string += ' )'
        PRED_TEMP.append(string)
    for i in range(len(lists[2])):
        lists[2][i] = PRED_TEMP[i]

    # F
    lists[7].append("@PRED")
    lists[7].append("( @F @CONC @F )")
    lists[7].append("@A")
    lists[7].append("@QUAN @VAR @F")
    lists[7].append(lists[4][4] + "  @F ")

    # CONC
    for i in lists[4]:
        Terminals.append(i)
    del lists[4][4]

    # A
    lists[8].append("( @CONST " + lists[3][0] + " @CONST )")
    lists[8].append("( @CONST " + lists[3][0] + " @VAR )")
    lists[8].append("( @VAR " + lists[3][0] + " @CONST )")
    lists[8].append("( @VAR " + lists[3][0] + " @VAR )")

    # QUAN
    for i in range(len(lists[5])):
        Terminals.append(lists[5][i])

    # check terminals for invalid characters
    for i in Terminals:
        if ")" in i:
            return (0, f"The symbol '{i}' contains the reserved character ')'.")
        elif "(" in i:
            return (0, f"The symbol '{i}' contains the reserved character '('.")
        elif "," in i:
            return (0, f"The symbol '{i}' contains the reserved character ','.")
        elif "=" in i:
            return (0, f"The symbol '{i}' contains the reserved character '=' for only the equality symbol.")
        elif ":" in i:
            return (0, f"The symbol '{i}' contains the reserved character ':'.")
        elif "'" in i:
            return (0, f"The symbol '{i}' contains the reserved character '.")
    Terminals.append(",")
    Terminals.append("(")
    Terminals.append(")")
    Terminals.append(lists[3][0])

    # make the grammar the user will read
    # write the Terminal symbols
    grammar = "Terminals: {\n"
    terminal_string = ""
    for i in Terminals:
        terminal_string += '"' + i + '" , '
    terminal_string = terminal_string[0:len(terminal_string)-2]
    grammar += terminal_string + '\n}\n\n'

    # write the non_Terminals symbols
    non_Terminals = ['@VAR', '@CONST', '@PRED', '@F', '@CONC', '@A', '@QUAN']
    grammar += "Non-Terminals: {\n"
    non_Terminals_string = ""
    for i in non_Terminals:
        non_Terminals_string += '"' + i + '" , '
    non_Terminals_string = non_Terminals_string[0:len(non_Terminals_string)-2]
    grammar += non_Terminals_string + '\n}\n\n'

    # write the start symbol
    start_symbol = '@F'
    grammar += "Start symbol: {\n"
    grammar += '"' + start_symbol + '"'
    grammar += '\n}\n\n'

    # write the productions
    productions = ""
    # @VAR
    productions += '@VAR -> '
    for i in lists[0]:
        productions += i + ' | '
    productions = productions[0:len(productions)-3]
    productions += '\n'
    # @CONST
    productions += '@CONST -> '
    for i in lists[1]:
        productions += i + ' | '
    productions = productions[0:len(productions)-2]
    productions += '\n'
    # @PRED
    productions += '@PRED -> '
    for i in lists[2]:
        productions += i + ' | '
    productions = productions[0:len(productions)-2]
    productions += '\n'
    # @F
    productions += '@F -> '
    for i in lists[7]:
        productions += i + ' | '
    productions = productions[0:len(productions)-2]
    productions += '\n'
    # @CONC
    productions += '@CONC -> '
    for i in lists[4]:
        productions += i + ' | '
    productions = productions[0:len(productions)-2]
    productions += '\n'
    # @A
    productions += '@A -> '
    for i in lists[8]:
        productions += i + ' | '
    productions = productions[0:len(productions)-2]
    productions += '\n'
    # @QUAN
    productions += '@QUAN -> '
    for i in lists[5]:
        productions += i + ' | '
    productions = productions[0:len(productions)-2]
    productions += '\n'
    # write productions to the grammar
    grammar += "Productions: {\n"
    grammar += productions
    grammar += '}\n'

    # writes grammar to a file
    pth = Path(Path.cwd()) / "grammar.txt"
    if Path("grammar.txt").is_file():
        f = open(pth, "w")
    else:
        f = open(pth, "w+")
    f.write(grammar)
    f.close()

    # prints grammar to the console aswell
    print()
    print("Grammar written into grammar.txt")
    print()

    # returns these lists if needed
    return (1, "None", Terminals, non_Terminals)
# makes the grammar and lists for non-terminals


def fCheck(lists, symbols):
    # check its a predicate
    for i in lists[2]:
        x = i.split(" ")
        if symbols[0] == x[0]:
            return lists[7][0]
    # check its a bracket
    if symbols[0] == '(':
        # then check if its A || f conc f
        # first check if its a var or constant symbol
        for i in lists[0]:
            if symbols[1] == i:
                return lists[7][2]
        for i in lists[1]:
            if symbols[1] == i:
                return lists[7][2]
        # check if its f conc f
        return lists[7][1]
    # check if quantifier
    for i in lists[5]:
        if symbols[0] == i:
            for j in lists[0]:
                if symbols[1] == j:
                    return lists[7][3]
    # check if negation
    temp = lists[7][4].split(" ")
    if symbols[0] == temp[0]:
        return lists[7][4]

    return 0
# pass it 2 symbols in symbols
# returns the correct symbols from F or 0


def aCheck(lists, symbols):
    options = [0, 1, 2, 3]

    # check bracket
    if symbols[0] != '(':
        return 0

    # check var
    for i in lists[0]:
        if symbols[1] == i:
            if 0 in options:
                options.remove(0)
            if 1 in options:
                options.remove(1)
            break
    # check constant
    for i in lists[1]:
        if symbols[1] == i:
            if 2 in options:
                options.remove(2)
            if 3 in options:
                options.remove(3)
            break

    # check equality
    if symbols[2] != lists[3][0]:
        return 0

    # check var
    for i in lists[0]:
        if symbols[3] == i:
            if 0 in options:
                options.remove(0)
            if 2 in options:
                options.remove(2)
            break
    # check constant
    for i in lists[1]:
        if symbols[3] == i:
            if 1 in options:
                options.remove(1)
            if 3 in options:
                options.remove(3)
            break

    # check bracket
    if symbols[4] != ')':
        return 0

    if len(options) != 1:
        return 0
    else:
        return lists[8][options[0]]
# pass it 5 symbols in symbols
# returns the correct symbols from A or 0


def predCheck(lists, symbols):
    whichPredicate = 0
    match = False
    # check first symbol
    for i in lists[2]:
        x = i.split(" ")
        if symbols[0] == x[0]:
            match = True
            break
        whichPredicate += 1

    if not match:
        return 0

    match = lists[2][whichPredicate]
    match = match.split(" ")
    length = len(match)
    symbols = symbols[0:length]
    if len(symbols) != length:
        return 0
    # check brackets
    if symbols[1] != '(':
        return 0
    if symbols[-1] != ')':
        return 0

    # check interior
    symbols = symbols[2:len(symbols)-1]

    if len(symbols) > 1:
        for i in range(0, len(symbols)):
            match = False
            # for the last symbol
            if i == len(symbols) - 1:
                for j in lists[0]:
                    if symbols[i] == j:
                        match = True
                        break
                if not match:
                    return 0
            else:
                # for any other part of the interior
                if (i+1) % 2 == 1:
                    for j in lists[0]:
                        if symbols[i] == j:
                            match = True
                            break
                    if not match:
                        return 0
                else:
                    if symbols[i] != ',':
                        return 0
    # for singular things
    elif len(symbols) == 1:
        for j in lists[0]:
            if symbols[0] == j:
                match = True
                break
        if not match:
            return 0
    else:
        return 0

    return lists[2][whichPredicate]
# pass it the formula starting at the symbol we are analysing and ending at the end of the formula eg: formula[x:]
# returns the correct symbols from PRED or 0


def varCheck(lists, symbol):
    for i in lists[0]:
        if symbol == i:
            return symbol
    return 0
# pass one symbol
# returns the correct symbols from VAR or 0


def constantsCheck(lists, symbol):
    for i in lists[1]:
        if symbol == i:
            return symbol
    return 0
# pass one symbol
# returns the correct symbols from CONSTANT or 0


def connecCheck(lists, symbol):
    for i in lists[4]:
        if symbol == i:
            return symbol
    return 0
# pass one symbol
# returns the correct symbols from CONNECTIVE or 0


def quanCheck(lists, symbol):
    for i in lists[5]:
        if symbol == i:
            return symbol
    return 0
# pass one symbol
# returns the correct symbols from QUAN or 0


def checkList(x, symbol):
    checker = False
    for i in x:
        if symbol == i:
            checker = True
            break
    return checker
# returns true if symbol is in list


def parser(lists, terminal_symbols, non_terminal_symbols):
    formula = lists[6]
    attempted_formula = []
    current_symbol = 0

    origin = Node("@F")

    check = recursiveCheck(lists, terminal_symbols, non_terminal_symbols, origin, formula, attempted_formula, current_symbol)

    # check output
    if check[0] == 0:
        return check
    elif len(attempted_formula) != len(formula):
        if len(attempted_formula) < len(formula):
            x = len(formula) - len(attempted_formula)
            return (0, f"The Parse Tree didn't match original formula. The formula has {x} more symbol(s) at the end: {formula[len(formula)-x:len(formula)]}")
        elif len(attempted_formula) > len(formula):
            x = len(attempted_formula) - len(formula)
            return (0, f"The Parse Tree didn't match original formula. The parse tree formulas {x} more symbol(s) at the end: {attempted_formula[len(attempted_formula)-x:len(attempted_formula)]}")

    check = True
    wrong = 0
    for i in range(len(attempted_formula)):
        if attempted_formula[i] != formula[i]:
            wrong = i
            check = False
            break
    if check:
        # output graph
        UniqueDotExporter(origin).to_picture("parseTree.png")
        print("Full Parse Tree successfully constucted and saved to parseTree.png")
        print()
        return (1, "None")
    else:
        return (0, f"The Parse Tree didn't match original formula. Difference found at symbol '{wrong}' with symbol '{formula[wrong]}'")


def recursiveCheck(lists, terminal_symbols, non_terminal_symbols, i, formula, attempted_formula, current_symbol):
    if checkList(terminal_symbols, i.name):
        feedback = i
    elif i.name == '@VAR':
        x = varCheck(lists, formula[current_symbol])
        feedback = x
    elif i.name == '@CONST':
        x = constantsCheck(lists, formula[current_symbol])
        feedback = x
    elif i.name == '@PRED':
        x = predCheck(lists, formula[current_symbol:])
        feedback = x
    elif i.name == '@CONC':
        x = connecCheck(lists, formula[current_symbol])
        feedback = x
    elif i.name == '@QUAN':
        x = quanCheck(lists, formula[current_symbol])
        feedback = x
    elif i.name == '@F':
        x = fCheck(lists, formula[current_symbol:current_symbol + 2])
        feedback = x
    elif i.name == '@A':
        x = aCheck(lists, formula[current_symbol:current_symbol + 5])
        feedback = x

    if feedback == 0:
        return (0, f"Not a valid syntax in the formula around character '{formula[current_symbol]}' at position number '{current_symbol}' in the formula", current_symbol)
    else:
        working_symbols = feedback.split(" ")
        for x in working_symbols:
            if checkList(non_terminal_symbols, x):
                n = Node(x, parent=i)
                feedback = recursiveCheck(lists, terminal_symbols, non_terminal_symbols, n, formula, attempted_formula, current_symbol)
                if feedback[0] == 0:
                    return (0, feedback[1], current_symbol)
                current_symbol = feedback[2]
            elif checkList(terminal_symbols, x):
                if "\\" in x[0]:
                    n = Node("\\\\" + x[1:], parent=i)
                else:
                    n = Node(x, parent=i)
                attempted_formula.append(x)
                current_symbol += 1

        return (1, "", current_symbol)


def log(fileName, status, msg):
    # get file address
    pth = Path(Path.cwd()) / "parser.log"

    # editing the file
    if Path('parser.log').is_file():
        f = open(pth, "a")
    # creating the log file if needed
    else:
        f = open(pth, "w+")

    f.write(f"Input filename: {fileName}\n")
    f.write(f"Status: {status}\n")
    f.write(f"Errors: {msg}\n")
    f.write("\n")
    f.close()
# appends to the log file with the details


main()
