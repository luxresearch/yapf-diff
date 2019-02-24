# yapf_diff
> change only what was changed

# install via pipenv

```{sh}
pipenv install git+https://github.com/skalt/yapf-diff.git@master#egg=yapf-diff
```

```
# requirements.txt: for a fast download
https://github.com/skalt/yapf-diff/archive/master.tar.gz
```
# usage

```
python -m yapf-diff --help # print usage
# usage: -m [-h] [-d] [-i] [--from-git-diff [BASE_REF]]
#
# format only changed lines
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -d, --diff            print the yapf args and produced diff
#   -i, --in-place        modify the changed files
#   --from-git-diff [BASE_REF]
#                         if used as a flag, this indicates that sdin is from
#                         git diff. If used as an argument, it indicates a ref
#                         against which to call git diff

# examples:
git diff origin/master | python -m yapf-diff --diff
python -m yapf-diff --from-git-diff="$(git log --merges -n 1)" --diff
```

# Credit where credit is due
This module modifies a function from `pycodestyle`, which is
under an MIT license. Their license is included within `./src/lib.py`.  Thanks
to the PyCQA team for doing a much better job at unified diff parsing than my
initial implementation.  

See also:
- https://github.com/hayd/pep8radius
- https://gist.github.com/mwek/59aefeefc812dea39c93c068eb30b491
