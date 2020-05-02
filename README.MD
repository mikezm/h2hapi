## Description ##
This repository represents the back-end for the H2H site (WIP). 
Using an AWS serverless deployment model, this Flask API uses 

## Requirements ##
 - Python 3.7
 - NodeJS (for serverless install)
 - Serverless
 - DynamoDB
 - Docker
 
 ## Installation ##
 Download python3 and install. I recommend using `Virtualenv` or some other environment manager.
  
  - Install Serverless `npm -g install serverless`
  - Install sls python requirements: `sls plugin install -n serverless-python-requirements`
  - Clone the repo: `git clone https://github.com/mikezm/h2hapi.git`
  - Navigate to the folder: `cd h2hapi` and setup a virtual environment with something like `Virtualenv`.
  - Install python requirements: `pip install -r requirements.txt`
  - Make sure Docker is installed and pull the DynamoDB local container: `docker pull amazon/dynamodb-local`
 
 ## Environment Variables ##
 
 There are a fair amount of environment variables to install for the AWS and the DB itself. 
 To keep this a public repository no tokens, DB assets, or encryption keys are part of the solution. 
 
- H2H_API_ENV="dev"
- H2H_SECRET_KEY="YouRSecRetTokenKeyHere"
- H2H_HASH_ROUNDS=######## *(a large number 80-110K)*
- H2H_ADMIN_USERNAME="admin@email.com"
- H2H_ADMIN_PWD="adminPassWd"
- AWS_ACCESS_KEY_ID="YouRSecRetAWSAuthID"
- AWS_SECRET_ACCESS_KEY="YouRSecRetAWSAccessKey"
- USERS_TABLENAME="USERS_TABLE_NAME"
- BLTOKENS_TABLENAME="BLACKLISTED_TOKENS_TABLE_NAME"
- ARTICLES_TABLENAME="ARTICLES_TABLE_NAME"
- AWS_DEFAULT_REGION="aws-region"

 ## Running the API ##
 Start dynamoDB in Docker: `docker run -p 8000:8000 amazon/dynamodb-local`
 
 In detached mode: `docker run -d -p 8000:8000 amazon/dynamodb-local`
 
 Run the API: `make run` or `sls wsgi serve`
 Run Unit Tests: `make test`
 
 
 