import os, json, datetime, sys
from operator import attrgetter
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.image import Image
from azureml.core.compute import AksCompute, ComputeTarget
from azureml.core.webservice import Webservice, AksWebservice
from azureml.core.authentication import AzureCliAuthentication

cli_auth = AzureCliAuthentication()
# Get workspace
ws = Workspace.from_config(auth=cli_auth)


image_name = "model-image"

images = Image.list(workspace=ws)

images = (m for m in images if m.name == image_name)

image = max(images, key=attrgetter('version'))
# print('From Max Version, Image used to deploy webservice on ACI: {}\nImage Version: {}\nImage Location = {}'.format(image.name, image.version, image.image_location))

# Check if AKS already Available
aks_service_name = "aks-service"
try:
    service = Webservice(name=aks_service_name, workspace=ws)
    service.update(image=image)
except:
    aks_target = AksCompute(ws,"akscompute")
    aks_config = AksWebservice.deploy_configuration(enable_app_insights=False)
    service = Webservice.deploy_from_image(
        workspace=ws,
        name=aks_service_name,
        image=image,
        deployment_config=aks_config,
        deployment_target=aks_target,
    )