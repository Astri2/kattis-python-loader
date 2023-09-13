from pathlib import Path
import subprocess
import sys
import zipfile
import io
import re
import requests
from enum import Enum
from time import perf_counter

class c(Enum):

    __use_colors__ = False

    g  = "\033[0m\033[1;92m"
    r  = "\033[0m\033[1;91m"
    d  = "\033[0m\033[1;49;90m"
    y  = "\033[0m\033[1;93m"
    cu  = "\033[0m\033[4;96m"

    w  = "\033[0m"

    def __str__(self):
        return self.value if c.__use_colors__ else ""
    def enable_colors():
        c.__use_colors__ = True


def get_difference_disp(ans,out):
    lines_ans = ans.split("\n")
    lines_out = out.split("\n")

    f_ans=""; f_out = ""
    len_min = min(len(lines_ans),len(lines_out))
    for i in range(0,len_min):
        col = c.g if lines_ans[i] == lines_out[i] else c.r
        f_ans+=str(col)+lines_ans[i]+"\n"
        f_out+=str(col)+lines_out[i]+"\n"
    f_ans+=str(c.y)+"\n".join(lines_ans[len_min:])+str(c.w)
    f_out+=str(c.y)+"\n".join(lines_out[len_min:])+str(c.w)
    return f_ans,f_out
        

def parse_params(argv: list):
    argc = len(argv)
    url: str = ""
    file: str = ""
    unit_tests: list = []
    folder = "./"
    option_map = {"-t": "--test", "-c": "--color", "-u": "--url", "-n": "--name", "-f": "--file", "-d": "--directory"}
    for i, arg in enumerate(argv): 
        if arg in option_map.keys(): argv[i] = option_map[arg]
    
    if "--color" in argv: 
        c.enable_colors()
    if "--url" in argv:
        i = argv.index("--url")
        if i+1 == argc:
            print(f"{c.r}error: --url option requires an url{c.w}")
            exit(1)
        url = argv[i+1]
    if "--file" in argv:
        i = argv.index("--file")
        if i+1 == argc: 
            print(f"{c.r}error: --file option requires a file path{c.w}")
            exit(1)
        file = Path(argv[i+1])
    if "--directory" in argv:
        i = argv.index("--directory")
        if i+1 == argc:
            print(f"{c.r}error: --folder option requires a folder path{c.w}")
        if(file): print(f"{c.y}warning: --folder option ingored because of --file option{c.w}")
        folder = argv[i+1]
    if "--name" in argv:
        i = argv.index("--name")
        if i+1 == argc:
            print(f"{c.r}error: --name option requires a name{c.w}")
            exit(1)
        name = argv[i+1]
        if not url: url = f"https://open.kattis.com/problems/{name}"
        else: print(f"{c.y}warning: --name option ingored for problem url because of --url option{c.w}")
        if not file: file = Path(f"{folder}{name}.py")
        else: print(f"{c.y}warning: --name option ingored for solution file because of --file option{c.w}")
    if "--test" in argv:
        i = argv.index("--test")+1
        while i < argc and str.isnumeric(argv[i]):
            unit_tests.append(int(argv[i]))
            i+=1
    if not(url and file):
        print("missing arguments, no url or file found")
        print("format : python3 main.py [-u <problem url>] [-f <solution file>] [-n <problem/solution name>] [-t <unit_tests_to_run...>] [<options...>]")
        exit(1)
    return url, file, unit_tests

def main():
    url, solution_path, unit_tests = parse_params(sys.argv)
    # print(f"url '{url}'\nfile '{solution_path}'\ncolor '{color}'\ntests'{unit_tests}'")
    print(f"Kattis Problem url: {c.cu}{url}{c.w}")
    print(f"Solution file: {c.cu}{solution_path}{c.w}")
    print(f"unit test IDs to run: {c.cu}", *unit_tests if unit_tests else ["all"], f"{c.w}\n",sep="")
    if not Path.exists(solution_path):
        print(f"{c.r}error: file {solution_path} does not exist !{c.w}")
        exit(1)

    samples_url = f"{url}/file/statement/samples.zip"
    
    r = requests.get(samples_url)
    if r.status_code == 404:
        print(f"{c.r}error: {samples_url} not found!{c.w}")
        exit(1)
    elif r.status_code != 200:
        print(f"{c.r}Unknown error while fetching {samples_url}{c.w}")
        r.raise_for_status()
        exit(1)
    
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        filePaths = [Path(file.filename) for file in z.filelist if file.filename.endswith(".in")]
        for i in range(len(filePaths)):
            if(len(unit_tests) == 0 or i+1 in unit_tests):
                print(f"{c.cu}Test {i+1}{c.w}:")
                test_input = z.read(filePaths[i].name).decode("utf-8")
                test_answer = z.read(f"{filePaths[i].stem}.ans").decode("utf-8").strip()
                t = perf_counter()

                p = subprocess.run([sys.executable, solution_path],
                                    input=test_input, encoding="utf-8", capture_output=True)
                t = perf_counter()-t
                if p.returncode != 0:
                    print("Error:", p.stderr)
                out = p.stdout.strip()
                # strip all lines
                out = "\n".join([line.strip() for line in out.split("\n")])

                print("Sample input:\n", test_input, sep="")
                if out != test_answer:
                    print(f"{c.r}Wrong answer!{c.w}")
                    f_ans,f_out = get_difference_disp(test_answer,out)
                    print("Expected:", len(test_answer),"\n\"", f_ans, sep="", end="\"\n\n")
                    print("Got:", len(out),"\n\"", f_out, sep="", end="\"\n")
                else:
                    print(f"{c.g}Good answer!{c.w}")
                    print(f"Answer:\n{c.g}{out}{c.w}")
                print(f"{c.d}took {round(t,3)}s{c.w}")
                print()

if __name__ == "__main__":
    main()