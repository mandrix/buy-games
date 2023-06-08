from setuptools import setup, find_packages

setup(
    name='buy-games',
    version='1.0.0',
    author='mandrix',
    author_email='mandrix@ejemplo.com',
    description='Descripción del paquete',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'django>=3.2.4',
        'requests>=2.25.1',
    ],
)
