# This file is part of GPropertyGrid project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

"""GPropertyGrid setup script"""

from distutils.core import setup
from gpropertygrid import VERSION

def run():
    setup(name="GPropertyGrid",
        version=VERSION,
        url="http://www.formateli.com/software/gpropertygrid/",
        download_url="", #TODO 
        description="Python Gtk 3 property grid widget.",
        author="Fredy Ramirez",
        author_email="", #TODO
        maintainer_email="", #TODO
        classifiers=[
            "Development Status :: Prototype",
            "Environment :: Win32 (MS Windows)",
            "Environment :: X11 Applications",
            "Intended Audience :: Developers",
            "Intended Audience :: Information Technology",
            "License :: OSI Approved :: GNU General Public License v3",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
        ],
        license="GNU General Public License v3",
        platforms=["OS Independent"],
        packages=["gpropertygrid",],
        package_data={},
        scripts=[],
        data_files=[("docs", ["README", "LICENSE", "COPYRIGHT"])],
    )

if __name__ == "__main__":
    run()

