import click, jinja2, os, sys, yaml

from cromulent import cc

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Cromwell on MGI Compute
    """
    pass

@click.command(short_help="dump the yaml attributes needed for cromwell config")
def yaml_cmd():
    """
    Output the a YAML string with the needed attributes top generate
    the cromwell config.
    """
    sys.stdout.write(yaml.dump(dict.fromkeys(cc.config_attributes())))
cli.add_command(yaml_cmd, "yaml")
