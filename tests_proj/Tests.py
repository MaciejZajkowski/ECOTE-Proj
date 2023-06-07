import os 
import re
import sys
sys.path.append('..')
from classes.Parser import Parser
from classes.Changer import Changer
import pandas as pd
from classes.Refactoring_machine import Refactoring_machine



def test1():
    #testing locating and renaming of function that has multiple definitions
    rm = Refactoring_machine()
    return rm.change_name('../test_data/case1.py','../test_results/test1.txt','main','func2','my_new_func',2)
def test2():
    #testing locating and renaming of function that has one occurnace
    rm = Refactoring_machine()
    return rm.change_name('../test_data/case1.py','../test_results/test2.txt','main','func1','my_new_func')
def test3():
    #testing locating and renaming of function located inside other function
    rm = Refactoring_machine()
    return rm.change_name('../test_data/case1.py','../test_results/test3.txt','main.func1','func2','my_new_func')
def test4():
    #testing of localization of function wrong occurance num
    rm = Refactoring_machine()
    return rm.change_name('../test_data/case1.py','../test_results/test4.txt','main','func1','my_new_func',2)
def test5():
    #file path dont exist
    rm = Refactoring_machine()
    return rm.change_name('../testa/case1.py','../test_results/test5.txt','main','func1','my_new_func',2)
def test6():
    #function doesnt t exist
    rm = Refactoring_machine()
    return rm.change_name('../test_data/case1.py','../test_results/test6.txt','main','not_existing','my_new_func',2)
def test7():
    #name path doesnt  exist
    rm = Refactoring_machine()
    return rm.change_name('../test_data/case1.py','../test_results/test7.txt','main.not_existing','func1','my_new_func',2)
def test8():
    #extracting with no arguments
    rm = Refactoring_machine()
    return rm.extract_function('../test_data/case2.py','../test_results/test8.txt',11,14)
def test9():
    #extracting with no returns 
    rm = Refactoring_machine()
    return rm.extract_function('../test_data/case2.py','../test_results/test9.txt',2,8)
def test10():
    #extracting with arguments and returns  
    rm = Refactoring_machine()
    return rm.extract_function('../test_data/case2.py','../test_results/test10.txt',14,15)
def test11():
    # imposible extraxtion - wrong levels 
    rm = Refactoring_machine()
    return rm.extract_function('../test_data/case2.py','../test_results/test11.txt',39,44)
def test12():
    #extracting inside function
    rm = Refactoring_machine()
    return rm.extract_function('../test_data/case2.py','../test_results/test12.txt',23,26)
def test13():
    #extracting inside function
    rm = Refactoring_machine()
    return rm.extract_function('../test_data/case2.py','../test_results/test13.txt',23,26)
def test14():
    #exceeding end
    rm = Refactoring_machine()
    return rm.extract_function('../test_data/case2.py','../test_results/test14.txt',23,426)
def test15():
    #swapped line numbers
    rm = Refactoring_machine()
    return rm.extract_function('../test_data/case2.py','../test_results/test15.txt',15,14)