from setuptools import setup, find_packages

setup(
    name='HabitTrackerIU',
    extras_require=dict(tests=['pytest']),
    version="0.1.0",
    py_modules=["main"],
    install_requires=["click", "tabulate"],
    entry_points={"console_scripts": ["habit = main:main_cli"]}

)


