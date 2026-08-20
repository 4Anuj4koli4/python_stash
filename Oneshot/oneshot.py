print("Hello, World!")

x: int = 34
y: float = 3.14
str1: str = "Hello"
bool1: bool = True

print("My name is", str1, "and I am", x, "years old.")
print(f"My name is {str1} and I am {x} years old.")




#Constant name

MAX_AGE: int = 100
PI: float = 3.14159

print(f"{str1} is active {bool1} and pi value is {PI}.")




# string manipulation

name: str = "JOhN DOe"

print(f"Original name: {name}")
print(f"Uppercase: {name.upper()}")
print(f"Lowercase: {name.lower()}")
print(f"Titlecase: {name.title()}")
print(f"Swapcase: {name.swapcase()}")
print(f"Capitalize: {name.capitalize()}")
print(f"Length of name: {len(name)}")
print(f"Replacing 'JOhN' with 'Jane': {name.replace('JOhN', 'Jane')}")
print(f"Finding 'DOe' in name: {name.find('DOe')}")
print(f"Counting occurrences of 'o' in name: {name.count('O')}")




#Cut or slice strings

print(f"First 4 characters: {name[:4]}")
print(f"Last 3 characters: {name[-3:]}")
print(f"Characters from index 2 to 5 / cut from index 2 to 5: {name[2:6]}")

first_name: str = "Mary"
last_name: str = "Smith"

print(f"{first_name} {last_name}")
print(first_name * 5)




# Operators - Arithmetic, Comparison, Logical

a: int = 10
b: int = 3

print(f"Addition: {a + b}")
print(f"Subtraction: {a - b}")
print(f"Multiplication: {a * b}")
print(f"Division: {a / b}")
print(f"Modulus: {a % b}") # Remainder of a divided by b
print(f"Exponentiation: {a ** b}") # a raised to the power of b
print(f"Floor Division: {a // b}") # rounded down to the nearest integer of a/b


print(f"Is a greater than b? {a > b}")
print(f"Is a less than b? {a < b}")
print(f"Is a equal to b? {a == b}")
print(f"Is a not equal to b? {a != b}")
print(f"Is a greater than or equal to b? {a >= b}")
print(f"Is a less than or equal to b? {a <= b}")

print(f"a and b: {a and b}")
print(f"a or b: {a or b}")
print(f"not a: {not a}")




# input and type conversion

user_first_name: str = input("Enter your first name: ").lower()
user_age: int = int(input("Enter your age: "))

print(f"Hello, {user_first_name}! You are {user_age} years old.")





# if/else/elif statements

temp = int(input("Enter the temperature in Celsius: "))
print(f"The temperature is {temp}°C.")

if temp > 30:
    print("It's a hot day.")
elif temp > 20:
    print("It's a nice day.")
elif temp > 10:
    print("It's a bit chilly.")
else:
    print("It's cold outside.")


score = int(input("Enter your score (0-100): "))

if score >= 90:
    grade = "A"
    msg = "Excellent!"
elif score >= 80:
    grade = "B"
    msg = "Good job!"
elif score >= 70:
    grade = "C"
    msg = "You passed."
else:
    grade = "F"
    msg = "Better luck next time."

print(f"Your score is {score}. Your grade is {grade}. {msg}")


driver_age: int = 25
has_license: bool = True
has_insurance: bool = False

if driver_age >= 18 and has_license:
    print("Yes they have a license and are old enough to drive.")

if driver_age >= 50 or has_insurance:
    print("Yes they are either 50 or older, or they have insurance.")

print(f"my age is {driver_age}")




#LISTS AND TUPLES - DATA STRUCTURES

#Lists : ordered, mutable, allows duplicates   [] brackets
#Tuples : ordered, immutable, allows duplicates  () brackets

#lists

languages: list[str] = ["Python", "Java", "C++", "JavaScript"]
numbers: list[int] = [1, 2, 3, 4, 5]
mixed_list: list = ["Python", 3.14, True, 42]

print(f"Languages: {languages}")
print(f"Numbers: {numbers}")
print(f"Mixed List: {mixed_list}")


print(f"First language: {languages[0]}")
print(f"Last language: {languages[-1]}")

print(f"First 2 Languages {languages[:2]}")
print(f"Last 2 Languages {languages[-2:]}")
print(f"Languages from index 1 to 3: {languages[1:4]}")

print(f"Length of languages list: {len(languages)}")

# modify list
numbers[2] = 10
numbers.append(6)
numbers.remove(4)
numbers.append(100)
numbers.insert(2, 50)  # Insert 50 at index 2
numbers.sort()  # Sort the list in ascending order
numbers.reverse()  # Reverse the list
numbers.pop()  # Remove the last element
print(f"Modified Numbers: {numbers}")


#Tuples

coordinates: tuple[int, int] = (10, 20)
print(f"Coordinates: {coordinates}")

color: tuple[int, int, int] = (255, 0, 0)  # RED RGB
print(f"Color: {color[0]}")
print(f"Color: {color.count(0)}") # Count how many times 0 appears in the tuple
print(f"Color: {color.index(0)}") # Find the index of the first occurrence of 0 in the tuple


