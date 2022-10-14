# kattis-python-loader
A quick script to automate kattis local test.

# Install
```bash
git clone https://github.com/Joffref/kattis-python-loader.git
```

# Getting started
```bash
# python3 main.py {problem_url} {your_answer_file} [options ...] [unit_tests_to_run ...]
python3 main.py https://open.kattis.com/problems/basicprogramming1 answer.py
```

> If your terminal supports text coloration, you can enable it by adding the -c option.

> If you don't want to run all the unit tests, you can specify which ones you want to run. If you want to run them all, keep it empty.

```bash
python3 main.py https://open.kattis.com/problems/basicprogramming1 answer.py -c
python3 main.py https://open.kattis.com/problems/basicprogramming1 answer.py 1 3
```

# Contribution
Feel free to contribute to this project. You can do it by:

Reporting bugs

Suggesting new features

Implementing new features

Fixing bugs

Improving documentation

...
