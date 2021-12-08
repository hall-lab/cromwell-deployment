import click, unittest
from click.testing import CliRunner

from cromulent.cli import yaml_cmd

class CliTest(unittest.TestCase):
    def test_yaml_cmd(self):
        runner = CliRunner()

        result = runner.invoke(yaml_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(yaml_cmd, [])
        self.assertEqual(result.exit_code, 0)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = """CROMWELL_ROOT_DIR: null
LSF_DEFAULT_DOCKER: null
LSF_DOCKER_VOLUMES: null
LSF_JOB_GROUP: null
LSF_QUEUE: null
LSF_USER_GROUP: null
"""
        self.assertEqual(result.output, expected_output)
# --

if __name__ == '__main__':
    unittest.main(verbosity=2)
