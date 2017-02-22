import os
import signal

from subprocess import call

from hokusai.config import HokusaiConfig
from hokusai.common import print_red, EXIT_SIGNALS

def development(rebuild):
  HokusaiConfig().check()
  docker_compose_yml = os.path.join(os.getcwd(), 'hokusai/development.yml')
  if not os.path.isfile(docker_compose_yml):
    print_red("Yaml file %s does not exist." % docker_compose_yml)
    return -1

  def cleanup(*args):
    return 0

  for sig in EXIT_SIGNALS:
    signal.signal(sig, cleanup)

  if rebuild:
    command = "docker-compose -f %s up --build" % docker_compose_yml
  else:
    command = "docker-compose -f %s up" % docker_compose_yml

  call(command, shell=True)
