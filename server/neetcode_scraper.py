from bs4 import BeautifulSoup
from main import conn 
import requests
import json

base_problem_url = "https://github.com/neetcode-gh/leetcode/blob/main/python/"
problem_list_url = "https://github.com/neetcode-gh/leetcode/tree/main/python"

html = requests.get("https://github.com/neetcode-gh/leetcode/tree/main/python")
soup = BeautifulSoup(html.content, 'html.parser')

class ProblemItem:
  def __init__(self, name, number):
    self.name = name
    self.number = number

def sanitize_name(name):
  name = name.split("-")[1:] # Gets rid of the problem number
  remove_file_extension = name[-1].split(".")[0]
  name[-1] = remove_file_extension
  return "-".join(name)

def find_all_problems():
  """
  Use BeautifulSoup to scrape the github site for all of the problems.
  """
  seen_numbers = [False] * 2500 
  items = json.loads(soup.get_text())['payload']['tree']['items']
  for it in items:
    problem_number = int(it["name"][:4])
    print(problem_number)
    if seen_numbers[problem_number]: 
      continue
    item = ProblemItem(name=it["name"], number=problem_number)
    seen_numbers[problem_number] = True  # Error handling when people mess up submissions on Neetcode Github.
    yield item 

def find_solution(solution: BeautifulSoup):
  """
  Parse the solution from the github page.
  """
  solution_text = "\n".join(json.loads(solution.get_text())["payload"]["blob"]["rawLines"])
  return solution_text

prepared = 'INSERT into problems(number, name, solution) VALUES(?, ?, ?)'
def add_to_database(number, name, solution):
  """
  Add the sanitized problem name and problem solution to the SQLite3 databse.
  """
  cursor = conn.cursor()
  values = (number, name, solution)
  cursor.execute(prepared, values)
  conn.commit()
  cursor.close()

def create_table_on_startup():
  """
  Creates the SQLite table on startup if it doesn't exist.
  """
  cursor = conn.cursor()
  cursor.execute("CREATE TABLE IF NOT EXISTS problems(number TEXT PRIMARY KEY NOT NULL, name TEXT, solution BLOB)")
  cursor.close()

def main():
  print("test")
  create_table_on_startup()
  for problem in find_all_problems():
    number = problem.number  # Problem number is primary key in SQLite3
    name = problem.name
    sanitized_name = sanitize_name(name)  # For convenience we get a pretty name
    new_url = base_problem_url + name  # The github url uses the same file name as the extension.
    content = requests.get(new_url)
    content = content.content
    solution_soup = BeautifulSoup(content, 'html.parser')
    problem_solution = find_solution(solution_soup)
    add_to_database(number, sanitized_name, problem_solution)
    print(f"Finished scraping for {sanitized_name}'s solution")

if __name__ == "__main__":
  main()
