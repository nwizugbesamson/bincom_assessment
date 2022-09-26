import os
import pathlib
import random
import dotenv
import psycopg2 as pg
from psycopg2.extensions import AsIs

DOT_ENV_PATH = pathlib.Path() / '.env'
if DOT_ENV_PATH.exists():
    dotenv.load_dotenv(dotenv_path=str(DOT_ENV_PATH))

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')


## Dictionary containing provided data
colours_per_week: dict = {
                    'monday': [	'GREEN', 'YELLOW', 'GREEN', 'BROWN', 
                                'BLUE', 'PINK', 'BLUE', 'YELLOW', 
                                'ORANGE', 'CREAM', 'ORANGE', 'RED', 
                                'WHITE', 'BLUE', 'WHITE', 'BLUE', 
                                'BLUE', 'BLUE', 'GREEN'],

                    'tuesday': ['ARSH', 'BROWN', 'GREEN', 'BROWN', 
                                'BLUE', 'BLUE', 'BLUE', 'PINK', 'PINK', 
                                'ORANGE', 'ORANGE', 'RED', 'WHITE', 
                                'BLUE', 'WHITE', 'WHITE', 'BLUE', 'BLUE', 
                                'BLUE'],
                    'wednesday': ['GREEN', 'YELLOW', 'GREEN', 'BROWN', 
                                  'BLUE', 'PINK', 'RED', 'YELLOW', 
                                  'ORANGE', 'RED', 'ORANGE', 'RED', 
                                  'BLUE', 'BLUE', 'WHITE', 'BLUE', 
                                  'BLUE', 'WHITE', 'WHITE'],
                    'thursday': ['BLUE', 'BLUE', 'GREEN', 'WHITE', 
                                 'BLUE', 'BROWN', 'PINK', 'YELLOW', 
                                 'ORANGE', 'CREAM', 'ORANGE', 'RED', 
                                 'WHITE', 'BLUE', 'WHITE', 'BLUE', 
                                 'BLUE', 'BLUE', 'GREEN'],
                    'friday': ['GREEN', 'WHITE', 'GREEN', 'BROWN', 
                                'BLUE', 'BLUE', 'BLACK', 'WHITE', 
                                'ORANGE', 'RED', 'RED', 'RED', 'WHITE', 
                                'BLUE', 'WHITE', 'BLUE', 'BLUE', 'BLUE', 'WHITE']
}


def colour_count(data:dict[str, list]) -> dict[str, int]:
    """return colour frequency count

    Args:
        data (dict[str, list]): weekdays and colours obsevered per day

    Returns:
        dict[str, int]: count of colours observed within week
    """
    colour_count: dict = {}
    for day in data:
        for colour in day:
            if colour not in colour_count:
                colour_count[colour] = 1
            colour_count[colour] += 1
    return colour_count

processed_data = colour_count(colours_per_week)

## 1. Which color of shirt is the mean color?
## Data is categorical and has no mean value as mean is the average of the distribution of values in a continous or discrete norminal data

## 2. Which color is mostly worn throughout the week?
def max_colour(colour_dict: dict[str, list]) -> str:
    """return colour with highest frequency
       
       Args:
        colour_dict (dict[str, list]) : office colours by day worn

       Returns:
            max_colour (str): colour with max frequency
    """
    
    max_colour = max(sorted(colour_dict.items(), key=lambda x: x[1]))
    return max_colour


frequent_colour = max_colour(processed_data)

## 3. Which color is the median?
## the data is categorical and cannot be sorted, hence it does not contain a median value


## 4. BONUS Get the variance of the colors
## variance is the deviation of data distribution from its mean, the data does not have a mean value and also does not have a variance

## 5. BONUS if a colour is chosen at random, what is the probability that the color is red?
def probability(colour_dict: dict[str, list], colour: str) -> str:
    """return the probability in percentage of picking given colour from data

    Args:
        colour_dict (dict[str, list]): _description_
        colour (str): colour to calculate probability for 

    Returns:
        str: probability of picking given colour in percentage
    """
    probability = (colour_dict['RED'] / sum(colour_dict.values())) * 100
    return f'the probability of picking {colour} is {probability:.2f}%'

red_probability = probability(processed_data, 'RED')

## Save the colours and their frequencies in postgresql database
def connect_pg( func):
    """Decorator function,
       create connection to database for query execution
       pass cursor into function
    """
    def inner_function(*args):
        conn = pg.connect(user=POSTGRES_USER, 
                          password=POSTGRES_PASSWORD, 
                          host=POSTGRES_HOST, 
                          port=POSTGRES_PORT, 
                          database=POSTGRES_DB )
        cursor = conn.cursor()
        func(*(args), _cursor=cursor)
        conn.commit()
        conn.close()
    return inner_function


@connect_pg
def create_table( _cursor: pg.cursor) -> None:
    _cursor.execute(
        """CREATE TABLE IF NOT EXISTS colour_frequency(
            colour VARCHAR(30),
            frequency DECIMAL(4, 0)
        
        )""")


@connect_pg
def insert_values(data: dict[str, int], _cursor: pg.cursor) -> None:
    for key, item in data.items():
        insert_value = (key, item)
        query = "INSERT INTO colour_frequency(colour, frequency) VALUES (%s, %s)"
        _cursor.execute(query, insert_value)


create_table()

insert_values(processed_data)


##  BONUS write a recursive searching algorithm to search for a number entered by user in a list of numbers.
def recursive_search(array: list[int], lower_bound: int, higher_bound: int, target: int):
    """search for integer in array of integers recursively

    Args:
        array (list[int]): input array
        lower_bound (int): min value of array
        higher_bound (int):max value of array
        target (int): target value

    Returns:
        int: index of target in array or -1 if not found
    """
    ## check array lenght is greater than 1
    if higher_bound >= lower_bound:
        ## base case
        mid = (higher_bound + lower_bound) // 2
        if array[mid] == target:
            return mid

        ## general recursive search
        elif array[mid] > target:
            return recursive_search(array, lower_bound, mid - 1, target)
 
        
        else:
            return recursive_search(array, mid + 1, higher_bound, target)
 
    else:
        return -1


## Write a program that generates random 4 digits number of 0s and 1s and convert the generated number to base 10.
binary_choice = int(''.join([random.choice([0, 1]) for _ in range (4)]), base=2)



## Write a program to sum the first 50 fibonacci sequence
def fibonacci(num):
    """return the fibonacci of given number
       implemented using for loop

    Args:
        num (int): fibonacci index to return

    Returns:
        int: fibonacci number
    """
    if num <= 0:
        return 'number must be greater than zero'
    if num == 1:
        return num
    first_num, second_num = 1, 1
    for _ in range(num - 1):
        first_num, second_num = second_num, first_num + second_num
    return first_num


fib_50_sum = sum([fibonacci(num) for num in range(1, 51)])
