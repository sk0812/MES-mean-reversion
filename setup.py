from setuptools import setup, find_packages

setup(
    name="futures_trading",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ib_insync>=0.9.85",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "python-dotenv>=1.0.0",
    ],
    author="Sid Kheria",
    description="A futures trading system with VWAP-based strategy",
    python_requires=">=3.8",
) 