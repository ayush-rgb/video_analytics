from setuptools import setup, find_packages, Extension
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
from Cython.Build import cythonize

class BinaryWheel(_bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False

extensions = cythonize([
    "video_analytics/*.py",
    "video_analytics/object_detector/models/*.py",
    "video_analytics/object_detector/utils/*.py",
], language_level=3)

setup(
    name="video_analytics",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    ext_modules=extensions,
    package_data={
        "video_analytics": ["weights/*.pt"]
    },
    cmdclass={"bdist_wheel": BinaryWheel},
)
