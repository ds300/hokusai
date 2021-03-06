from hokusai.lib.command import command
from hokusai.lib.common import print_red, print_green, shout
from hokusai.services.deployment import Deployment
from hokusai.services.ecr import ECR

@command()
def gitlog():
  ecr = ECR()

  staging_deployment = Deployment('staging')
  staging_tag = staging_deployment.current_tag
  if staging_tag is None:
    raise HokusaiError("Could not find a tag for staging.  Aborting.")
  staging_tag = ecr.find_git_sha1_image_tag(staging_tag)
  if staging_tag is None:
    raise HokusaiError("Could not find a git SHA1 tag for tag %s.  Aborting." % staging_tag)

  production_deployment = Deployment('production')
  production_tag = production_deployment.current_tag
  if production_tag is None:
    raise HokusaiError("Could not find a tag for production.  Aborting.")
  production_tag = ecr.find_git_sha1_image_tag(production_tag)
  if production_tag is None:
    raise HokusaiError("Could not find a git SHA1 for tag %s.  Aborting." % production_tag)

  print_green("Comparing %s to %s" % (production_tag, staging_tag))
  shout("git log --right-only %s..%s" % (production_tag, staging_tag), print_output=True)
