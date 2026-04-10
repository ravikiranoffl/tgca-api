from setuptools import setup, find_packages

setup(
    name='tgca_api',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'google-generativeai',
        'python-dotenv'
    ],
    description='A real-time news intelligence engine powered by TGCA and Gemini.',
)
