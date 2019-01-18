/**
 * @function Hammer
 * Manually add data to firestore
 */

/**
 * Load app config from app.config.js (do not commit this file)
 */
const config = require('./app.config');
const firebase = require('firebase');

firebase.initializeApp(config);

const firestore = firebase.firestore();
const settings = { timestampsInSnapshots: true };
firestore.settings(settings);

const coursesRef = firestore.collection("cursos"); /* Destination collection */

/**
 * @method ManualFill
 * Read data from json file and populate firestore with its data
 */
const fs = require('fs');
var data_file = './scripts/dataset/courses_data.json'; /* Source file */

fs.readFile(data_file, 'utf8', function (err, data) {
    if (err) throw err;
    var data_array = JSON.parse(data);

    data_array.forEach(data_item => addData(data_item))
});

function addData(document){
    coursesRef.doc(document.sigla).set(document);
}