from setuptools import setup, find_packages

setup(
    name="RetroStats",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description="Game statistics for RetroPie",
    author="Daniel Langesten",
    author_email="",
    python_requires=">=3.7.0",
    packages=find_packages(),
    install_requires=["flask"],
    entry_points={
        "console_scripts": [
            "retro-stats-cli=stats.main:main",
            "retro-stats-server=server.main:main",
        ]
    },
)
