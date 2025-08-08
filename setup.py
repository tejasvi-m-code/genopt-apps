from setuptools import find_packages, setup
from typing import List

def get_requirements()-> List[str]:
    """
    
    This function will return list of requirements
    
    """

    requirement_lst:List[str] =[]
    try:
        with open('requirements.txt','r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirem
ent and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
setup(
    name ="web app",
    version ="0.0.1",    author ="Tejasvi Manoj",
    author_email = "manoj.tejasvi@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)
