import setuptools

with open("README.md", "r") as fh:
 long_description = fh.read()
setuptools.setup(
 name="trello_client-basics-api-bobruk76",
 version="0.0.1",
 author="Poliakov Vladimir",
 author_email="vladimir.m.polyakov@gmail.com",
 description="consol app to trello",
 long_description=long_description,
 long_description_content_type="text/markdown",
 url="https://github.com/bobruk76/D1",
 classifiers=[ "Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent", ],
 python_requires='>=3.6',)
