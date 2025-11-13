from setuptools import setup, find_packages

setup(
    name="market_ib_api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "boto3",
        "fastapi",
        "ib_insync",
        "pydantic-settings",
        "ta",
        "numpy",
        "pydantic",
        "setuptools",
    ],
    python_requires='>=3.10',
)
