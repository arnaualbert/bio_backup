from    pathlib import Path
import  json

'''Example of getting the data dir.'''

# About __file__
# ----------------------------------------------------
# - __file__ is a global variable defined automatically when python executes a .py file.
# - It contains the path to the .py file as a string.

# - It allows us to use paths relative to the file.
#   Useful to make our programs work from anywhere.

# - Caveat: __file__ is not defined in the interpreter.
#   In that case you must define it manually.
#   See "get_this_file_path()" function below.


# Use this function to make your code work in the interpreter
# ----------------------------------------------------
def get_this_file_path() -> str:

    try:    result = __file__
    except: result = '/some/path'

    return result


# Normally, your scripts will just access __file__
# ----------------------------------------------------
def main() -> None:

    # 1. Get data dir
    this_file:  Path = Path(__file__)
    this_dir:   Path = this_file.resolve().parent
    data_dir:   Path = (this_dir/'..'/'data').resolve()

    # 2. Read json file
    json_file:  Path        = data_dir/'scientific-papers.json'
    json_text:  str         = json_file.read_text()
    paper_list: list[dict]  = json.loads(json_text)

    # 3. Pretty-print paper titles
    title_list:     list[str] = [ paper['title'] for paper in paper_list ]
    title_list_str: str       = '\n'.join(title_list)
    print(title_list_str)

# ----------------------------------------------------
if __name__ == '__main__':
    main()
# ----------------------------------------------------
