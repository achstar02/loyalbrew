const https = require('https');
const projectId = 'loyalbrew-app-2f8c7';
const apiKey = 'AIzaSyAlHVGBROFf3aOjaMUSJy4nzomLHfXMcgg';

function fetchCollection(collection) {
  return new Promise((resolve, reject) => {
    const url = 'https://firestore.googleapis.com/v1/projects/' + projectId + '/databases/(default)/documents/' + collection + '?key=' + apiKey;
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          try { resolve(JSON.parse(data)); } catch(e) { resolve({error: 'parse error'}); }
        } else {
          resolve({error: 'http ' + res.statusCode});
        }
      });
    }).on('error', e => resolve({error: e.message}));
  });
}

async function main() {
  console.log('=== Firebase Firestore 结构检查 ===\n');
  
  const merchants = await fetchCollection('merchants');
  if (merchants.documents) {
    console.log('merchants 集合: ' + merchants.documents.length + ' docs');
    merchants.documents.forEach(doc => {
      const name = doc.name.split('/').pop();
      const fields = doc.fields;
      console.log('  - ' + name + ': ' + (fields.name ? fields.name.stringValue : '(no name)'));
    });
  } else {
    console.log('merchants: ' + (merchants.error || 'empty'));
  }
  
  const orders = await fetchCollection('merchants/test_shop/orders');
  if (orders.documents) {
    console.log('\norders (test_shop): ' + orders.documents.length + ' docs');
    orders.documents.slice(0,3).forEach(doc => {
      const f = doc.fields;
      console.log('  - ' + (f.items ? f.items.arrayValue.values.length + ' items' : '?') + ', merchantId: ' + (f.merchantId ? f.merchantId.stringValue : 'N/A'));
    });
  } else {
    console.log('\norders: ' + (orders.error || 'empty'));
  }
  
  const complaints = await fetchCollection('complaints');
  if (complaints.documents) {
    console.log('\ncomplaints: ' + complaints.documents.length + ' docs');
    complaints.documents.slice(0,3).forEach(doc => {
      const f = doc.fields;
      console.log('  - merchantId: ' + (f.merchantId ? f.merchantId.stringValue : 'N/A') + ', status: ' + (f.status ? f.status.stringValue : 'N/A'));
    });
  } else {
    console.log('\ncomplaints: ' + (complaints.error || 'empty'));
  }
  
  console.log('\n=== 完成 ===');
}

main();
