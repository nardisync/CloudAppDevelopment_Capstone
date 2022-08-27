/**
 * Get all databases
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {

  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
  const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
  });
  cloudant.setServiceUrl(params.COUCH_URL);

  let dbList = getDbs(cloudant);
  return { dbs: dbList };
}

// This method returns a promise, but IBM Cloud Function does not 
// wait for this promise to get resolved, so it returns an 
// empty promise as : '{}'
function getDbs(cloudant) {
    cloudant.getAllDbs().then((body) => {
        body.forEach((db) => {
            dbList.push(db);
        });
    }).catch((err) => { console.log(err); });
}


/*
Example of return:
    {
        "dbs": [
            "dealerships",
            "reviews"
        ]
    }

*/