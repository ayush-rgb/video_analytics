from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os

def collect_cython_modules():
    extensions = []
    for root, dirs, files in os.walk("video_analytics"):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                full_path = os.path.join(root, file)
                module_name = full_path.replace("/", ".").replace(".py", "")
                extensions.append(Extension(module_name, [full_path]))
    return extensions

setup(
    name="video_analytics",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    ext_modules=cythonize(collect_cython_modules(), language_level=3),
    package_data={"video_analytics": ["weights/*.pt"]},
)
