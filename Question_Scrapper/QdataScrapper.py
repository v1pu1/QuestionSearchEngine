# Import required packages
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

# Set up Selenium webdriver
# Define the webdriver service
s = Service('geckodriver.exe')

# Intantiate the webdriver
driver = webdriver.Firefox(service=s)

# check heading_class is present or not first by document.querySelector("");, leetcode page's heading and body class changes day by day

HEADING_CLASS = ".mr-2.text-label-1"
BODY_CLASS = ".px-5.pt-4"
# path to "./Qdata" -> current folder ke andar Qdata
QDATA_FOLDER = "Qdata"

# To read links from a text file and store it as a python List object
def get_problem_links():
    links = [] # List to store the links 
    # Open the file
    with open("lc1.txt", "r") as file:
        # Read each line and append it to the "links" list
        for line in file:
            links.append(line)
    return links        

"""
"os.path.join()" is used to construct a valid path by joining individual path components together.

Here's how os.path.join() works:

1. It takes the first path component as the base directory or path segment.
2. It iteratively appends the remaining components to the base path, separated by the appropriate path separator based on the underlying operating system.
3. It constructs the final path by joining all the components together.

Using os.path.join() helps ensure that your code is portable and works correctly across different platforms. It handles the differences in path separators automatically, making your code more robust and less prone to errors when working with file and directory paths.
"""

# add problem number(acc. to leetcode) & name to "index.txt" in (QDATA_FOLDER = Qdata) folder
def add_problem_name_to_index_file(text):
    """
    It constructs the path to the index file by joining the QDATA_FOLDER variable (which holds the path to a directory) with the filename "index.txt" using the os.path.join() function.
    """
    file_path = os.path.join(QDATA_FOLDER, "index.txt")
    # Write the problem text to the file created at "/{QDATA_FOLDER}/Qindex.txt"
    with open(file_path, "a") as index_file:
        index_file.write(text + "\n")

# add problem link to "Qindex.txt" in (QDATA_FOLDER = Qdata) folder
def add_problem_link_to_Qindex_file(text):
    """
    It constructs the path to the index file by joining the QDATA_FOLDER variable (which holds the path to a directory) with the filename "Qindex.txt" using the os.path.join() function.
    """
    file_path = os.path.join(QDATA_FOLDER, "Qindex.txt")
    # Write the problem text to the file created at "/{QDATA_FOLDER}/Qindex.txt"
    with open(file_path, "a", encoding="utf-8", errors="ignore") as Qindex_file:
        Qindex_file.write(text) # No need for "\n" because while reading links from file "\n" already appended in each of the line of links file

def create_file_and_add_problem_text_to_file(file_name, text):
    """
    It constructs the path to the index file by joining the QDATA_FOLDER variable (which holds the path to a directory) with the filename "file_name" using the os.path.join() function.
    """
    folder_path = os.path.join(QDATA_FOLDER, file_name)
    #Create a new folder at "folder_path"
    os.makedirs(folder_path, exist_ok=True)
    """
    It constructs the path to the index file by joining the "folder_path" (which holds the path) with the filename "file_name.txt" using the os.path.join() function.
    """
    file_path = os.path.join(folder_path, file_name+".txt")
    # Write the problem text to the file created at "/{QDATA_FOLDER}/file_name/file_name.txt"
    with open(file_path, "w", encoding="utf-8", errors="ignore") as new_file:
        new_file.write(text)


def getPagaData(link, index):
    # we use try...except -> Some questions are leetcode premium and their page can't be loaded 
    try:
        # Load the URL in the chrome browser
        driver.get(link)
        # Wait until a certain condition is met or for max 10sec. Condition -> certain element gets loaded
        WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, BODY_CLASS)))
        time.sleep(1)
        # https://chat.openai.com/share/f420bfcc-109c-4504-a23d-1631d84e0169

        # Get heading and body elements
        heading = driver.find_element(By.CSS_SELECTOR, HEADING_CLASS)
        body = driver.find_element(By.CSS_SELECTOR, BODY_CLASS)

        print("Scraping :: " + heading.text)
        if (heading.text):
            add_problem_name_to_index_file(heading.text)
            add_problem_link_to_Qindex_file(link)
            create_file_and_add_problem_text_to_file(str(index), body.text)
        time.sleep(1)
        return True
    # If the question link is Leetcode Premium then do nothing and print 
    except Exception as e:
        print("This link : " + str(link) + " is of Leetcode Premium question !!! SKIPPING !!!")
        return False

# Initially index is 1 for first problem 
index = 1
# Get list of all problem links
links = get_problem_links()
# For each link 
for link in links:
    # Get the problem heading and body + index
    success = getPagaData(link, index)
    #if question is not leetcode premium then success = true
    if (success):
        index = index+1


driver.quit()