# setup.py  (na raiz)
from pathlib import Path
from setuptools import setup, find_packages

setup(
    name="tech_challenge_escalas",
    version="0.1.0",
    description="Algoritmo Genético para gerar escalas de supermercado",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=Path("requirements.txt").read_text().splitlines(),
)