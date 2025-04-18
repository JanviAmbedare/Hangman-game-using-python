import sys
import time


celebration_boy = ["""

         O   
       _/|\_
        / \ 
                ""","""

      ___O___   
         |
        / \ 
                ""","""

      \__O__/   
         |
        / \ 
                ""","""
              
     ..     ..
      \__O__/   
         |
        / \ 
                ""","""
    ...     ...          
     ..     ..
      \__O__/   
         |
        / \ 
                """]


########## FOR DEMO ################
if __name__ == "__main__":
    for i in range(5):
        print(celebration_boy[i])
        time.sleep(1)
        print("\033c")
        # console_clear = "\033[H\033[J"
        # time.sleep(1)
        # print(console_clear)