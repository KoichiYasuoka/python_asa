from setuptools import setup

setup(
    name='asapy',  # Required
    version='1.0.0',  # Required
    description='Python版ASA',  # Optional
    author='Takeuchi-Lab-LM',
    author_email='asarel@cl.cs.okayama-u.ac.jp',  # Optional
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    packages=['asapy'],  # Required
    package_data={"asapy":["*/*.*","*/*/*.*"]},
)
