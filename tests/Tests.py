import sys
sys.path.append('..')
from classes.Changer import Changer
from classes.Refactoring_machine import Refactoring_machine
from classes.Parser import Parser

def test1():
    rm = Refactoring_machine()
    return rm.change_name('../test_data/case1.py','./test1.txt','main','func1','new_func')[0]

def test2():
    rm = Refactoring_machine()
    return rm.change_name('../test_data/case1.py','./test_results/test2.txt','main','func2','new_func')[0]

test2()