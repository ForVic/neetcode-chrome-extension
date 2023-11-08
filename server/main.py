from flask import Flask
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
conn = sqlite3.connect("problems.db", check_same_thread=False)

@app.route("/", methods=["GET"])
def entry():
  return "Success", 200

@app.route("/solution/<solution_id>", methods=["GET"])
def get_solution(solution_id):
  cursor = conn.cursor()
  sql = f"SELECT solution FROM problems WHERE number=?"
  solution = cursor.execute(sql, (solution_id,))
  res = solution.fetchall()
  if res:
    return res
  else:
    return "Neetcode solution not found in database"

@app.route("/problem/<problem_name>", methods=["GET"])
def get_solution_by_problem_name(problem_name):
  cursor = conn.cursor()
  sql = f"SELECT solution FROM problems WHERE name=?"
  solution = cursor.execute(sql, (problem_name,))
  res = solution.fetchall()
  if res:
    return res
  else:
    return "Neetcode solution not found in database"

def main():
  app.run(debug=True)

if __name__ == "__main__":
  main()

