#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""build.py: Generate a project build."""
__author__ = "Jeremy TRASBOT <contact@jeremy-trasbot.fr"

import os
import glob
import shutil

print("STEP 1 - Clear build directory")

files = glob.glob('../dist/flags/*')
for f in files:
    shutil.rmtree(f)

print("STEP 2 - Generate main CSS and copy svg to build directory")

cssBase = open("../src/base.css", "r")
css = cssBase.read()
cssBase.close()

os.mkdir("../dist/flags/country", 0o777)
os.mkdir("../dist/flags/special", 0o777)

print("STEP 2A - Generate countries ans regional")

css = css + "\n\n/* Countries and regional flags */"

for filename in glob.iglob("../src/country/" + '**/*.svg', recursive=True):
     print(filename)
     if "/" not in filename.replace("../src/country/", ""):
          shutil.copy(filename, "../dist/flags/country/")
          countryCode = filename.replace("../src/country/", "").replace(".svg", "")
          css = css + "\n\n.flags-country-" + countryCode + " {\n    background-image: url(flags/country/" + countryCode + ".svg);\n}"
     else:
        country, subcountry = filename.replace("../src/country/", "").split("/")
        subcountry = subcountry.replace(".svg", "")
        if not os.path.isdir("../dist/flags/country/" + country):
           os.mkdir("../dist/flags/country/" + country)
        shutil.copy(filename, "../dist/flags/country/" + country)
        css = css + "\n\n.flags-country-" + country + "-" + subcountry + " {\n    background-image: url(flags/country/" + country + "/" + subcountry + ".svg);\n}"

print("STEP 2B - Generate special")

css = css + "\n\n/* Special flags */"

for filename in glob.iglob("../src/special/" + '**/*.svg', recursive=True):
     print(filename)
     shutil.copy(filename, "../dist/flags/special/")
     code = filename.replace("../src/special/", "").replace(".svg", "")
     css = css + "\n\n.flags-special-" + code + " {\n    background-image: url(flags/special/" + code + ".svg);\n}"

print("STEP 3 - Write CSS")
cssFinal = open("../dist/flags.css", "w")
cssFinal.write(css)
cssFinal.close()