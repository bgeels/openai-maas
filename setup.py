from setuptools import setup

setup(
  name="openai-maas",
  version="1.0.1",
  author="Ben Geels",
  author_email="ben.geels019@gmail.com",
  description="Creates memes leveraging OpenAI API",
  url="https://github.com/bgeels/openai-maas",
  license="MIT",
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
  ],
  package_data={ 'openai_maas': [
    'fonts/*'
  ]},
  install_requires=[
    "alt-profanity-check==1.1.3",
    "openai==0.26.0",
    "Pillow==9.4.0"
  ]
)
