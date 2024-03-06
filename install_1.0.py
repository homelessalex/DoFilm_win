import os
import pathlib
#os.system ("winget install --id Git.Git -e --source winget")

os.system(  "cd " + os.path.dirname(os.path.abspath(__file__))+" & "+
            "git clone https://github.com/homelessalex/DoFilm_win.git"+" & "+
            "cd dofilm"+" & "+
            "mkdir rendered imgs"+" & "+
            "py -m pip install numpy colour-science Cython setuptools flet matplotlib numba scipy wheel rawpy"+" & "+
            "cd " + os.path.abspath("DoFilm")
            )

#os.replace(os.path.abspath("dist/DoFilm.app"), os.path.abspath("dist/DoFilm.app"))
#os.remove(os.path.abspath("dist"))
#os.remove(os.path.abspath("build"))
#"mv " + os.path.abspath("dist/DoFilm.app") + " " + os.path.dirname(os.path.abspath(__file__))+"\n" +
