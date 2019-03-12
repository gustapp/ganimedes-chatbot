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

/**
 * @method ExportToCSV
 * Read data from json file and populate firestore with its data
 */
const fs = require('fs');

const coursesRef = firestore.collection("cursos"); /* Source collection */

/**
 * @function toCsv
 * Extract data of interest and realize some pre pre processing
 */
function toCsv(doc){
    let fields = [
        doc.name,
        doc.objetivos,
        doc.programa,
        doc.programa_resumido
    ]

    fields_clean = fields.map(field => field.replace(/,/g, ''))

    return fields_clean.join(',') + '\n'
}

const filePath = './scripts/dataset/courses_descriptions.csv';

const csvHeader = 'Curso,Objetivos,Programa,Resumo\n';

fs.writeFile(filePath, csvHeader, (err) => {
    if (err) throw err;
    console.log('The file has been initialized!');

    coursesRef.get().then(querySnapshot => {
        querySnapshot.forEach(doc => {
            let course_data = toCsv(doc.data());
    
            fs.appendFile(filePath, course_data, (err) => {
                if (err) throw err;
                console.log('success doc: ', doc.id);
            });
        });
    })
    .catch(function(error) {
        console.log("Error getting documents: ", error);
    });    
}); 
