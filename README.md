# Breast cancer prediction with linear regression with the help of ECR and ECS (Fargate)

First create one ec2 instance with ubuntu AMI / all traffic (only for demo) / 20gb this comfiguration.

Login to you server 

## Update the pacakages:

    sudo apt-get update

## create and activate python env

    sudo apt install python3-venv -y
    python3 -m venv mlpro
    source mlpro/bin/activate   
    deactivate 

## Install AWSCLI
 
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    sudo apt install unzip -y
    unzip awscliv2.zip
    sudo ./aws/install 

## Configure the aws

    aws configure             

Install Docker:

    sudo vi docker-install.sh

    # Add Docker's official GPG key:
    sudo apt update
    sudo apt install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
    Types: deb
    URIs: https://download.docker.com/linux/ubuntu
    Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
    Components: stable
    Signed-By: /etc/apt/keyrings/docker.asc
    EOF

    sudo apt update -y
    sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
    docker --version
    sudo usermod -aG docker $USER         #OR you can use "newgrp docker" as a next commmand
    sudo chown $USER /var/run/docker.sock 
    sudo systemctl enable docker
    sudo systemctl start docker
    sudo systemctl status docker

    sudo chmod +x docker-install.sh
    ./docker-install.sh

## Clone the repo

    git clone https://github.com/vipulwarthe/breast-cancer-LR-ML-model-deploy-on-ecs.git
    cd <repo name>

    pip install -r requirements.txt

## select the kernel and Run the notebook 

    pip install ipykernel

## Run the application

    python app.py

## copy the public IP along with 5000 port to access the application as per below url

    http://<public ip>:5000/predict?s1=-0.96666522&s2=0.32786912&s3=-0.93579507&s4=-0.91104225&s5=0.60962671&s6=0.36569592&s7=-0.10914833&s8=-0.62181482&s9=-0.63860111&s10=0.53651178&s11=-0.46379509&s12=0.5132434&s13=-0.45632075&s14=-0.59189989&s15=0.67370318&s16=1.26928541&s17=2.17185315&s18=1.12535098&s19=0.64821758&s20=1.09244461&s21=-0.96440581&s22=-0.08750638&s23=-0.94145109&s24=-0.84547739&s25=-0.07511418&s26=-0.01862761&s27=-0.10400188&s28=-0.47718048&s29=-0.5634723&s30=0.05526303

## Login to the AWS and create one ECR repo "cancer-app-repo" and use push commands to login into ECR

    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 459499397844.dkr.ecr.us-east-1.amazonaws.com
    docker build -t breast-cancer-repo .
    docker tag breast-cancer-repo:latest 459499397844.dkr.ecr.us-east-1.amazonaws.com/breast-cancer-repo:latest
    docker push 459499397844.dkr.ecr.us-east-1.amazonaws.com/breast-cancer-repo:latest

* Create one ECS cluster "cancer-app-cluster" with serverless Fargate compute configuration, create IAM role or it will create by deafault for us, other settings use default and create the cluster.
  
* create New Task Defination - give the name for task defination family (cancer-new-task) - Launch type - AWS Fargate - other configration requirements default - 
- container 1 - Name(cancer-app) - Image URl - add container port - 5000-TCP-HTTP - Other settings default - Log collection - untick - other settings default - create task
 
* go to the cluster - Services - Service details - Task definition family name - Service name - Environment(existing cluster) - compute configuration - capacity provider stratigy -
- capacity provider -fargate - Deployment configuration - Scheduling strategy (select Replica) - desired task -1 - other setting related to deployment default - Networking - select security group with selected port 5000
- other setting default - create service

- go to the Task tab - click on Task - copy public ip - paste into browser with 5000 port with input values
  
- http://<public ip>:5000/predict?s1=-0.96666522&s2=0.32786912&s3=-0.93579507&s4=-0.91104225&s5=0.60962671&s6=0.36569592&s7=-0.10914833&s8=-0.62181482&s9=-0.63860111&s10=0.53651178&s

## you will successfully get the prediction

Hurray! finally my CancerApp is in operation. Now when we copy the URL in the browser, it predicted the result as ‘0’ which means a patient is diagnosed as Benign for breast cancer.
  


