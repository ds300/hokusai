import click

import hokusai

from hokusai.cli.base import base
from hokusai.cli.staging import KUBE_CONTEXT
from hokusai.lib.common import set_verbosity, CONTEXT_SETTINGS, clean_string
from hokusai.lib.config import config

@base.group()
def review_app(context_settings=CONTEXT_SETTINGS):
  """Create/Manage review apps"""
  pass

@review_app.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
@click.option('-sf', '--source-file', type=click.STRING, default='hokusai/staging.yml', help="The source yaml file from which to create the new resource file (default: hokusai/staging.yml)")
def setup(app_name, verbose, source_file):
  """Setup a new review-app - create a Yaml file based on APP_NAME and --source-file"""
  set_verbosity(verbose)
  hokusai.create_new_app_yaml(source_file, app_name)


@review_app.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def create(app_name, verbose):
  """Creates the Kubernetes based resources defined in ./hokusai/{APP_NAME}.yml"""
  hokusai.k8s_create(KUBE_CONTEXT, tag=app_name, namespace=clean_string(app_name), yaml_file_name=app_name)


@review_app.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def delete(app_name, verbose):
  """Deletes the Kubernetes based resources defined in ./hokusai/{APP_NAME}.yml"""
  set_verbosity(verbose)
  hokusai.k8s_delete(KUBE_CONTEXT, namespace=clean_string(app_name), yaml_file_name=app_name)


@review_app.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def update(app_name, verbose):
  """Updates the Kubernetes based resources defined in ./hokusai/{APP_NAME}.yml"""
  set_verbosity(verbose)
  hokusai.k8s_update(KUBE_CONTEXT, namespace=clean_string(app_name), yaml_file_name=app_name)


@review_app.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.option('--resources/--no-resources', default=True, help='Print Kubernetes API objects defined in ./hokusai/APP_NAME.yml (default: true)')
@click.option('--pods/--no-pods', default=True, help='Print pods (default: true)')
@click.option('--describe', type=click.BOOL, is_flag=True, help="Print 'kubectl describe' output")
@click.option('--top', type=click.BOOL, is_flag=True, help='Print top pods')
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def status(app_name, resources, pods, describe, top, verbose):
  """Print the Kubernetes resources status defined in the staging context / {APP_NAME} namespace"""
  set_verbosity(verbose)
  hokusai.k8s_status(KUBE_CONTEXT, resources, pods, describe, top, namespace=clean_string(app_name), yaml_file_name=app_name)


@review_app.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.argument('command', type=click.STRING)
@click.option('--tty', type=click.BOOL, is_flag=True, help='Attach the terminal')
@click.option('--tag', type=click.STRING, help='The image tag to run (defaults to APP_NAME)')
@click.option('--env', type=click.STRING, multiple=True, help='Environment variables in the form of "KEY=VALUE"')
@click.option('--constraint', type=click.STRING, multiple=True, help='Constrain command to run on nodes matching labels in the form of "key=value"')
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def run(app_name, command, tty, tag, env, constraint, verbose):
  """Launch a new container and run a command"""
  set_verbosity(verbose)
  if tag is None:
    tag = clean_string(app_name)
  hokusai.run(KUBE_CONTEXT, command, tty, tag, env, constraint, namespace=clean_string(app_name))


@review_app.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.option('-s', '--timestamps', type=click.BOOL, is_flag=True, help='Include timestamps')
@click.option('-f', '--follow', type=click.BOOL, is_flag=True, help='Follow logs')
@click.option('-t', '--tail', type=click.INT, help="Number of lines of recent logs to display")
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def logs(app_name, timestamps, follow, tail, verbose):
  """Get container logs"""
  set_verbosity(verbose)
  hokusai.logs(KUBE_CONTEXT, timestamps, follow, tail, namespace=clean_string(app_name))


@review_app.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.argument('tag', type=click.STRING)
@click.option('--migration', type=click.STRING, help='Run a migration before deploying')
@click.option('--constraint', type=click.STRING, multiple=True, help='Constrain migration and deploy hooks to run on nodes matching labels in the form of "key=value"')
@click.option('--git-remote', type=click.STRING, help='Push deployment tags to git remote')
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def deploy(app_name, tag, migration, constraint, git_remote, verbose):
  """Update the project's deployment(s) to reference the given image tag"""
  set_verbosity(verbose)
  hokusai.update(KUBE_CONTEXT, tag, migration, constraint, git_remote, namespace=clean_string(app_name), resolve_tag_sha1=False)


@review_app.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.option('-d', '--deployment', type=click.STRING, help='Only refresh the given deployment')
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def refresh(app_name, deployment, verbose):
  """Refresh the project's deployment(s) by recreating the currently running containers"""
  set_verbosity(verbose)
  hokusai.refresh(KUBE_CONTEXT, deployment, namespace=clean_string(app_name))


@review_app.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.option('-d', '--deployment', type=click.STRING, help='Only refresh the given deployment')
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def restart(app_name, deployment, verbose):
  """Alias for 'refresh'"""
  set_verbosity(verbose)
  hokusai.refresh(KUBE_CONTEXT, deployment, namespace=clean_string(app_name))


@review_app.group()
def env(context_settings=CONTEXT_SETTINGS):
  """Interact with the runtime environment for the review app"""
  pass


@env.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def copy(app_name, verbose):
  """Copies the app's environment config map to the namespace {APP_NAME}"""
  set_verbosity(verbose)
  hokusai.k8s_copy_config(KUBE_CONTEXT, clean_string(app_name))


@env.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def create(app_name, verbose):
  """Create the Kubernetes configmap object `{project_name}-environment` in the {APP_NAME} namespace"""
  set_verbosity(verbose)
  hokusai.create_env(KUBE_CONTEXT, namespace=clean_string(app_name))


@env.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.argument('env_vars', type=click.STRING, nargs=-1)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def get(app_name, env_vars, verbose):
  """Print environment variables stored on the Kubernetes server"""
  set_verbosity(verbose)
  hokusai.get_env(KUBE_CONTEXT, env_vars, namespace=clean_string(app_name))


@env.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.argument('env_vars', type=click.STRING, nargs=-1)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def set(app_name, env_vars, verbose):
  """Set environment variables - each of {ENV_VARS} must be in of form 'KEY=VALUE'"""
  set_verbosity(verbose)
  hokusai.set_env(KUBE_CONTEXT, env_vars, namespace=clean_string(app_name))


@env.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.argument('env_vars', type=click.STRING, nargs=-1)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def unset(app_name, env_vars, verbose):
  """Unset environment variables - each of {ENV_VARS} must be of the form 'KEY'"""
  set_verbosity(verbose)
  hokusai.unset_env(KUBE_CONTEXT, env_vars, namespace=clean_string(app_name))


@env.command(context_settings=CONTEXT_SETTINGS)
@click.argument('app_name', type=click.STRING)
@click.option('-v', '--verbose', type=click.BOOL, is_flag=True, help='Verbose output')
def delete(app_name, verbose):
  """Delete the Kubernetes configmap object `{project_name}-environment`"""
  set_verbosity(verbose)
  hokusai.delete_env(KUBE_CONTEXT, namespace=clean_string(app_name))

