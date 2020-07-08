
from masses import masses

def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])

def sort(tup):  
    tup.sort(key = lambda x: x[0])  
    return tup  

def sum_1_or_2_nums(form, pos, mw, mass):
    ms = 0
    # check for > 9
    if form[pos:pos+2].isnumeric():
        ms += mass * int(form[pos:pos+2])
    else:
        # check for > 1
        if form[pos:pos+1].isnumeric():
            ms += mass * int(form[pos:pos+1])
        else:
            # no subscript just 1 element
            ms += mass
    return ms + mw

formula = 'C5H7(NO3)3(CCl3)2' # 489.86 from https://www.lenntech.com/calculators/molecular/molecular-weight-calculator.htm

l = list((parenthetic_contents(formula)))

lst = sorted(l, key = lambda x: x[1], reverse=False)

mw = 0
total_mw = 0

for i, c in enumerate(lst):
    # find the str in the formula and check the
    # next item to see if it's a number for the multiplier
    form = c[1]
    print(f'form {form}')
    srch_str = '('+form+')'
    srch_len = len(srch_str)
    pos = formula.find(srch_str)
    if formula[pos+srch_len].isnumeric():
        multiplier = int(formula[pos+srch_len])
    else: multiplier = 1 # number outside of parenthesis
    # delete this part of the formula so last bit can be calculated
    if multiplier != 1:
        # a number is present assuming < 10
        print(f'srch_str {srch_str}')
        formula = formula.replace(formula[pos:pos+srch_len+1], '')
    # ToDo: delete parts of orginal string too
    for j in range(len(form)):
        # check to see if numeric and then skip if so
        if not form[j:1].isnumeric():
            # check both 1 and 2 letter elements
            mass1 = masses.get(form[j:j+1])
            mass2 = masses.get(form[j:j+2])
            # do mass2 first and skip mass1 unless mass2 is None
            if not mass2 is None: 
                mw = sum_1_or_2_nums(form, j+2, mw, mass2)
                print('mass2', mw)
            else:
                if not mass1 is None:
                    # one letter element
                    mw = sum_1_or_2_nums(form, j+1, mw, mass1)
                    print('mass1', mw)
    total_mw += mw * multiplier 
    print(f'formula({form}) = {mw} and mw * multiplier = {mw*multiplier}')
    mw = 0
print(f'total_mw {total_mw}')
print(f'formula left to do = {formula}')


    



# using an outside parenthesis set gives
#[(1, 'NO3'), (0, 'C3H5(NO3)3')]

#print(list(parenthetic_contents('(a(b(c)(d)e)(f)g)')))
#[(2, 'c'), (2, 'd'), (1, 'b(c)(d)e'), (1, 'f'), (0, 'a(b(c)(d)e)(f)g')]

#https://stackoverflow.com/questions/4284991/parsing-nested-parentheses-in-python-grab-content-by-level

