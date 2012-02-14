"""
xmldict
========

Convert xml to python dictionaries, and vice-versa.

Installation
------------

    pip install xmldict

On most of the systems, you will need the `sudo` permissions if you are doing a system wide
install.

    sudo pip install xmldict


Exmaple
---------------------
::
    # Converting xml to dictionary
    >>> xmldict.xml_to_dict('''
    ... <root>
    ...   <persons>
    ...     <person>
    ...       <name first="foo" last="bar" />
    ...     </person>
    ...     <person>
    ...       <name first="baz" last="bar" />
    ...     </person>
    ...   </persons>
    ... </root>
    ... ''')
    {'root': {'persons': {'person': [{'name': {'last': 'bar', 'first': 'foo'}}, {'name': {'last': 'bar', 'first': 'baz'}}]}}}


::
    # Converting dictionary to xml
    >>> xmldict.dict_to_xml({'root': {'persons': {'person': [{'name': {'last': 'bar', 'first': 'foo'}}, {'name': {'last': 'bar', 'first': 'baz'}}]}}})
    '<root><persons><person><name><last>bar</last><first>foo</first></name></person><person><name><last>bar</last><first>baz</first></name></person></persons></root>'

Convert xml to python dictionaries.

"""

from setuptools import setup
setup(name='xmldict',
      version='0.4',
      description='Convert xml to python dictionaries.',
      long_description=__doc__,
      author='Rahul Kumar',
      author_email='rahul@thoughtnirvana.com',
      license='BSD',
      url='https://github.com/thoughtnirvana/xmldict',
      py_modules=['xmldict']
     )
