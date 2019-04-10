# yapf_diff
> change only what was changed

# install
<details open><summary>with pipenv</summary>

```{sh}
pipenv install git+https://github.com/luxresearch/yapf-diff.git@master#egg=yapf-diff
```
</details>

<details><summary>with pip</summary>

```{sh}
pip install git+https://github.com/luxresearch/yapf-diff.git@master#egg=yapf-diff
```
</details>
<details><summary>in requirements.txt</summary>

```
# requirements.txt: for a fast download
https://github.com/luxresearch/yapf-diff/archive/master.tar.gz
```
</details>

# should I use `yapf_diff`?
Only if formatting all the lines in your modified file(s) would cause an unacceptably big diff in your revision history. [PEP 8](https://www.python.org/dev/peps/pep-0008/#id15) recommends keeping your code consistent with the surrounding code. `yapf-diff` guarantees consistency only within the lines touched within a diff.

- if you're the the one choosing how and when to lint, choose [`black`](https://github.com/ambv/black) for consistency and speed.
- if formatting entire file at a time is an option, use something like

```bash
git diff --name-only | xargs black # or yapf, if you need a custom format
```

# usage

```bash
# usage: yapf-diff [-h] [-d] [--debug] [-i] [--from-git-diff [BASE_REF]]
#
# format only changed lines
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -d, --diff            print the yapf args and produced diff
#   --debug               print the style yapf is picking up
#   -i, --in-place        modify the changed files
#   --from-git-diff [BASE_REF]
#                         if used as a flag, this indicates that stdin is from
#                         git diff. If used as an argument, it indicates a ref
#                         against which to call git diff

# examples:
git diff origin/master | python -m yapf-diff --diff
python -m yapf-diff --from-git-diff="$(git log --merges -n 1)" --diff
```

# Credit where credit is due
This module modifies a function from `pycodestyle`, which is under an MIT license.
Their license is included within [`./src/lib.py`](./src/lib.py).
Thanks to the PyCQA team for doing a much better job at unified diff parsing than my initial implementation.  

See also:
- https://github.com/hayd/pep8radius
- https://gist.github.com/mwek/59aefeefc812dea39c93c068eb30b491
