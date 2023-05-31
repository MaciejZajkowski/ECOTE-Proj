import pandas as pd

class Changer():
    def __init__(self) -> None:
        pass
    
    def take_arguments_from_box(self,data,box):
        arg = []
        for i in range(box[0],box[1]):
            n_args = [ self.find_argument(data,x,i,data.iloc[i].functions) for x in data.iloc[i].arguments if not x.isnumeric() and "'" not in x and '"' not in x]
            arg = arg + n_args
        return arg

    def take_argument_from_box(self,data,box):
        arg = []
        for i in range(box[0],box[1]):
            n_args = [ self.find_argument(data,x,i,data.iloc[i].functions) for x in data.iloc[i].arguments if not x.isnumeric() and "'" not in x and '"' not in x]
            arg = arg + n_args
        return arg
        
        
    def find_argument(self,data,argument,line_num, function):
        _ = data.loc[(data.result == argument )& (data.functions == function)]
        potential_lines = [x for x in _.index.to_list() if x < line_num]
        potential_lines.sort()
        return potential_lines[-1]
    
    def rename_function(self,data,function_path,fname,name):
        index_of_occur = []
        for i,row in data.iterrows():
            if function_path in row.functions and row['name'] == fname:
                index_of_occur.append(i)
        new_lines_of_text = {}
        for i in data.index.to_list():
            if i in index_of_occur:
                new_lines_of_text[i] = data.iloc[i].line_text.replace(fname,name)
            else:
                new_lines_of_text[i] = data.iloc[i].line_text
        data.line_text = pd.Series(new_lines_of_text)
        return data
    
    def take_prerequesits(self,data,line_num):
    
        def _help_func(data,line_num):
            arguments = data.iloc[line_num].arguments
            prereq = data.loc[data.result.isin(arguments)].index.to_list()
            prereq = [x for x in prereq if x < line_num]
            if len(prereq) == 0:
                return []
            grand = []
            for i in prereq:
                    _ = _help_func(data,i)
                    if len(_) != 0:
                        grand.append(_[-1])
                        
            rv =  grand + prereq
            return rv
        prereq = _help_func(data,line_num)
        temp_lines = data.iloc[prereq]
        rv = []
        for res in temp_lines.result.unique():
            result_type_list = temp_lines.loc[temp_lines.result == res].index.to_list()
            result_type_list.sort()
            rv.append(result_type_list[-1])
        return rv
    
    def take_prerequesits_from_box(self,data,box):
        list_of_lines = data.loc[data.functions == data.iloc[box[1]].functions].index.to_list()
        list_of_lines = [x for x in list_of_lines if x > box[1]]
        prereq = []
        for i in list_of_lines:
            f = data.iloc[i].functions
            for arg in data.iloc[i].arguments:
                if not arg.isnumeric() and "'" not in arg and '"' not in arg:
                    prereq = prereq + [self.find_argument(data,arg,i,f)]
        
        prereq = pd.unique(prereq).tolist()
        prereq = [x for x in prereq if x in range(box[0],box[1])]
        return prereq
    
    def make_function(self,data,start_line,end_line,name):
        if data.iloc[start_line].level_num != data.iloc[end_line + 1].level_num or data.iloc[start_line].functions != data.iloc[end_line + 1].functions:
            return False
        returns = self.take_prerequesits_from_box(data,(start_line,end_line))
        arguments = self.take_arguments_from_box(data,(start_line,end_line))
        arguments = data.iloc[arguments].result.to_list()
        returns = data.iloc[returns].result.to_list()
        if len(returns) == 0:
            pass
        replace = "'"
        
        start_index = data.loc[data.functions == data.iloc[start_line].functions].index.to_list()[0]
        def_string = f"def {name}({str(arguments)[1:-1].replace(replace,'')}):"
        start_level = data.iloc[start_line].level_num
        fun ={start_index: [def_string,start_level]} 
        
        start_index_backup = start_index 
        
        
        for i in range(start_line,end_line):
            start_index +=1
            fun[start_index] = [data.iloc[i].line_text,start_level +1]
        
        if len(returns) != 0:
            start_index +=1
            fun[start_index] = [f"return {str(returns)[1:-1].replace(replace,'')}",start_level+1]
            func_str = f"{str(returns)[1:-1].replace(replace,'')} = {name}({str(arguments)[1:-1].replace(replace,'')})"
        else:
            func_str = f"{name}({str(arguments)[1:-1].replace(replace,'')})"
            
        envoction = pd.DataFrame([{'line_text':func_str,'level_num':start_level}])
        
        
        
        
        my_function = pd.DataFrame(fun).T
        my_function.columns=['line_text','level_num']
        
        po = data.loc[data.index >  end_line][['line_text','level_num']]
        przed = data.loc[data.index <  start_line][['line_text','level_num']]
            
    
        #print(func_str)
        changed = pd.concat([przed,envoction,po]).reset_index(drop=True)
        przed = changed.iloc[changed.index < start_index_backup]
        po = changed.iloc[changed.index > start_index_backup]
        return pd.concat([przed,my_function,po]).reset_index(drop=True)
    
    