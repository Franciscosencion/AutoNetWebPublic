# AutoNetWeb

This is an open source work in progress project mainly focused on Network configuration management and automation. Project is being developed with **Django** and **Python** on the backend, and **HTML**, **CSS**, **JavaScript** on the front-end.

I will create a proper documentation that includes the functionalities already available, meanwhile, below are a brief description of some of the functionalities available:

1. Create Branches.
2. Register Network devices and associate them to a branch.
3. Support for model driven APIs such **RESTCONF**, and legacy API such **SSH** using **NetMiko**.
4. On routers only **retrieving configuration** and **interfaces** are available on **Cisco Devices** **only** at this moment.
5. On Switches, only **retrieving configuration**, **interfaces**, **changing port VLAN assignment**, **Synchronizing VLANs** are available using **RESTCONF** on **Cisco Devices only** at this moment.

For portability sake, I decided to use **SQLITE** as the database engine for this project, this is subject to modification in the future if I am in the need of a more scalable **DBMS** such **PostgreSQL** or **MySQL**.

**Note:** credentials used to interact with devices is separate from django built-in User Authentication system. Devices credentials are defined during creation of devices and store in the database as clear text which could present security risks depending on how and where you use this.

***Important***

Django Restful Framework API has been integrated to this project to perform task such registering devices, creating branches through API calls. REST framework is a collaboratively funded project. If you use REST framework commercially DRF developers strongly encourage you to invest in its continued development by [signing up for a paid plan](https://fund.django-rest-framework.org/topics/funding/).


If you have any questions, feel free to contact me at the emails below or at my **LinkedIn** profile **Francisco Sencion**:

- **francisco.sencion@gmail.com**
- **francisco.sencion@yahoo.com**


## Setup Instructions

1. Clone repository:
      ```
      git clone "repository"
      ```
2. Enabling virtual environment and installing dependencies using pipenv python module. You can install pipenv with **pip install pipenv**:
      ```
      pipenv install -r requirements.txt
      ```
3. Make Django migrations to setup the models:
      ```
      django manage.py makemigrations
      django manage.py migrate
      ```
4. Create Django Super User:
      ```
      python manage.py createsuperuser
      ```
5. Run Server:
      ```
      django manage.py runserver
      ```
6. Access application in your browser at **localhost:8000** and log in using the super user you created in step 4.

