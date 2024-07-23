<a href="https://laurenzsommerlad.com"><img src="https://img.shields.io/badge/website-000000?style=for-the-badge&logo=About.me&logoColor=white" alt="Personal Website"/></a>
<a href="https://github.laurenzsommerlad.com"><img src="https://img.shields.io/badge/github%20pages-121013?style=for-the-badge&logo=github&logoColor=white" alt="Github Pages - About Me"/></a>
<a href="https://github.com/LaurenzSommerlad" target="_blank"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Profile"/></a>
<a href="https://gitlab.com/LaurenzSommerlad" target="_blank"><img src="https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white" alt="GitLab Profile"/></a>

## The Dream Team - Hackathon 2nd Place AI in Medicine Challenge 🥈
### Detection of rare child diseases by applying graph machine learning to a remote dataset with federated machine learning
<br>

![Team Photo](https://github.com/LaurenzSommerlad/TUM.ai-Makeathon2024-Amigo-Challenge/assets/36761347/78b360be-0c70-4f10-91ef-2664a297fb40)


This challenge was part of the <a href="https://makeathon.tum-ai.com" target="_blank">TUM.ai Makeathon 2024</a> provided by CareForeRare Foundation in Cooperation with LMU, Capegini, MI4People, FeatureCloud, Neo4j and Dr. von Hauner Children's Hospital.

### Inspiration
We chose this federated learning-based graph neural network project because of the value and impact it could have in rare disease prediction among children across the world.

### What it does
It accurately predicts if a child is healthy or diagnosed with a rare disease. Moreover, we can predict the patients’ disease categories based on the first letter of the ICD-10 code system.

### How we built it
If a patient has one or more phenotypes and genes, we used a random forest to perform classification. We also implemented the first notions of graph neural networks. The application is made with Python and pushed to FeatureCloud inside a docker container.

### Challenges we ran into
The first challenge was to get the docker container running on the FeatureCloud infrastructure. We faced many timeout issues related to our neo4j queries. Furthermore, we did not have direct access to the production data. This means we could initially only explore and train on the synthetic dataset, which was unfortunately not relatable. Another challenge was retrieving the logs from the feature cloud, which needed to be sent always manually through Discord.

### Accomplishments that we are proud of
We were the first team with a submission and working solution, having good initial scores and utilizing innovative ML algorithms to perform binary and multi-label classification. We also implemented a Graph Machine Learning approach on a separate branch, which unfortunately could not yet be tested due to infrastructure limitations.

### What we learned
How to work with Cypher to query the graph-based database neo4j. How to work with the FeatureCloud infrastructure and Federated Machine Learning, classification algorithms, graph neural networks, and ultimately the medical context that is the prerequisite of understanding the correlations between genes, proteins, phenotypes, and the respective diseases.
to start development you require python and a Docker Setup.

## Authors
- <a href="https://laurenzsommerlad.com" target="_blank">Laurenz Sommerlad</a> <a href="https://www.linkedin.com/in/laurenzsommerlad/" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white" alt="LinkedIn"/></a><br>
- [Sandhanakrishnan Ravichandran](https://www.linkedin.com/in/sandhanakrishnanr/) <br>
- [Roman Mishchuk](https://www.linkedin.com/in/roman-mishchuk-0ab260bb/) <br>
- [Martin Mohammed](https://www.linkedin.com/in/martin-mohammed-30019a207/)

## Project Links

- <a href="https://devpost.com/software/the-dream-team-7uik58" target="_blank">Devpost Submission</a><br>
- <a href="https://tum-ai.notion.site/AI-in-Medicine-Project-AMIGO-d882e781fbfc4056b474fee54cdb0b2f" target="_blank">AI in Medicine: Project AMIGO Challenge & Instructions</a><br>
- <a href="https://github.com/LaurenzSommerlad/TUM.ai-Makeathon2024-Amigo-Challenge" target="_blank">Github Repo</a>

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

### How to run this application with docker-compose. 

```docker-compose up -d ```

This command performs similar actions to the previous lengthy Docker command. It builds the Docker image and tags it as featurecloud.ai/dreamteam:latest, sets up local volume mappings, and opens the corresponding ports.

## More Hackathons
- <a href="https://makeathon.tum-ai.com" target="_blank">TUM.ai Makeathon</a> 2023 Applied AI Challenge
  - Description: web-based chatbot that combines the strengths of ChatGPT, Cohere Summarizer, and a detailed questionnaire to ideate on AI use cases and business models
  - <a href="https://devpost.com/software/appliedai_canai" target="_blank" rel="nofollow noopener noreferrer">Devpost Submission</a>
  - <a href="https://github.com/LaurenzSommerlad/tum.ai-makeathon2023-frontend" target="_blank">Gatsby Frontend with Tailwind CSS</a>
  - <a href="https://github.com/LaurenzSommerlad/TUM.ai-Makeathon2023-API-Endpoint/" target="_blank">FastAPI Backend</a>

Organized by <a href="https://www.tum-ai.com" target="_blank">TUM.ai e.V.</a>

## Contact ##
<a href="https://laurenzsommerlad.com" rel="me"><img src="https://img.shields.io/badge/website-000000?style=for-the-badge&logo=About.me&logoColor=white" alt="Personal Website"/></a>
<a href="https://www.linkedin.com/in/laurenzsommerlad" target="_blank" rel="me"><img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
<a href="https://x.com/Lauros_World" target="_blank" rel="me"><img src="https://img.shields.io/badge/X-%23000000.svg?style=for-the-badge&logo=X&logoColor=white" alt="X (Former Twitter)"/></a>
<a href="https://www.instagram.com/laurenzsommerlad/" target="_blank" rel="me"><img src="https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=Instagram&logoColor=white" alt="Instagram"/></a>
<a href="https://www.threads.net/@laurenzsommerlad" target="_blank" rel="me"><img src="https://img.shields.io/badge/Threads-000000?style=for-the-badge&logo=Threads&logoColor=white" alt="Threads"/></a>
<a href="https://www.youtube.com/@LaurenzSommerlad" target="_blank" rel="me"><img src="https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white" alt="YouTube Channel"/></a>
<a href="https://www.facebook.com/LaurenzSommerlad.official/" target="_blank" rel="me"><img src="https://img.shields.io/badge/Facebook-%231877F2.svg?style=for-the-badge&logo=Facebook&logoColor=white" alt="Facebook"/></a>
<a href="https://mastodon.social/@LaurenzSommerlad" target="_blank" rel="me"><img src="https://img.shields.io/badge/-MASTODON-%232B90D9?style=for-the-badge&logo=mastodon&logoColor=white" alt="Mastodon"/></a>
<a href="https://linktr.ee/LaurenzSommerlad" target="_blank" rel="me"><img src="https://img.shields.io/badge/linktree-1de9b6?style=for-the-badge&logo=linktree&logoColor=white" alt="Linktree"/></a>
