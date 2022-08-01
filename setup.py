from setuptools import setup


setup(
    name='event-driven-architecture-demos',
    version='0.0.0',
    url='',
    license='Proprietary',
    author='Silo AI',
    author_email='sebastian.remander@gmail.com',
    description='EDA demo for local development setup',
    install_requires=[
        "aiokafka~=0.7.2",
        "fastapi~=0.77.1",
        "uvicorn~=0.17.6",
    ],
)
