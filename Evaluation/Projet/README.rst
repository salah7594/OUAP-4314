=========================
How to launch the project
=========================

Navigate to OUAP-4314/Evaluation/Projet and start the containers:

.. code-block:: bash

    docker-compose up

You can also start the containers in detached mode and check their logs:

.. code-block:: bash

    docker-compose up -d
    docker-compose logs

Check if the containers are up using either:

.. code-block:: bash

    docker-compose ps

or:

.. code-block:: bash

    docker ps

Gracefully shut the containers down:

.. code-block:: bash

    docker-compose down
