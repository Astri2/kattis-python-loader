from pathlib import Path
import subprocess
import sys
import zipfile
import io
import re
import requests
from enum import Enum
from time import time

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
        

def main():
    samples_url = f"{sys.argv[1]}/file/statement/samples.zip"
    tests_to_run = [i for i in sys.argv[3:] if re.match("[0-9]+",i)]
    if "-c" in sys.argv[3:]: c.enable_colors()
    r = requests.get(samples_url)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        filePaths = [Path(file.filename) for file in z.filelist if file.filename.endswith(".in")]
        for i in range(len(filePaths)):
            if(len(tests_to_run) == 0 or str(i+1) in tests_to_run):
                print(f"{c.cu}Test {i+1}{c.w}:")
                test_input = z.read(filePaths[i].name).decode("utf-8")
                test_answer = re.sub(r"\s+$","",z.read(f"{filePaths[i].stem}.ans").decode("utf-8"))
                t = time()
                p = subprocess.run([sys.executable, sys.argv[2]],
                                    input=test_input, encoding="utf-8", capture_output=True)
                t = time()-t
                if p.returncode != 0:
                    print("Error:", p.stderr)
                out = re.sub(r"\s+$","",p.stdout)
                print("Sample input:\n", test_input, sep="")
                if out != test_answer:
                    print(f"{c.r}Wrong answer!{c.w}")
                    f_ans,f_out = get_difference_disp(test_answer,out)
                    print("Expected:", len(test_answer),"\n\"", f_ans, sep="", end="\"\n\n")
                    print("Got:", len(out),"\n\"", f_out, sep="", end="\"\n")
                else:
                    print(f"{c.g}Good answer!{c.w}")
                    print("Answer:\n", out, sep="")
                print(f"{c.d}took {round(t,3)}s{c.w}")
                print()

if __name__ == "__main__":
    main()