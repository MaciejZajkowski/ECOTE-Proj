import pandas as pd

class Changer():
    def __init__(self) -> None:
        pass
    
    def take_arguments_from_box(self,data,box):
        arg = []
        for i in range(box[0],box[1]):
            n_args = [ self.find_argument2(data,x,i,data.iloc[i].functions) for x in data.iloc[i].arguments if not x.isnumeric() and "'" not in x and '"' not in x if x is not None]
            arg = arg + n_args
        arg = [x for x in arg if x is not None]
        arg = pd.Series(arg).unique().tolist()
        return arg

    def take_argument_from_box(self,data,box):
        arg = []
        for i in range(box[0],box[1]):
            n_args = [ self.find_argument(data,x,i,data.iloc[i].functions) for x in data.iloc[i].arguments if not x.isnumeric() and "'" not in x and '"' not in x]
            arg = arg + n_args
        return arg
        
        
    def find_argument(self,data,argument,line_num, function):
        #print(line_num)
        _ = data.loc[(data.result == argument )& (data.functions == function)]
        potential_lines = [x for x in _.index.to_list() if x < line_num]
        potential_lines.sort()
        #if len(potential_lines) == 0:
        
    def find_argument2(self,data,argument,line_num, function):
        _ = data.loc[(data.result == argument )& (data.functions == function)]
        potential_lines = [x for x in _.index.to_list() if x < line_num]
        potential_lines.sort()
        if len(potential_lines) == 0:
            return None
        else: return potential_lines[-1]
    
    def take_application_index(self,function,data):
        original_id  = function.name
        fname = function['name']
        index_of_occur = []
        index_to_exclude = []
        for i,row in data.iterrows():
                if row['kind'] == 'def' and row['name'] == fname and i > original_id:
                    omitted  = self.take_application_index(data.iloc[i],data)
                    index_to_exclude =  index_to_exclude + omitted
                    index_to_exclude.append(i)
                if function.functions in row.functions and row['name'] == fname and i >= original_id:
                    index_of_occur.append(i)
        return [x for x in index_of_occur if  x  not in index_to_exclude]
        
    def rename_function(self,data,function_path,fname,name,i=0):
        index_of_occur = []
        # #check if class
        # class_flag = False
        # temp = function_path +'.' + fname
        
        func = data.loc[(data['name'] == fname) & (data.kind =='def') & (data.functions == function_path)].iloc[i]
        index_of_occur = self.take_application_index(func,data)
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
            if data.iloc[i].arguments is not None:
                for arg in data.iloc[i].arguments:
                    if not arg.isnumeric() and "'" not in arg and '"' not in arg:
                        _ = self.find_argument2(data,arg,i,f)
                        if _ is not None:
                            prereq = prereq + [_]
                        
        
        prereq = pd.unique(prereq).tolist()
        prereq = [x for x in prereq if x in range(box[0],box[1])]
        return prereq
    
    def make_function(self,data,start_line,end_line,name):
        if data.iloc[start_line].level_num != data.iloc[end_line + 1].level_num or data.iloc[start_line].functions != data.iloc[end_line + 1].functions:
            return False
        returns = self.take_prerequesits_from_box(data,(start_line,end_line))
        arguments = self.take_arguments_from_box(data,(start_line,end_line))
        replace = "'"
        if len(arguments) != 0:
            arguments = data.iloc[arguments].result.to_list()
            def_string = f"def {name}({str(arguments)[1:-1].replace(replace,'')}):"
            func_str = f"{name}({str(arguments)[1:-1].replace(replace,'')})"
        else:
            def_string = f"def {name}():"
            func_str = f"{name}()"
        returns = data.iloc[returns].result.to_list()
        if len(returns) == 0:
            pass
        
        
        start_index = data.loc[data.functions == data.iloc[start_line].functions].index.to_list()[0]
        
        start_level = data.iloc[start_line].level_num
        fun ={start_index: [def_string,start_level]} 
        
        start_index_backup = start_index 
        
        
        for i in range(start_line,end_line):
            start_index +=1
            fun[start_index] = [data.iloc[i].line_text,start_level +1]
        
        if len(returns) != 0:
            start_index +=1
            fun[start_index] = [f"return {str(returns)[1:-1].replace(replace,'')}",start_level+1]
            func_str = f"{str(returns)[1:-1].replace(replace,'')} = " +func_str
            
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
    
    