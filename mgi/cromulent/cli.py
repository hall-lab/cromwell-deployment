import click, jinja2, os, sys, yaml

from cromulent import cc

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Cromwell on MGI Compute
    """
    pass

@click.command(short_help="dump the cromwell config")
@click.argument("yaml-file", type=click.File('r'), nargs=1)
def cc_print_cmd(yaml_file):
    """
    Cromwell Config [CC] Print

    Given a filled in CC YAML file, apply it to the cromwell configuration and print.
    """
    data = yaml.safe_load(yaml_file)
    with open(cc.config_template_fn(), "r") as f:
        config_t = jinja2.Template(f.read())
    sys.stdout.write(config_t.render(data))
cli.add_command(cc_print_cmd, "cc-print")

@click.command(short_help="print the yaml attributes needed for cromwell config")
def cc_yaml_cmd():
    """
    Cromwell Config [CC] YAML

    Output the a YAML string with the needed attributes top generate
    the cromwell config.
    """
    sys.stdout.write(yaml.dump(dict.fromkeys(cc.config_attributes())))
cli.add_command(cc_yaml_cmd, "yaml")
