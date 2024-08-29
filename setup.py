from setuptools import setup, find_packages

setup(
    name="zetta-backend-toolkit",
    version="0.1.0",
    author="Gonzalo Geraci",
    author_email="gonza.geraci@gmail.com",
    description="Un toolkit Backend para FastAPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gonzageraci/Zetta-Backend-Toolkit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
        "fastapi",
        "starlette",
    ],
)