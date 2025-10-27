from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
import os

class BinaryWheel(_bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False  # Marks the wheel as platform-specific

def collect_cython_extensions(base_dir="video_analytics"):
    extensions = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                path = os.path.join(root, file)
                # Convert file path to module name (portable across OS)
                module_name = os.path.splitext(path)[0].replace(os.path.sep, ".")
                extensions.append(Extension(module_name, [path]))
    return extensions

setup(
    name="video_analytics",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    ext_modules=cythonize(collect_cython_extensions(), language_level=3),
    package_data={
        "video_analytics": ["weights/*.pt"]
    },
    cmdclass={"bdist_wheel": BinaryWheel},
)
