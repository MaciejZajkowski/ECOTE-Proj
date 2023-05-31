import os
import pandas as pd
class Parser():
    def __init__(self) -> None:
        pass
    
    def _get_level(self,line):
        return line.count('    ')
    
    def _look_for_assign(self,line:str):
        if '=' in  line:
            splits = line.split('=')
            splits[0] = splits[0].replace(' ','')
            return True,splits
        else:
            return False, 0
    
    def _split_by_operators(self,line):
        operators = ['-','+','*','/']
        for operator in operators:
            line = line.replace(operator,'___TEMPORARY_SPLIT___')
        line = line.replace(' ','')
        return line.split('___TEMPORARY_SPLIT___')
    
    def _get_function(self,line):
        if line[0:5] == 'class':
            
            if '(' in line and ')' in line:
                parent = line[line.find("(")+1:line.find(")")]
                class_name = line[5:line.find("(")]
            else:
                parent = None
                class_name = line[5:]
            return 'class', class_name,parent
        elif line[0:3] == 'for':
            iterators = line[line.find("for")+3:line.find("in")]
            iterators = iterators.replace(" ",'')
            iterators = iterators.split(',')
            arguments = None
            if '(' and ')' in line:
                arguments = line[line.find("(")+1:line.find(")")]
                arguments = self._split_by_operators(arguments)
                if arguments[0] == '':
                    arguments = None
            return 'for', iterators,arguments
        elif line[0:3] == 'def':
            name = line[line.find("def")+3:line.find("(")]
            return 'def',name,None
        elif '('in line and ')' in line:
            name =line[:line.find("(")]
            arguments = line[line.find("(")+1:line.find(")")]
            arguments = self._split_by_operators(arguments)
            if arguments[0] == '':
                arguments = None
            return 'func',name,arguments
        elif 'return' in line:
            line = line.replace('return', '')
            arguments = self._split_by_operators(line)
            return 'return',None,arguments
        return None,None,None
    
    def get_data(self,lines):
        data = {}
        for i,line in enumerate(lines):
            row = {}
            row['original_text'] = line
            row['level_num'] = self._get_level(line)
            row['kind'] = None
            line = line.replace('    ','')
            line = line.replace('\n','')
            row['line_text'] = line
            assign_flag,ass_res = self._look_for_assign(line)
            if assign_flag:
                row["result"] = ass_res[0]
                line = ass_res[1]
            kind,name,arguments = self._get_function(line)
            row['kind'] = kind
            if kind == 'for':
                row['result'] = name
                row['name'] = None
            else:
                row['name'] = name
            if kind is None:
                arguments = self._split_by_operators(line)
            row['arguments'] = arguments
            data[i] = row
            #print (split_by_operators(line), data['original_text'])
            #split_by_operators(line)
        return data
    
    def parse_functions(self,data):
        last_f_name = {}
        last = ['main']
        for i,row in data.iterrows():
            #print(row['name'],row['level_num'],last)
            
            if row.kind == 'def' or row.kind == 'class':
                last.append(row['name'])
                #print('tutaj',row['name'])
            if row['level_num'] == 0:
                last_f_name[i] = 'main'
            else:
                #print('tutaj')
                last_f_name[i] = last[-1]
                
            if row['kind'] == 'return':
                last.pop()
        data['functions'] = pd.Series(last_f_name)
        return data
    
    def build_tree(path_to_script:str):
        if not os.path.exists(path_to_script):
            return False,"Path doesn not exist"
        if not path_to_script.split('.')[-1] == 'py':
            return False, "It need to be python script"
        with open('../test_data/case1.py') as f:
            lines = f.readlines()
             