import sys
sys.path.append('.')
from Parser import Parser
from Changer import Changer

class Refactoring_machine():
    def __init__(self) -> None:
        self.parser = Parser()
        self.changer = Changer()
    
    def change_name(file_path,save_path,name_path,name,final_name):
        
    