=========================
How to launch the project
=========================

Navigate to OUAP-4314/Evaluation/Projet and start the containers:

.. code-block:: bash

    docker-compose up

Check if the containers are up using either:

.. code-block:: bash

    docker-compose ps

or:

.. code-block:: bash

    docker ps

Gracefully shut the containers down:

.. code-block:: bash

    docker-compose down

Note: the main docker-compose.yml works well with Debian operating systems. With a macos system, use the docker-compose_for_mac.yml file with the following command:

.. code-block:: bash

    docker-compose -f docker-compose_for_mac.yml up
