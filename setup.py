from setuptools import find_packages, setup


setup(
    name='students_rating',
    version='1.0.0',
    license='BSD',
    description='students_rating',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask_bootstrap',
    ],
)