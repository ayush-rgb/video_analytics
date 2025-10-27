from setuptools import setup, find_packages, Extension
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
from Cython.Build import cythonize
import os

class BinaryWheel(_bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False  # Mark as non-pure, since it has .so files

# Dynamically collect .py files you want to cythonize (optional)
cython_modules = []
for root, dirs, files in os.walk("video_analytics"):
    for file in files:
        if file.endswith(".py") and file != "__init__.py":
            full_path = os.path.join(root, file)
            module_name = full_path.replace("/", ".").replace(".py", "")
            cython_modules.append(Extension(module_name, [full_path]))

setup(
    name="video_analytics",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "video_analytics": [
            "*.so",
            "weights/*.pt",
            "object_detector/**/*.so",
        ],
    },
    ext_modules=cythonize(cython_modules, language_level=3),
    cmdclass={"bdist_wheel": BinaryWheel},
)
