from setuptools import setup, find_packages
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

class BinaryWheel(_bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False  # make it platform-specific

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
    cmdclass={"bdist_wheel": BinaryWheel},
)
