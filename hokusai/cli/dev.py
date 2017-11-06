import click

import hokusai

from hokusai.lib.config import config

from hokusai.cli.base import base
from hokusai.lib.common import set_verbosity, CONTEXT_SETTINGS

@base.group()
def dev(context_settings=CONTEXT_SETTINGS):
  """Interact with docker-compose development environment
  defined by ./hokusai/development.yml"""
  pass


@dev.command(context_settings=CONTEXT_SETTINGS)
@click.option('--build/--no-build', default=True, help='Force a build of the :latest image before starting (default: true)')
@click.option('-d', '--detach', type=click.BOOL, is_flag=True, help="Run containers in the background")
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def start(build, detach, verbose):
  """Start the development environment defined in ./hokusai/development.yml"""
  set_verbosity(verbose)
  hokusai.dev_start(build, detach)


@dev.command(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def stop(verbose):
  """Stop the development environment defined in ./hokusai/development.yml"""
  set_verbosity(verbose)
  hokusai.dev_stop()


@dev.command(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def status(verbose):
  """Print the status of the development environment defined in ./hokusai/development.yml"""
  set_verbosity(verbose)
  hokusai.dev_status()


@dev.command(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
@click.option('-f', '--follow', type=click.BOOL, is_flag=True, help="Follow output")
@click.option('-t', '--tail', type=click.INT, help="Number of lines of recent logs to display")
def logs(follow, tail, verbose):
  """Print logs from the development environment defined in ./hokusai/development.yml"""
  set_verbosity(verbose)
  hokusai.dev_logs(follow, tail)


@dev.command(context_settings=CONTEXT_SETTINGS)
@click.argument('command')
@click.option('--service-name', type=click.STRING, default=config.project_name, help="The service name to launch the container as (default: %s)" % config.project_name)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def run(command, service_name, verbose):
  """Run a command in a new container in the development environment defined in ./hokusai/development.yml"""
  set_verbosity(verbose)
  hokusai.dev_run(command, service_name)


@dev.command(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def clean(verbose):
  """Stop and remove all containers in the development environment defined in ./hokusai/development.yml"""
  set_verbosity(verbose)
  hokusai.dev_clean()
