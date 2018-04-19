=========================
How to launch the project
=========================

You may first need to pull the Docker image for mongo from dockerhub:

.. code-block:: bash

    docker pull mongo

Navigate to OUAP-4314/Evaluation/Projet and start the containers:

.. code-block:: bash

    docker-compose up

You can also start the containers in detached mode and check their logs:

.. code-block:: bash

    docker-compose up -d
    docker-compose logs

Check if the containers are up:

.. code-block:: bash

    docker-compose ps

Gracefully shut the containers down:

.. code-block:: bash

    docker-compose down

Deploy the project on a Raspberry Pi:

.. code-block:: bash

    docker-compose -f rpi_docker-compose.yml up

Deploy the project on macOS:

.. code-block:: bash

    docker-compose -f mac_docker-compose.yml up

N.B.: the deployment is optimized for docker-compose. If you wish to launch each container separately,
some adjustements regarding the Mongo client instanciation are required, because with docker-compose,
a temporary Docker network is created to link the containers between them. Else the containers have to
connect to the MongoDB container with localhost and port 27017.

.. code-block:: bash

    client = MongoClient("localhost", 27017)

Instead of:

.. code-block:: bash
    
    client = MongoClient("mongo")
