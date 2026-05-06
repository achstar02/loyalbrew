// Check if 01118975678 is a merchant ID
const { initializeApp } = require('firebase-admin/app');
const { getFirestore } = require('firebase-admin/firestore');

// Initialize with project ID
initializeApp({ projectId: 'loyalbrew-app-2f8c7' });
const db = getFirestore();

async function check() {
  // Check if this is a merchant
  const merchantDoc = await db.collection('merchants').doc('01118975678').get();
  console.log('\n=== Merchant Check ===');
  console.log('Is merchant 01118975678:', merchantDoc.exists);
  if (merchantDoc.exists) {
    console.log('Merchant data:', JSON.stringify(merchantDoc.data(), null, 2));
  }
  
  // Check all merchants
  const merchantsSnap = await db.collection('merchants').get();
  console.log('\n=== All Merchants ===');
  merchantsSnap.docs.forEach(d => {
    const data = d.data();
    console.log(`ID: ${d.id}, Name: ${data.name}, Phone: ${data.phone || 'N/A'}`);
  });
  
  // Check complaints with this phone
  const complaintsSnap = await db.collection('complaints').get();
  console.log('\n=== All Complaints ===');
  complaintsSnap.docs.forEach(d => {
    const c = d.data();
    console.log(`ID: ${c.id}, MerchantId: ${c.merchantId}, Member: ${c.memberName} (${c.memberPhone})`);
  });
}

check().catch(console.error);
