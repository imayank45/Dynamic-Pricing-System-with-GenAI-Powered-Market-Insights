from setuptools import setup, find_packages

setup(
    name="dynamic_pricing",
    version="0.1.0",
    packages=find_packages(),
    install_requires=open("requirements.txt").readlines(),
    author="Mayank Kathane",
    description="Dynamic Pricing System with GenAI-Powered Market Insights",
)