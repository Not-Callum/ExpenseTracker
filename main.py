import sqlite3
from datetime import datetime

#connecting to database, for some reason my database was not being placed in the right directory so excuse the file path
con = sqlite3.connect("C:/Users/Owner/Desktop/JavaScript Src/JustITCourse/PYTHON/ExpenseTracker/Expense.db")
cur = con.cursor()

#creating a table, I wanted a primary key, and a cost that could not be null, but the category can be null but defaults to unknown if not given. Date is defaulted at inserting data in python.

def CreateExpenseTable():
  cur.execute('''CREATE TABLE IF NOT EXISTS expenses(expenseID INTEGER PRIMARY KEY AUTOINCREMENT, expenseName TEXT NOT NULL,cost DECIMAL(5,2) NOT NULL, category TEXT DEFAULT 'Unknown', date DATE)''')
 
#CreateExpenseTable()

#this will always insert if there is a name and a cost, however there are optional arguments. This will only really accept the first of those arguments but I figured, we may not always have a category.
def CreateExpense(name, cost, *args):
  #checking for arguments, because the insert queries are different and must discern whether the optional category argument is present.
  if args:
    cur.execute('''INSERT INTO expenses(expenseName, cost, category, date)
    VALUES(?, ?, ?, ?)
    ''', (name, cost,args[0], datetime.today().strftime('%Y-%m-%d')))
  else:
    cur.execute('''INSERT INTO expenses(expenseName, cost, date)
    VALUES(?, ?, ?)
    ''', (name, cost, datetime.today().strftime('%Y-%m-%d')))
  con.commit()




#self explanatory, but just looping through all results in the table
def ReadAllExpenses():
  cur.execute("SELECT * FROM expenses")
  expenses = cur.fetchall()
  for expense in expenses:
    print(expense)

#ReadAllExpenses()


#this is for the future, where the user input can choose from these outputs rather than having to manually input it every time. I will however have to give the option of creating new categories or simply not inputting a category.
def GetAllCategories():
  listOfCategories = []
  cur.execute("SELECT DISTINCT category FROM expenses")
  category = cur.fetchall()
  for cat in category:
    listOfCategories.append(cat)
  return listOfCategories

#These are all quite self explanatory
def GetTotalAmount():
  cur.execute("SELECT SUM(cost) FROM expenses")
  costs = cur.fetchall()
  return costs

def GetCategoryTotalAmount(category):
  cur.execute("SELECT SUM(cost) FROM expenses WHERE category = ?", (category,))
  costs = cur.fetchall()
  return costs

def DeleteExpense(expenseID):
  cur.execute("DELETE FROM expenses WHERE expenseID = ?", (expenseID,))
  con.commit()

def GetExpenseFromID(expenseID):
  cur.execute("SELECT * FROM expenses WHERE expenseID = ?", (expenseID,))
  expenseMatch = cur.fetchall()
  for expense in expenseMatch:
    return(expense)


# START OF HANDLING FUNCTIONS 

#These orginally were in the main loop part of this program, but the indentation was ugly so they've been moved here and put into neat little functions! :)

def handleCreatNewExpense():
  #Dynamically creating a new expense.
      expenseName = str(input("What would you like to call the expense?"))
      expenseCost = float(input("How much did it cost?"))
      index = 0
      categoryList = []
      #loop through all results and give an index value to show the user what they are selecting.
      for category in GetAllCategories():
        #because the select query returns tuples, you must index the result to get the string value of the select query
        categoryList.append(category[0])
        index += 1
        print(f"{index}. {category[0]}")

      #extra option to create a new category for this expense.
      lastOption = len(categoryList) + 1
      print(f"{lastOption}. Create a new category?")
      categoryChoice = int(input("Please choose the index number of the category you'd like to use?"))
      
      if categoryChoice == lastOption:
        newCategory = input("What would you like to call this category?")
        try:
          CreateExpense(expenseName, expenseCost, newCategory)
          print("Success!")
        except Exception as e:
          print(f"Error!: {e}")
      else:
        try:
          #must make sure to -1 to account for 0 indexing.
          CreateExpense(expenseName, expenseCost, str(categoryList[categoryChoice - 1]))
          print("Success! New expense created!")
        except Exception as e:
          print(f"Error!: {e}")


def handleExpenseDeletion():
  idDeleteInput = input("Which one of these do you wish to delete? (input the ID, the first number) ")
  try:
    print(GetExpenseFromID(idDeleteInput))
  except Exception as e:
    print(f"Error: {e}")
    return
  YesOrNo = input("Is this the one you wish to delete? Type Y for yes and N for no: ")
  if YesOrNo == "Y":
    try:
      DeleteExpense(idDeleteInput)
      print("Successful deletion!")
    except Exception as e:
      print(f"Error: {e}")
  else:
    print("Cancelled!")



def handleExpenseDetails():
  #give option for viewing spending per category or getting total spent ever
  viewingInput = input("Would you like to: 1 - View the total spent in a category, 2 - View the total spent ever: ")
  match viewingInput:
    case "1":
      for category in GetAllCategories():
        print(category)
      categoryView = input("Which category would you like to view the sum of?")
      try:
        print(GetCategoryTotalAmount(categoryView))
      except Exception as e:
        print(f"Error: {e}")


    case "2":
      try:
        total = GetTotalAmount()
        print(f"Your total is {total}")
      except Exception as e:
        print(f"Error: {e}")


# START OF THE MAIN PROGRAM LOOP
active = True
print("Hello! Welcome to the expense tracker. What would you like to do today?")

while active == True:
  userinput = input("Would you like to: 1 - View your expenses, 2- Create a new expense, 3 - Delete an expense?, 4- View details about your expenses?, 5 - Quit the program? (type the number associated with each option)")

  #matching the user's input to decide what to do.

  match userinput:
    case "1":
      print("Here are your expense results!")
      ReadAllExpenses()
      print("------------------------------------------------------------------------------------------")
      continue

    case "2":
      handleCreatNewExpense()
      continue

    case "3":
      #because this task requires an ID, may as well show all the IDs, could make it searchable using a LIKE in the query instead and select it that way but alas.
      ReadAllExpenses()
      handleExpenseDeletion()
        
      continue
    case "4":
      handleExpenseDetails()
      continue
    case "5":
      print("Goodbye! Thanks for using the program!")
      break


con.close()