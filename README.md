# MaskRCNN ML Flask App
------

## Running locally

1. Clone repo with submodules
2. 
    $ git clone --recurse-submodules git@github.com:charyeezy/mrcnn-docker.git

3. Set up [Conda](https://www.anaconda.com/distribution/) or virtual environment and install reqs for frontend and backend

    $ conda env create -f environment.yml
    $ conda activate mrcnn

4. Set up MaskRCNN project and pycoco tools
   
   $ cd backend/Mask_RCNN && python3 setup.py install
   $ cd coco/PythonAPI && make

5. Download Coco weights
   
    $ wget -O backend/mask_rcnn_coco.h5 https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5


6. Install Jupyter kernel and make sure mrcnn-predict runs with this kernel
   python -m ipykernel install --user --name mrcnn 

7. Jupyter Gateway
   
   $ jupyter kernelgateway --KernelGatewayApp.api='kernel_gateway.notebook_http' --KernelGatewayApp.ip=0.0.0.0 --KernelGatewayApp.port=9090 --KernelGatewayApp.seed_uri=mrcnn-predict.ipynb --KernelGatewayApp.allow_origin='*'


## Running Flask in HTTPS

1. Use self-signed certificates using [openssl](https://www.openssl.org/source/)

    $ cd frontend/src && openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365


## Build DockerFiles

1. Create data volume
    $ docker volume create --name mrcnn-data

2. Create a user-defined bridge using built-in `bridge` network driver for app

    $ docker network create mrcnn-net

3. Build and run frontend docker with data volume

    $ docker build --rm -f "frontend/DockerFile" -t mrcnn-frontend:latest "frontend"
    $ docker run --network mrcnn-net -itd --rm --name mrcnn-frontend -p 5000:5000  -v  mrcnn-data:/app mrcnn-frontend 

4.  Build and run backend docker with data volume and connect 

    $ docker build --rm -f "backend/DockerFile" -t mrcnn-backend:latest "backend"
    $ docker run --network mrcnn-net -it --rm --name mrcnn-backend -p 9001:8888  -p 9090:9090 --volumes-from mrcnn-frontend mrcnn-backend 

5. [Optional] Run with Jupyter notebook to edit
    $ docker run --network mrcnn-net -it --rm --name mrcnn-backend -p 9001:8888  -p 9090:9090 --volumes-from mrcnn-frontend mrcnn-backend  jupyter notebook --allow-root 



## Frontend

1. Upload pictures using [Flask-Dropzone](https://github.com/greyli/flask-dropzone)
2. Shows prediction returned from model

## Backend

Matterport's [MaskRCNN](https://github.com/matterport/Mask_RCNN) is main model. The HTTP REST API is hosted using a [Jupter Kernel Gateway](https://github.com/jupyter/kernel_gateway) in Jupyter notebook. 


## Get Docker IP

    $ docker network inspect mrcnn-net
    $ docker inspect <containerNameOrId> | grep '"IPAddress"' | head -n 1