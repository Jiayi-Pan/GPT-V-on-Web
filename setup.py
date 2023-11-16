from setuptools import setup

setup(
    name="webai",
    version="0.0.1",
    packages=['webai'],
    install_requires=["openai", "selenium"],
    entry_points={
        "console_scripts": [
            "webai = webai:main"
        ]
    },
    include_package_data=True
)
