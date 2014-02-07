import unittest
import datetime
from xmldict import xml_to_dict, dict_to_xml

class TestXmlutils(unittest.TestCase):
    def test_xml_to_dict_simple(self):
        test = '''
        <payment_method>
        <created_at type="datetime">2011-02-12T20:20:46Z</created_at>
        <is_retained type="boolean">true</is_retained>
        <first_name>Bob</first_name>
        <expiry_month type="integer">1</expiry_month>
        <address_1 nil="true"></address_1>
        </payment_method>
        '''

        expected = {'payment_method': {'address_1': {'nil': 'true'},
                                       'created_at': datetime.datetime(2011, 2, 12, 20, 20, 46),
                                       'expiry_month': 1,
                                       'first_name': 'Bob',
                                       'is_retained': True}}

        self.assertEqual(expected, xml_to_dict(test, strict=False))

    def test_xml_to_dict_list(self):
        test = '''
        <messages>
        <message>message1</message>
        <message>message2</message>
        </messages>
        '''

        expected = {'messages': {'message': ['message1', 'message2']}}
        self.assertEqual(expected, xml_to_dict(test, strict=False))

    def test_xml_to_dict_strict(self):
        test = '''
        <payment_method>
        <created_at type="datetime">2011-02-12T20:20:46Z</created_at>
        <is_retained type="boolean">true</is_retained>
        <messages>
            <message class="error" context="input.cvv" key="too_long" />
            <message class="error" context="input.card_number" key="failed_checksum" />
        </messages>
        </payment_method>
        '''

        expected = {'payment_method': {
            'created_at': {
                '@type': 'datetime',
                '#value': datetime.datetime(2011, 2, 12, 20, 20, 46),
                '#text': '2011-02-12T20:20:46Z'
            },
            'is_retained': {
                '@type': 'boolean',
                '#value': True,
                '#text': 'true'
            },
            'messages': {'message': [{'@class': 'error',
                                      '@context': 'input.cvv',
                                      '@key': 'too_long'},
                                     {'@class': 'error',
                                      '@context': 'input.card_number',
                                      '@key': 'failed_checksum'}]},
        }}

        self.assertEqual(expected, xml_to_dict(test, strict=True))

    def test_xml_to_dict_and_reverse(self):

        self.maxDiff = None

        test = '''
        <messages>
        <message id="1">
        a
        b
        ...
        </message>
        <message id="2">
        c
        d
        ...
        </message>
        </messages>
        '''

        expected = {'messages':
                     {'message':
                        [
                            {'@id': '1',
                             '#value': 'a\n        b\n        ...',
                             '#text': '\n        a\n        b\n        ...\n        ',
                            },
                            {'@id': '2',
                             '#value': 'c\n        d\n        ...',
                             '#text': '\n        c\n        d\n        ...\n        ',
                            },
                        ]
                    }
                  }

        self.assertEqual(expected, xml_to_dict(test, strict=True))

        # once converted to dict, go back to xml
        self.assertEqual(test, dict_to_xml(expected))

    def test_xml_to_dict_order(self):
        order1 = '<a><c>2</c><c>3</c><b>1</b></a>'
        order2 = '<a><b>1</b><c>2</c><c>3</c></a>'
        expected ={'a': {'c': ['2', '3'], 'b': '1'}}
        self.assertEqual(expected, xml_to_dict(order1))
        self.assertEqual(expected, xml_to_dict(order2))

    def test_dict_to_xml_simple(self):
        dict_xml = {'transaction': {'amount': '100.00', 'currency_code': 'USD'}}
        expected = '<transaction><amount>100.00</amount><currency_code>USD</currency_code></transaction>'
        self.assertEqual(expected, dict_to_xml(dict_xml))

    def test_dict_to_xml_empty(self):
        dict_xml = {'messages': {'message': None}}
        expected = '<messages><message>null</message></messages>'
        self.assertEqual(expected, dict_to_xml(dict_xml))

    def test_dict_to_xml_lists(self):
        dict_xml = {'messages': {'message': ['message1', 'message2'], 'flag': True}}
        expected = '<messages><message>message1</message><message>message2</message><flag>true</flag></messages>'
        self.assertEqual(expected, dict_to_xml(dict_xml))

    def test_dict_to_xml_attributes(self):
        dict_xml = {'messages': {
            'message': [{'@foo': 'bar1', 'baz': 'baz1', '#text': 'message1'},
                        {'@foo': 'bar2', 'baz': 'baz2', '#text': 'message2'}],
            'flag': True
        }}
        expected = '<messages><message foo="bar1"><baz>baz1</baz>message1</message><message foo="bar2"><baz>baz2</baz>message2</message><flag>true</flag></messages>'
        self.assertEqual(expected, dict_to_xml(dict_xml))

if __name__ == '__main__':
    unittest.main()
