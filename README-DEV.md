
## Migrations in live system:

https://medium.com/walkin/database-migration-writing-scripts-best-practices-3634c2134782

## Troubleshooting:


### Problem
The 'ERROR [root] Error: Target database is not up to date.' occurs.

### Solution:

Read and apply from here:
https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date



Mirrow repo between github and gitlab

https://docs.gitlab.com/ee/ci/ci_cd_for_external_repos/github_integration.html


Setup gitlab CI/CD with docker-compose

Requirements:
* Remote server
* docker installed

1. SCP in you remote server and follow these instructions to install gitlab-runner:

https://docs.gitlab.com/runner/install/index.html

2. Next register your gitlab-runner with you repo following:

https://docs.gitlab.com/runner/register/index.html

3. Next setup .gitlab-ci.yml file:


# This file is a template, and might need editing before it works on your project.
# see https://docs.gitlab.com/ce/ci/yaml/README.html for all available options

# you can delete this line if you're not using Docker
image: busybox:latest

before_script:
  - echo "Before script section"
  - echo "For example you might run an update here or install a build dependency"
  - echo "Or perhaps you might print out some debugging details"

after_script:
  - echo "After script section"
  - echo "For example you might do some cleanup here"

build1:
  stage: build
  script:
    - echo "Do your build here"

test1:
  stage: test
  script:
    - echo "Do a test here"
    - echo "For example run a test suite"

test2:
  stage: test
  script:
    - echo "Do another parallel test here"
    - echo "For example run a lint test"

deploy1:
  stage: deploy
  script:
    - echo "Do your deploy here"

Example:

https://gitlab.com/right.basedonscience/right_database/-/blob/master/.gitlab-ci.yml

Further Reading:
https://medium.com/@sean_bradley/auto-devops-with-gitlab-ci-and-docker-compose-f931233f080f
https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
Very complete example to deploy Flask App:
https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/

Video to deploy via gitlab/gitlab-runner
https://www.youtube.com/watch?v=RV0845KmsNI&t=191s
