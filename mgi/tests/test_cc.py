import os, unittest
from jinja2 import Template

from cromulent import cc

class CcTest(unittest.TestCase):
    
    #def setUp(self):
    #    self.temp_d = tempfile.TemporaryDirectory()
    #def tearDown(self):
    #    self.temp_d.cleanup()

    def test_config_attributes(self):
        attrs = cc.config_attributes()
        self.assertTrue(bool(attrs))

    def test_resources(self):
        resources_dn = cc.resources_dn()
        expected_dn = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "cromulent", "resources")
        cc_template_fn = cc.config_template_fn()
        expected_fn = os.path.join(expected_dn, "compute1.conf.jinja")
        self.assertEqual(cc_template_fn, expected_fn)

# --

if __name__ == '__main__':
    unittest.main(verbosity=2)
