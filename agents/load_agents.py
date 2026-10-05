import importlib
import inspect
import os
from .agent import Agent

def load_agents():
    agents = []

    agents_directory = os.path.dirname(__file__)

    for file in os.listdir(agents_directory):
        if file in {"agent.py", "load_agents.py", "__init__.py"}:
            continue

        if not file.endswith(".py"):
            continue

        module_name = f"agents.{file[:-3]}"
        module = importlib.import_module(module_name)

        for _, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, Agent) and cls is not Agent:
                agents.append(cls)
                break

    return agents