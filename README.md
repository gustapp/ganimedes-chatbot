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

6. Start Local Server (DEBUG mode)

    - Launch `Python: Flask` on `main_emulate.py` file
        . It should start the server on port 5000

### **Pre-requesites**

* [NodeJS](https://nodejs.org/en/) + [NPM](https://www.npmjs.com/)

    > `apt install nodejs npm` 

* [Google Cloud Functions Emulator](https://cloud.google.com/functions/docs/emulator)

    > `npm install -g @google-cloud/functions-emulator`

* [Firebase Tools](https://firebase.google.com/docs/cli/?hl=en-us)

    > `npm install -g firebase-tools`

* [VSCode](https://code.visualstudio.com/)

* [Dialogflow Project Setup](https://dialogflow.com/)

* [Firebase Project Setup](https://firebase.google.com/)

### **Debug locally**

1. Install all project dependencies *(functions folder)*

    > `npm install`

2. Build project *(functions folder)*

    > `npm run build`

3. Start functions

    > `functions start`

4. Deploy functions

    > `functions deploy dialogflowFirebaseFulfillment --trigger-http`

5. Inspect functions

    > `functions inspect dialogflowFirebaseFulfillment`

6. Debug in VSCode

    Launch `Cloud functions debug` configurations at **launch.json**. Now, just debug the code!

7. Realize a call (*using mock file*)

    > `functions call dialogflowFirebaseFulfillment --f='./test/mock/getCourseInfo.json'`

### **Run Tests**

Currently, this project uses **Jest** to run its *Unit Tests* for each cloud functions. The tests consists basically on mocked calls (*mock folder*).

To run the test, execute the previous section steps from **1** to **4**. After that, execute the following at *functions folder*:

> `npm run test`

curl -X POST -H "Content-Type: application/json" -d @./functions/test/mock/getConceptDescription.json http://localhost:5000/dialogflow-fulfillment


### **TODOS**

- Create make.sh
- Fix get explanation and context
- Move tests to pytest (deco supertest .ts)

- Rethink deploy
