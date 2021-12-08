import click, jinja2, os, yaml

from cromulent import cc

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Cromwell on MGI Compute
    """
    pass
