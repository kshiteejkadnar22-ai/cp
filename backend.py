import random
import csv


# asep titles from csv
def load_asep_project_titles(filename="asep_project.csv"):
    try:
        with open(filename,"r") as file:
            reader = csv.reader(file)
            return [row[0] for row in reader if row] 
    except FileNotFoundError:
        print("Error: 'asep_project.csv' file not found!")    
        return []
    
# module 1 psp titles from csv
def load_psp_cp_titles(filename="psp_cp.csv"):
    try: 
        with open(filename,"r") as file:
            reader=csv.reader(file)
            return [row[0] for row in reader if row]
    except FileNotFoundError:
        print("Error: 'psp_cp.csv' file not found!")
        return []
    
# module 1 wd titles from csv
def load_wd_cp_titles(filename="wd_cp.csv"):
    try:
        with open(filename,"r") as file:
            reader = csv.reader(file) 
            return [row[0] for row in reader if row] 
    except FileNotFoundError:
        print("Error: 'wd_cp.csv' file not found!")
        return []
    
# module 2 da titles from csv
def load_da_cp_titles(filename="da_cp.csv"):
    try:
        with open(filename,"r") as file:
            reader=csv.reader(file)
            return [row[0] for row in reader if row]
    except FileNotFoundError:
        print("Error: 'da_cp.csv' file not found!")
        return []
    
# module 2 pfe titles from csv
def load_pfe_cp_titles(filename="pfe_cp.csv"):
    try:
        with open(filename,"r") as file:
            reader=csv.reader(file)
            return [row[0] for row in reader if row]
    except FileNotFoundError:
        print("Error: 'pfe_cp.csv' file not found!")
        return []
    
# module 2 aem titles from csv
def load_aem_cp_titles(filename="aem_cp.csv"):
    try:
        with open(filename,"r") as file:
            reader=csv.reader(file)
            return [row[0] for row in reader if row]
    except FileNotFoundError:
        print("Error: 'aem_cp.csv' file not found!")
        return [] 
    

# generating random    
def show_random_ideas(project_list, count=5):
    if not project_list:
        print("\nNo project ideas available!")
        return
    
    # only selecting 5
    count=min(count,len(project_list))
    selected = random.sample(project_list, count)

    print("Here are some suggested project ideas:")
    for i, idea in enumerate(selected, start=1):
        print(i,idea)
    print()  

    

# main program
def main():
    print("=====================================")
    print("         PROJECT IDEA GENERATOR      ")
    print("=====================================")

    print("Select type of project titles you want:")
    print("1. ASEP Project Titles")
    print("2. Course Project Titles")
    project_type = input("Enter your choice (1 or 2): ").strip()
    print("-------------------------------------")

    # asep
    if project_type=="1":
        print("You selected ASEP Project Titles")
        print()
        asep_project=load_asep_project_titles()
        show_random_ideas(asep_project,count=5)

    # module
    elif project_type=="2":
        print("You selected Course Project Titles")
        print("Select your module \n 1. Module 1 \n 2. Module 2")
        project_type=input("Enter your choice (1 or 2): ").strip()

        print("-------------------------------------")

        # module 1
        if project_type=="1":
            print("You selected Module 1")
            print("Select your subject \n 1. Problem Solving & Programming (PSP) \n 2. Web Development")
            project_type=input("Enter your choice (1 or 2): ").strip()

            print("-------------------------------------")

            if project_type=="1":
                print("You selected Course Project Titles for Problem Solving & Programming (PSP)")
                print()
                psp_cp=load_psp_cp_titles()
                show_random_ideas(psp_cp,count=5)

            elif project_type=="2":
                print("You selected Course Project Titles for Web Development")
                print()
                wd_cp=load_wd_cp_titles()
                show_random_ideas(wd_cp,count=5)

            else:
                print("Enter valid choice")

        # module 2
        elif project_type=="2":
            print("You selected Module 2")
            print("Select your subject \n 1. Data Analysis (DA) \n 2. Python for Engineers (PFE) \n 3. Applied Electromechanics (AEM)")
            project_type=input("Enter your choice (1 or 2 or 3): ").strip()

            print("-------------------------------------")

            if project_type=="1":
                print("You selected Course Project Titles for Data Analysis (DA)")
                print()
                da_cp=load_da_cp_titles()
                show_random_ideas(da_cp,count=5)

            elif project_type=="2":
                print("You selected Course Project Titles for Python for Engineers (PFE)")
                print()
                pfe_cp=load_pfe_cp_titles()
                show_random_ideas(pfe_cp,count=5)

            elif project_type=="3":
                print("You selected Course Project Titles for Applied Electromechanics (AEM)")
                print()
                aem_cp=load_aem_cp_titles()
                show_random_ideas(aem_cp,count=5)

            else:
                print("Enter valid choice")

    else:
        print("Enter valid choice")



# running program
if __name__ == "__main__":
    main()

