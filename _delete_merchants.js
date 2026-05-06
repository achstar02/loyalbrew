// Delete all merchants from Firestore to start fresh
const { initializeApp, cert } = require('firebase-admin');
const { getFirestore } = require('firebase-admin/firestore');

const serviceAccount = {
  type: "service_account",
  project_id: "loyalbrew-app-2f8c7",
  private_key_id: process.env.FIREBASE_PRIVATE_KEY_ID || "",
  private_key: (process.env.FIREBASE_PRIVATE_KEY || "").replace(/\\n/g, '\n'),
  client_email: process.env.FIREBASE_CLIENT_EMAIL || "",
  client_id: process.env.FIREBASE_CLIENT_ID || "",
  auth_uri: "https://accounts.google.com/o/oauth2/auth",
  token_uri: "https://oauth2.googleapis.com/token",
  auth_provider_x509_cert_url: "https://www.googleapis.com/oauth2/v1/certs",
  client_x509_cert_url: process.env.FIREBASE_CLIENT_X509_CERT_URL || ""
};

let app;
try {
  app = initializeApp({
    credential: cert(serviceAccount)
  });
} catch(e) {
  console.log('App already initialized or credentials missing');
  app = initializeApp();
}

const db = getFirestore();

async function deleteAllMerchants() {
  console.log('Connecting to Firestore project: loyalbrew-app-2f8c7');
  
  const collections = ['merchants'];
  const subCollections = ['menu', 'orders', 'wallets'];
  
  for (const col of collections) {
    console.log(`\n📦 Processing collection: ${col}`);
    try {
      const snap = await db.collection(col).get();
      console.log(`   Found ${snap.size} documents`);
      
      if (snap.size === 0) {
        console.log('   ✅ No documents to delete');
        continue;
      }
      
      const batchSize = 200;
      let deleted = 0;
      
      const batch = db.batch();
      snap.docs.forEach((doc, i) => {
        batch.delete(doc.ref);
        if ((i + 1) % batchSize === 0 || i === snap.size - 1) {
          // We'll commit each individually for safety
        }
      });
      
      // Delete one by one to handle sub-collections
      for (const doc of snap.docs) {
        const docId = doc.id;
        console.log(`   🗑 Deleting: ${docId}...`);
        
        // Delete sub-collections first
        for (const subCol of subCollections) {
          try {
            const subSnap = await db.collection(col).doc(docId).collection(subCol).get();
            for (const subDoc of subSnap.docs) {
              await subDoc.ref.delete();
            }
            if (subSnap.size > 0) {
              console.log(`      - Deleted ${subSnap.size} docs from ${subCol}`);
            }
          } catch(e) {}
        }
        
        // Delete main document
        await doc.ref.delete();
        deleted++;
        console.log(`   ✅ Deleted ${deleted}/${snap.size}`);
      }
      
      console.log(`   🎉 Deleted ${deleted} documents from ${col}`);
      
    } catch(e) {
      console.log(`   ❌ Error: ${e.message}`);
    }
  }
  
  console.log('\n✅ All merchant data deleted!');
}

deleteAllMerchants().then(() => process.exit(0)).catch(e => {
  console.error('Fatal error:', e.message);
  process.exit(1);
});