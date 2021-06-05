from setuptools import setup

setup(name='basic_mondrian_health',
      version='0.2',
      description='A basic mondrian fork for anonymizing our custom example health data',
      author='Immanuel Kunz',
      author_email='immanuel.kunz@aisec.fraunhofer.de',
      license='MIT',
      packages=setuptools.find_packages(),
      zip_safe=False,
      package_data={
            'basic_mondrian_health': ['data/*'],
      })