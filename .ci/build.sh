#!/bin/bash
set -e

# Load the environment
if [[ -n $CONDA ]]; then
    . $CONDA/etc/profile.d/conda.sh
    conda activate ./env
fi

python build.py
make dirhtml

mkdir gh-pages
cd gh-pages
git clone -b gh-pages --single-branch https://github.com/dfm/gist.gallery.git .

rm -rf .git

cp -r ../_build/dirhtml/* .

git init
touch .nojekyll
git add .nojekyll
git add -f *
git -c user.name='dfm' -c user.email='foreman.mackey@gmail.com' \
    commit -m "rebuild gh-pages"
git push -f https://dfm:$GITHUB_API_KEY@github.com/dfm/gist.gallery \
    HEAD:gh-pages >/dev/null 2>&1 -q
