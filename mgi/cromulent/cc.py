import jinja2, os, yaml

def config_attributes():
    return [ "CROMWELL_ROOT_DIR", "LSF_DEFAULT_DOCKER", "LSF_DOCKER_VOLUMES", "LSF_JOB_GROUP",]
#--
 
def resources_dn():
    return os.path.join(os.path.dirname(__file__), "resources")
#--

def config_template_fn():
    return os.path.join(resources_dn(), "compute1.conf.jinja")
#--
