#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import json
import shutil
import subprocess

import requests


command = sys.executable + " -m nbconvert --to rst {0}"
pandoc = "pandoc {0} -o {1}.rst"


FORMATS = [
    ".adoc",
    ".asciidoc",
    ".context",
    ".ctx",
    ".db",
    ".doc",
    ".docx",
    ".dokuwiki",
    ".epub",
    ".fb2",
    ".htm",
    ".html",
    ".icml",
    ".json",
    ".latex",
    ".lhs",
    ".ltx",
    ".markdown",
    ".md",
    ".ms",
    ".muse",
    ".native",
    ".odt",
    ".opml",
    ".org",
    ".pdf",
    ".pptx",
    ".roff",
    ".rst",
    ".rtf",
    ".s5",
    ".t2t",
    ".tei",
    ".tei.xml",
    ".tex",
    ".texi",
    ".texinfo",
    ".text",
    ".textile",
    ".txt",
    ".wiki",
    ".xhtml",
    ".ipynb",
]


def get_gist(gist_id, content_dir="content"):
    url = "https://api.github.com/gists/{0}".format(gist_id)
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    description = data.get("description", None)
    owner = data.get("owner", {}).get("login", "github_user")

    os.makedirs(os.path.join(content_dir, owner), exist_ok=True)
    directory = os.path.join(content_dir, owner, gist_id)
    shutil.rmtree(directory, ignore_errors=True)
    subprocess.check_call(
        "git clone --depth=1 {0} {1}".format(data["git_pull_url"], directory),
        shell=True,
    )
    shutil.rmtree(os.path.join(directory, ".git"))
    in_files = list(sorted(glob.glob(os.path.join(directory, "*"))))

    files = []
    filemap = {}
    readme = None
    for filename in in_files:
        basename, ext = os.path.splitext(filename)
        outfile = basename + ".rst"
        filemap[outfile] = filename
        if ext.lower() == ".rst":
            pass
        if ext.lower() == ".ipynb":
            subprocess.check_call(command.format(filename), shell=True)
        elif ext.lower() in FORMATS:
            subprocess.check_call(
                pandoc.format(filename, basename), shell=True,
            )
        else:
            with open(outfile, "wb") as f:
                f.write("::\n\n".encode("utf-8"))
                with open(filename, "rb") as f_in:
                    for line in f_in:
                        f.write("    ".encode("utf-8"))
                        f.write(line)
                f.write("\n\n\n".encode("utf-8"))
        files.append(outfile)

        if os.path.split(filename)[1].lower().startswith("readme"):
            readme = outfile

        os.remove(filename)

    basefile = os.path.join(directory, "__combined__file__.rst")
    with open(basefile, "wb") as f:
        f.write(".. _{0}:\n\n".format(gist_id).encode("utf-8"))
        if description:
            f.write("{0}\n".format(description).encode("utf-8"))
            f.write(("=" * len(description) + "\n\n").encode("utf-8"))

        f.write(
            (
                ".. note:: The original gist can be found at: "
                "`{0} <{0}>`_\n\n".format(data["html_url"])
            ).encode("utf-8")
        )
    if readme is not None:
        open(basefile, "ab").write(open(readme, "rb").read())
        os.remove(readme)
    for file in files:
        if file == readme:
            continue
        with open(basefile, "ab") as f:
            fn = os.path.split(filemap[file])[1]
            f.write("{0}\n".format(fn).encode("utf-8"))
            f.write("{0}\n\n".format("-" * len(fn)).encode("utf-8"))
            f.write(open(file, "rb").read())
        os.remove(file)
    shutil.move(basefile, os.path.join(directory, "index.rst"))

    return data, directory


def generate_all(content_dir="content"):
    with open("index.json", "r") as f:
        index = json.load(f)

    for el in index:
        if "path" in el and os.path.exists(el["path"]):
            continue
        data, path = get_gist(el["gist_id"], content_dir=content_dir)
        el["path"] = path

    with open("index.json", "w") as f:
        json.dump(index, f, indent=2)

    with open("index.rst", "w") as f:
        f.write("gist.gallery\n=============\n\n")
        f.write(".. toctree::\n")
        f.write("   :maxdepth: 1\n\n")
        for el in index:
            f.write("   {0}/index\n".format(el["path"]))


if __name__ == "__main__":
    generate_all()
