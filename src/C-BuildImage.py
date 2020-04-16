import os, json, sys
from azureml.core import Workspace
from azureml.core.image import ContainerImage, Image
from azureml.core.model import Model
from azureml.core.authentication import AzureCliAuthentication

#os.chdir("./code")

cli_auth = AzureCliAuthentication()
ws = Workspace.from_config(auth=cli_auth)

model = Model(ws, "Model")

image_config = ContainerImage.image_configuration(execution_script = "score.py",
                                                runtime = "python",
                                                 conda_file = "conda.yml",
                                                 description = "Predict regression",
                                                 tags = {"regression": "classification",  "classification" : "ml"}
                                                 )

image = ContainerImage.create(name = "model-image", 
                              models = [model], 
                              image_config = image_config,
                              workspace = ws
                              )