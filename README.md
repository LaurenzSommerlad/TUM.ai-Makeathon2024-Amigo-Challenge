# The Dream Team
### Detection of rare child diseases by applying graph machine learning to a remote dataset with federated machine learning
<br>

![Team Photo](https://github.com/LaurenzSommerlad/TUM.ai-Makeathon2024-Amigo-Challenge/assets/36761347/78b360be-0c70-4f10-91ef-2664a297fb40)


This challenge was part of the TUM.ai Makeathon 2024 provided by CareForeRare Foundation in Cooperation with LMU, Capegini, MI4People, FeatureCloud, Neo4j and Dr. von Hauner Children's Hospital.

#### Inspiration
We chose this federated learning-based graph neural network project because of the value and impact it could have in rare disease prediction among children across the world.

#### What it does
It accurately predicts if a child is healthy or diagnosed with a rare disease. Moreover, we can predict the patients’ disease categories based on the first letter of the ICD-10 code system.

#### How we built it
If a patient has one or more phenotypes and genes, we used a random forest to perform classification. We also implemented the first notions of graph neural networks. The application is made with Python and pushed to FeatureCloud inside a docker container.

#### Challenges we ran into
The first challenge was to get the docker container running on the FeatureCloud infrastructure. We faced many timeout issues related to our neo4j queries. Furthermore, we did not have direct access to the production data. This means we could initially only explore and train on the synthetic dataset, which was unfortunately not relatable. Another challenge was retrieving the logs from the feature cloud, which needed to be sent always manually through Discord.

#### Accomplishments that we are proud of
We were the first team with a submission and working solution, having good initial scores and utilizing innovative ML algorithms to perform binary and multi-label classification. We also implemented a Graph Machine Learning approach on a separate branch, which unfortunately could not yet be tested due to infrastructure limitations.

#### What we learned
How to work with Cypher to query the graph-based database neo4j. How to work with the FeatureCloud infrastructure and Federated Machine Learning, classification algorithms, graph neural networks, and ultimately the medical context that is the prerequisite of understanding the correlations between genes, proteins, phenotypes, and the respective diseases.
to start development you require python and a Docker Setup.

#### Authors
[Laurenz Sommerlad](https://www.linkedin.com/in/laurenzsommerlad/) <br>
[Sandhanakrishnan Ravichandran](https://www.linkedin.com/in/sandhanakrishnanr/) <br>
[Roman Mishchuk](https://www.linkedin.com/in/roman-mishchuk-0ab260bb/) <br>
[Martin Mohammed](https://www.linkedin.com/in/martin-mohammed-30019a207/)
### FeatureCloud Setup
The Following example solution is build on https://github.com/FeatureCloud/app-round/

```
pip install virtualenv

python -m venv careforrare

# For Mac Users
source ./careforrare/bin/activate

# For Windows Users (use Powershell)
 ./careforrare/Scripts/Activate.ps1

# Install Requirements
pip install -r requirements.txt

# Develop your application with local environment you have to set local variables
# Please get in touch with the Care-For-Rare Team

# Build and push your container by facilitating makefile. Please change the name of DOCKER_IMAGE_NAME in your file
# if make does not work in your env please utilize statements in Makefile to create same results
make build

# to do a test run of your container with the following statement. In the logs you should see a server starting. When using Windows bases Systems we recognized mounting works better when triggering command directly in WSL System. 
docker run -d -v ./config.yml:/mnt/input/config.yml -v ./data/output:/mnt/output -p 9000:9000 featurecloud.ai/dreamteam:latest
# or on Windows:
docker run -d -v ${pwd}/config.yml:/mnt/input/config.yml -v ${pwd}/data/output:/mnt/output -p 9000:9000 featurecloud.ai/dreamteam:latest

# Trigger the start of the application states
curl --location 'http://localhost:9000/setup' --header 'Content-Type: application/json' --data '{"id": "0000000000000000","coordinator": false,"coordinatorID": "0000000000000000","clients": []}'

# Look at logs using. Make sure to close container after testing
docker logs <containerID>

# Push the new image to the registry
make push

Alternatively you are free to utilize the full functionalities of the feature-cloud api and Testbed
https://featurecloud.ai/developers

```

# How to run this application with docker-compose. 

```docker-compose up -d ```

This command performs similar actions to the previous lengthy Docker command. It builds the Docker image and tags it as featurecloud.ai/dreamteam:latest, sets up local volume mappings, and opens the corresponding ports.
