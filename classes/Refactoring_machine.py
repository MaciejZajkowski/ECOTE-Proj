import sys
import pandas as pd
sys.path.append('..')
from classes.Parser import Parser
from classes.Changer import Changer
import os
import pathlib


class Refactoring_machine():
    def __init__(self) -> None:
        self.parser = Parser()
        self.changer = Changer()
    
    def create_file(self,data):
        def apply_changes(line,tabs):
            line = tabs *"    " + line + '\n'
            return line
        lines = data.apply(lambda x: apply_changes( x['line_text'],x['level_num']),axis =1)
        return lines
        
       
    def _save_data(self,data,save_path):
        p = pathlib.Path(save_path)
        if not os.path.exists(p.parents[0]):
            return False,"Save Path does not exist"
        
        text = self.create_file(data)
        text.to_list()
        try:
            with open(save_path,'w') as f:
                for line in text:
                    f.write(line)
            f.close()
        except:
            return False,"error in writing file"
        return True, "Succes"
        
        
        
    def change_name(self,file_path,save_path,name_path,name,final_name,occurance = 1):
        if not os.path.exists(file_path):
            return False,"File Path does not exist"
        if not file_path.split('.')[-1] == 'py':
            return False, "It need to be python script"
        with open(file_path) as f:
            lines = f.readlines()
        data =  pd.DataFrame(self.parser.get_data(lines)).T
        data = self.parser.parse_functions(data)
        
        if name not in data['name'].values:
            return False,"Non Existing name"

        if len([function for function in data.functions.to_list() if name_path in function]) == 0:
            return False, "Non Existing name_path"
        if len(data.loc[(data['name'] == name) & (data.kind =='def') & (data.functions == name_path)]) < occurance or occurance <= 0:
            return False, "Not enaugth occurances / wrong occurnace number"
        data = self.changer.rename_function(data,name_path,name,final_name,occurance -1)
        return self._save_data(data,save_path)
        
    def extract_function(self,file_path,save_path,start_line,end_line,name = 'my_new_function'):
        start_line,end_line = start_line-1,end_line-1
        if not os.path.exists(file_path):
            return False,"Path does not exist"
        if not file_path.split('.')[-1] == 'py':
            return False, "It need to be python script"
        with open(file_path) as f:
            lines = f.readlines()
        
        data =  pd.DataFrame(self.parser.get_data(lines)).T
        data = self.parser.parse_functions(data)

        if name in data['name'].tolist():
            return False, 'function with this name already exists in program'
        if end_line < start_line:
            end_line,start_line = start_line,end_line
        
        if end_line < 0 or start_line < 0:
            return False, 'cannot have non positive parameters'

        if end_line > len(data):
            return False, "end line exceedes line numbers"
        if data.iloc[start_line].level_num != data.iloc[end_line].level_num:
            return False, "cannot extract function"
        
        data = self.changer.make_function(data,start_line,end_line,name)
        return self._save_data(data,save_path)
             
        
    