# **Ganimedes Bot**
## Jupiter conversational recommender system

[logo]: ./public/ganimedes-logo.png

## **Get Started**
To get started with `Ganimedes`, clone this repository locally and install the following prerequisites:

1. Create conda environment

    > `conda create --name ganimedes --clone base`
    
    > `conda activate ganimedes`

2. Install dependencies

    > `cd functions/src`
    
    > `pip install -r requirements.txt`

3. Compile OpenKE

    > `cd model/kb/OpenKE`
    
    > `mkdir release`
    
    > `bash make.sh`

4. Train Knowledge Embedding

    > `mkdir -p ../artifacts/kge ../artifacts/dicts`
    
    > `python example_train_transe.py`
    
    > `python ../../../../../scripts/create_dicts.py`

5. Firebase Authentication Set-up
    
    - Follow the procedure available at (https://firebase.google.com/docs/admin/setup)
    - Make a new directory `auth` and paste the json file
    - In the file `main.py`, change the name of the json authentication file to reflect this change

6. Start Local Server (DEBUG mode)

    - Launch `Python: Flask` on `main_emulate.py` file
        . It should start the server on port 5000

### **Pre-requesites**

* [VSCode](https://code.visualstudio.com/) and install python extension

* [Conda](https://docs.conda.io/en/latest/miniconda.html)

* [Dialogflow Project Setup](https://dialogflow.com/)

* [Firebase Project Setup](https://firebase.google.com/)


### **Run Tests**

Currently, the tests consists basically on mocked calls (*mock folder*).

To run a test, execute the previous section steps from **1** to **4**. After that, execute the following command with the mocked call you want to simulate.

`curl -X POST -H "Content-Type: application/json" -d @./functions/test/mock/getConceptDescription.json http://localhost:5000/dialogflow-fulfillment`

### **TODOS**

- Create make.sh
- Fix get explanation and context
- Move tests to pytest (deco supertest .ts)

- Rethink deploy
