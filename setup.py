from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os

# Dynamically collect all .py files to cythonize (excluding __init__.py)
extensions = []
for root, _, files in os.walk("video_analytics"):
    for file in files:
        if file.endswith(".py") and file != "__init__.py":
            full_path = os.path.join(root, file)
            module_name = full_path.replace("/", ".").replace("\\", ".").replace(".py", "")
            extensions.append(Extension(module_name, [full_path]))

setup(
    name="video_analytics",
    version="0.1.0",
    author="Your Name",
    packages=find_packages(),
    ext_modules=cythonize(extensions, language_level=3),
    include_package_data=True,
    package_data={
        "video_analytics": ["weights/*.pt"],
    },
    zip_safe=False,  # Ensures Cython extensions load correctly from the wheel
)