#matrix - 2d lists

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]     #nested list
print(f"Matrix: {matrix[1][1]}")

students = [("John", 20), ("Jane", 22), ("Mike", 19)]  # list of tuples
print(f"students : {students}")
print(f"students : {students[0]}")
print(f"students : {students[0][0]}")  # Accessing the first student's name




# Loops - Repeat a block of code multiple times - Control flow

for i in range(1, 6):
    print(f"Number: {i}")

for i in range(1, 6):
    print(f"Number: {i}", end=" ")  # Print on the same line with space
print()

fruits = ["Apple", "Banana", "Cherry", "Date"]
for fruit in fruits:
    print(f"- {fruit}")


for i, fruit in enumerate(fruits):  # enumerate() returns both the index and the value of each item in the list
    print(f"{i}. {fruit}")

for i in range(1, 3):
    for j in range(1, 3):
        print(f"{i} x {j} = {i*j}")




# while loop

print("Countdown from 5:")
i = 5
while i > 0:
    print(f"Number: {i}")
    i -= 1

print("Countdown finished!")


lottery_number = 7
guess = 6
attempts = 0

while guess != lottery_number and attempts < 3:
    attempts += 1
    print(f"Attempt {attempts}: Guessing: {guess}")

    if guess < lottery_number:
        print("Too low! Try again.")
    else:
        print("Too high! Try again.")
    guess += 1  # Increment guess for the next attempt

if guess == lottery_number:
    print(f"Congratulations! You guessed the lottery number {lottery_number} in {attempts} attempts.")




#Dictionaries and Sets - Data Structures

#Dictionaries - unordered, mutable, key-value pairs   {} Brackets   ---   {key : Values}
#sets - unordered, mutable, unique elements     {} Brackets


# dictionary
person = {"name": "John",
          "age": 30,
          "city": "New York"}

#add or edit key-value pair
person["age"] = 31  # Update age
person["country"] = "USA"  # Add new key-value pair
del person["city"]  # Remove key-value pair by key

print(f"Person: {person}")
print(f"Name: {person['name']}")
print(f"Age: {person['age']}")
print(f"Country: {person['country']}")

Keys = person.keys()  # Get all keys list
Values = person.values()  # Get all values list

print(f"Keys: {Keys}, Values: {Values}") #returns list of keys and values in the dictionary

items = person.items()  # Get all key-value pairs as tuples
print(f"Items: {items}")  # returns list of tuples of key-value pairs in the dictionary


for key, value in person.items():
    print(f"{key}: {value}")  # Print each key-value pair in the dictionary

for key in person:
    print(f"{key}")

print(person)




# Sets
numbers_set = {1, 2, 3, 4, 5}
colors_set = {"red", "green", "blue"}


numbers_set.add(6)  # Add an element to the set
numbers_set.remove(3)  # Remove an element from the set
numbers_set.discard(10)  # Remove an element if it exists, otherwise do nothing
numbers_set.update([7, 8, 9])  # Add multiple elements to the set
numbers_set.pop()  # Remove and return an arbitrary element from the set
# numbers_set.clear()  # Remove all elements from the set

print(f"Numbers Set: {numbers_set}")
print(f"Colors Set: {colors_set}")


numbers1 = {1, 2, 3, 4, 5}
numbers2 = {4, 5, 6, 7, 8}

merge = numbers1.union(numbers2)  # Merge two sets
same = numbers1.intersection(numbers2)  # Find common elements in two sets
diff = numbers1.difference(numbers2)  # Find elements in numbers1 but not in numbers2

print(f"Merged Set: {merge}")
print(f"Common Elements: {same}")
print(f"Difference: {diff}")




# Functions - Reusable blocks of code
# functions help organize code and avoid repetition

def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))  # Call the function

def add(a, b):   # dont need to specify the type of a and b
    return a + b

c = add(5, 3)
print(c)


# kwargs - keyword arguments
# args - positional arguments
def variable_arguments(*args, **kwargs):
    print("Positional arguments:", args)
    print("Keyword arguments:", kwargs)

args_kwargs_result = variable_arguments(1, 2, 3, name="Alice", age=30)  # Call the function with variable arguments


count = 10

def calculate_area(length):
    global count  # Access the global variable 'count'

    area = length * count
    count += 20   # cant modify the global variable without declaring it as global
    print(count)
    return area

calculate_area(5)  # Call the function with a length of 5




# Error Handling - dealing with exceptions and errors in code
# try/except blocks are used to catch and handle exceptions

try:
    result = 10 / 0
    print(result)
except ZeroDivisionError:                             # if error is known, we can specify the error type
    print("Error: Division by zero is not allowed.")
except Exception as e:                                 # if error is unknown, we can use Exception as e to catch any exception and print the error message
    print(f"Error: {e}")
finally:                                               # finally block is always executed, regardless of whether an exception occurred or not
    print("Execution completed.")