import click, unittest
from click.testing import CliRunner

from cromulent.cli import cli

class CliTest(unittest.TestCase):
    def test_cromulent_cli(self):
        runner = CliRunner()

        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["-h"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
# --

if __name__ == '__main__':
    unittest.main(verbosity=2)
