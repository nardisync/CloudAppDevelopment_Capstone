const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

/* -------------------------------------------------------------------------------- */

// As the other functions, it returns the database names, but uses async await keywords.
// It make promise driven code easier to read and write
async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);
    try {
        let dbList = await cloudant.getAllDbs();
        console.log({ "dbs": dbList.result })
        return { "dbs": dbList.result };
    } catch (error) {
        console.log( { error: error.description })
        return { error: error.description };
    }
}

/* -------------------------------------------------------------------------------- */

// This function return all the Dealerships in the database dbName
// as a JSON format 
async function getAllDealerships(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    const dbName = 'dealerships'
    cloudant.setServiceUrl(params.COUCH_URL);
    try {
        let dbDealershipsDocs = await cloudant.postAllDocs({ db: dbName, includeDocs: true, })
        //dbDealershipsDocs.result.rows.forEach(element => console.log(element['doc']))
        console.log(dbDealershipsDocs.result.rows)
        return dbDealershipsDocs.result.rows

    } catch (error) {
        if (error.status == "404") {
            console.log("404: The database is empty")
            console.log(error.body)
        }
        else if (error.status == "500") {
            console.log("500: Something went wrong on the server")
            console.log(error.body)
        }
        else{
            console.log(error)
        }
        return { error: error.body };
    }
}

/* -------------------------------------------------------------------------------- */

// This function return all the Dealerships in the database dbName 
// with the 'selector' filter as a JSON format 
// Example : selector = {
//              'st': 'XX'
//           }
//  It returns all the entries with the state abbr. as 'XX'

async function getAllDealershipsWithState(params, selector) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    const dbName = 'dealerships'
    cloudant.setServiceUrl(params.COUCH_URL);

    try {
        let dbDealershipsDocs = await cloudant.postFind({ db: dbName, selector:selector})
        console.log(dbDealershipsDocs.result)
        return dbDealershipsDocs.result

    } catch (error) {
        if (error.status == "404") {
            console.log("404: The state does not exist")
            console.log(error.body)
        }
        else if (error.status == "500") {
            console.log("500: Something went wrong on the server")
            console.log(error.body)
        }
        else{
            console.log(error)
        }
        return { error: error.body };
    }
}

/* -------------------------------------------------------------------------------- */
/* ------------------------------ Testing the functions --------------------------- */
/* -------------------------------------------------------------------------------- */
temp_params = {
    "COUCH_URL": "NONE",
    "IAM_API_KEY": "NONE"
}
temp_selector = {
    'st': 'XX'
}

//main (temp_params)
//getAllDealerships(temp_params)
//getAllDealershipsWithState(temp_params, temp_selector)

