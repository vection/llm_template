from setuptools import setup, find_packages

setup(
    name='llm_template',
    version='0.1.0',
    author='Aviv Harazi',
    author_email='avivzx@gmail.com',
    description='Package designed to simplify the concept of getting structured output from LLMs',
    install_requires=[
            'transformers==4.41.1','torch==2.2.1'
    ],
    long_description="""Control your in-house LLM outputs by producing structured JSON outputs. llm_template enables the generation of robust JSON outputs from any instruction model. It can also create intricate schemas, working faster and more accurately than standard generation functions in most scenarios. This is achieved by injecting schema tokens into the response, compelling the LLM to generate only the values.""",
    long_description_content_type='text/markdown',
    url='https://github.com/vection/llm_template',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
