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

    data_array.forEach(data_item => moveFieldToCollection(data_item))
});

/**
 * @library
 * Tooling functions
 */
function addData(document){
    coursesRef.doc(document.sigla).set(document).then(docRef => {
        console.log("success: ", docRef.id);
    })
    .catch(error => {
        console.log("Error on write: ", error);
    });
}

function moveFieldToCollection(document){
    document.oferecimento.forEach(item => {
        item.horario.forEach(schedule => {
            let offerDocRef = coursesRef.doc(document.sigla).collection("oferecimentos").doc(item.codigo_turma)
            .update({
                horario: firebase.firestore.FieldValue.delete()
            }).then(info => {
                console.log("success ", info)
            })
            .catch(err => {
                console.log("error ", err)
            })

            // let count = 0;
            // offerDocRef.collection("horarios").add(schedule)
            // .then(docRef => {
            //     count++;
            //     console.log(`success: ${docRef.id} ${count}`);
            // })
            // .catch(error => {
            //     console.log("Error on write: ", error);
            // });
        })
        // .update({
        //     oferecimento: firebase.firestore.FieldValue.delete()
        // }).then(info => {
        //     console.log("success ", info)
        // })
        // .catch(err => {
        //     console.log("error ", err)
        // })
        // .collection("oferecimentos").doc(item.codigo_turma).set(item)
        // .then(docRef => {
        //     console.log("success:");
        // })
        // .catch(error => {
        //     console.log("Error on write: ", error);
        // });


        // .collection("oferecimentos").doc(item.codigo_turma).get()
        // .then(doc => {
        //     if (!doc.exists) {
        //         console.log('No such document!');
        //     } else {
        //         let offer = doc.data();
        //         offer.horario.forEach(schedule => {
        //             let count = 0;
        //             doc.ref.collection("horarios").set(schedule).then(docRef => {
        //                 console.log("success: ", count);
        //                 count++;
        //             })
        //             .catch(error => {
        //                 console.log("Error on write: ", error);
        //             });
        //         })
        //     }
        // })
        // .catch(error => {
        //     console.log("Error on write: ", error);
        // });
    })
}