import os

class Parser():
    def __init__(self) -> None:
        pass    
    def _to_notation():
        pass
    def build_tree(path_to_script:str):
        if not os.path.exists(path_to_script):
            return False,"Path doesn not exist"
        if not path_to_script.split('.')[-1] == 'py':
            return False, "It need to be python script"
        if 