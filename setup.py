from setuptools import setup, find_packages

setup(
    name="potato_stream_server",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=["aiohttp==3", "aiohttp-cors==0.7.0",],
)
