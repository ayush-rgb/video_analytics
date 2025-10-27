from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

# List every Python file to compile (excluding __init__.py)
extensions = [
    Extension("video_analytics.wrapper", ["video_analytics/wrapper.py"]),
    Extension("video_analytics.object_detector.models.common", ["video_analytics/object_detector/models/common.py"]),
    Extension("video_analytics.object_detector.models.experimental", ["video_analytics/object_detector/models/experimental.py"]),
    Extension("video_analytics.object_detector.models.yolo", ["video_analytics/object_detector/models/yolo.py"]),
    Extension("video_analytics.object_detector.utils.activations", ["video_analytics/object_detector/utils/activations.py"]),
    Extension("video_analytics.object_detector.utils.add_nms", ["video_analytics/object_detector/utils/add_nms.py"]),
    Extension("video_analytics.object_detector.utils.autoanchor", ["video_analytics/object_detector/utils/autoanchor.py"]),
    Extension("video_analytics.object_detector.utils.datasets", ["video_analytics/object_detector/utils/datasets.py"]),
    Extension("video_analytics.object_detector.utils.general", ["video_analytics/object_detector/utils/general.py"]),
    Extension("video_analytics.object_detector.utils.google_utils", ["video_analytics/object_detector/utils/google_utils.py"]),
    Extension("video_analytics.object_detector.utils.loss", ["video_analytics/object_detector/utils/loss.py"]),
    Extension("video_analytics.object_detector.utils.metrics", ["video_analytics/object_detector/utils/metrics.py"]),
    Extension("video_analytics.object_detector.utils.plots", ["video_analytics/object_detector/utils/plots.py"]),
    Extension("video_analytics.object_detector.utils.torch_utils", ["video_analytics/object_detector/utils/torch_utils.py"]),
]

setup(
    name="video_analytics",
    version="0.1.0",
    author="Your Name",
    packages=find_packages(include=["video_analytics", "video_analytics.*"]),
    ext_modules=cythonize(extensions, language_level=3),
    include_package_data=True,
    package_data={"video_analytics": ["weights/*.pt"]},
    zip_safe=False,  # needed for binary extensions
)
