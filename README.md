# **Ganimedes Bot**
## Jupiter conversational recommender system

[logo]: ./public/ganimedes-logo.png

## **Get Started**
To get started with `Ganimedes`, clone this repository locally and install the following prerequisites:

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

