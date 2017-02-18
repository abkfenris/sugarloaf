import copy
import os

from fabric.api import local, prompt
from fabric.contrib.console import confirm
import yaml
from git import repo



def _image_version(config):
    """
    Returns the image and version from a Kubernetes config
    """
    image_version = config['spec']['template']['spec']['containers'][0]['image']
    image, version = image_version.split(':')
    return image, version

def _tag(image, version):
    return image + ':' + str(version)

def _build(image, version, directory):
    """
    Builds a docker image from directory after confirmation
    """
    tag = _tag(image, version)
    if confirm('Build new {t}?'.format(t=tag)):
        print('')
        local('docker build -t {t} {d}'.format(t=tag, d=directory))

def _push(image, version):
    """
    Pushes image to gcloud
    """
    tag = _tag(image, version)
    if confirm('Push image {t} to gcloud?'.format(t=tag)):
        print('')
        local('gcloud docker -- push {t}'.format(t=tag))


def deploy_web():
    """
    Deploy the updated web container to kubernetes
    """
    config_path = 'k8s/web.yaml'

    with open(config_path) as f:
        config = yaml.safe_load(f)
        image, version = _image_version(config)
    
    print('Current version {v} for image {i}'.format(v=version, i=image))

    new_version = prompt('New version:')
    print('')

    _build(image, new_version, '.')
    print('')
    
    _push(image, new_version)
    print('')