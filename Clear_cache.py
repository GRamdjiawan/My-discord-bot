import os
class Clear_cache():
    def __init__(self):
        full_path_name = os.path.dirname(os.path.realpath(__file__))
        print(full_path_name)
        path_name = full_path_name+"\__pycache__" 
        print(path_name)
        if os.listdir(path_name):
            for file in os.listdir(path_name):
                os.remove(path_name+"\\"+file)
            os.rmdir(path_name)
        else:
            print("not found")