import click, os, tempfile, unittest, yaml
from click.testing import CliRunner

from cromulent import cc
from cromulent.cli import cc_print_cmd

class CcPrintCmdTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test_yaml_cmd(self):
        runner = CliRunner()

        result = runner.invoke(cc_print_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cc_print_cmd, [])
        self.assertEqual(result.exit_code, 2)

        data = dict.fromkeys(cc.config_attributes(), "TEST")
        yaml_fn = os.path.join(self.temp_d.name, "cromwell-attrs.yaml")
        with open(yaml_fn, "w") as f:
            f.write(yaml.dump(data))
        result = runner.invoke(cc_print_cmd, [yaml_fn], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = """CROMWELL_ROOT_DIR: null
"""
        #self.assertEqual(result.output, expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
