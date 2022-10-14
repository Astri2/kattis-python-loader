import subprocess
import sys
import zipfile
import io
import re

import requests

pb_id = "".join(letter for letter in "".join(
    sys.argv[1:]).lower() if letter.isalnum())
samples_url = f"{sys.argv[1]}/file/statement/samples.zip"
test_to_run = sys.argv[3:]
r = requests.get(samples_url)
r.raise_for_status()

with zipfile.ZipFile(io.BytesIO(r.content)) as z:
    for i in range(1,len(z.filelist)//2+1):
        if(len(test_to_run) == 0 or str(i) in test_to_run):
            test_input = z.read(f"{i}.in").decode("utf-8")
            test_answer = re.sub(r"\s+$","",z.read(f"{i}.ans").decode("utf-8"))
            p = subprocess.run([sys.executable, sys.argv[2]],
                                input=test_input, encoding="utf-8", capture_output=True)
            if p.returncode != 0:
                print("Error:", p.stderr)
            out = re.sub(r"\s+$","",p.stdout)
            print("Sample input:\n", test_input, sep="")
            if out != test_answer:
                print("Wrong answer!")
                print("Expected:", len(test_answer),"\n", test_answer, sep="")
                print("Got:", len(out),"\n", out, sep="")
            else:
                print("Good answer!")
                print("Answer:\n", out, sep="")
