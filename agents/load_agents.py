import importlib
import os

def load_agents():
    
    agents = []
    
    for file in os.listdir(os.path.dirname(__file__)):
        
        if file.startswith("student_") and file.endswith(".py"):
            
            module_name = f"agents.{file[:-3]}"
            module = importlib.import_module(module_name)
            class_name = file[8:-3] 
            cls = getattr(module, class_name)
            agents.append(cls) 
            
    return agents # returns classes which starts with "student_" and ends with ".py"
