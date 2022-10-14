import subprocess
import sys
import zipfile
import io
import re
import requests
from enum import Enum

class c(Enum):

    __use_colors__ = False

    g  = "\033[0m\033[1;92m"
    gu = "\033[0m\033[4;49;92m"
    r  = "\033[0m\033[1;91m"
    ru = "\033[0m\033[4;49;91m"
    c  = "\033[0m\033[4;96m"
    yu  = "\033[0m\033[4;93m"

    w  = "\033[0m"

    def __str__(self):
        return self.value if c.__use_colors__ else ""
    def enable_colors():
        c.__use_colors__ = True


def get_difference_disp(ans,out):
    f_ans=""; f_out = ""
    len_min = min(len(ans),len(out))
    for i in range(0,len_min):
        col = c.gu if ans[i] == out[i] else c.ru
        f_ans+=str(col)+ans[i]
        f_out+=str(col)+ans[i]
    f_ans+=str(c.yu)+ans[len_min:]+str(c.w)
    f_out+=str(c.yu)+out[len_min:]+str(c.w)
    return f_ans,f_out
        

def main():
    samples_url = f"{sys.argv[1]}/file/statement/samples.zip"
    tests_to_run = [i for i in sys.argv[3:] if re.match("[0-9]+",i)]
    if "-c" in sys.argv[3:]: c.enable_colors()
    r = requests.get(samples_url)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        for i in range(1,len(z.filelist)//2+1):
            if(len(tests_to_run) == 0 or str(i) in tests_to_run):
                print(f"{c.c}Test {i}:{c.w}")
                test_input = z.read(f"{i}.in").decode("utf-8")
                test_answer = re.sub(r"\s+$","",z.read(f"{i}.ans").decode("utf-8"))
                p = subprocess.run([sys.executable, sys.argv[2]],
                                    input=test_input, encoding="utf-8", capture_output=True)
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
                print()

if __name__ == "__main__":
    main()