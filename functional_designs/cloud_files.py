"""
Map files to users
each users in admin 
delete files and users 
backup files of a user and allow restore 

"""
from typing import Optional

# first map files to owners
# then map users to groups 
# then allow removal of files 
# backup and restore files of user 

class Cloud:
    
    def __init__(self):
        self.files = {}
        
    def add_file(self, new_file: str, user: str) -> None:
        
        self.files[new_file] = user
        
    def get_user(self, target_file: str) -> Optional[str]:
        if not target_file: 
            return None 
        
        
        



def main():
    
    
    pass


if __name__ == "__main__":
    main()