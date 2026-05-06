// LoyalBrew Cloud Functions - 安全验证服务
// 部署方式: firebase deploy --only functions

const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp();

// ============ 密码验证 API ============
// 商户登录时调用此函数验证密码（不返回明文密码）
exports.verifyMerchantPassword = functions.https.onCall(async (data, context) => {
  const { merchantId, password } = data;
  
  if (!merchantId || !password) {
    throw new functions.https.HttpsError('invalid-argument', 'Missing merchantId or password');
  }
  
  try {
    const merchantDoc = await admin.firestore().collection('merchants').doc(merchantId).get();
    
    if (!merchantDoc.exists) {
      throw new functions.https.HttpsError('not-found', 'Merchant not found');
    }
    
    const merchantData = merchantDoc.data();
    const storedPassword = merchantData.password;
    
    // 验证密码（直接比对，因为密码已在后端）
    if (password === storedPassword) {
      // 使用自定义 token 返回（可选）
      return { 
        success: true, 
        merchantId: merchantId,
        merchantName: merchantData.merchant_name
      };
    } else {
      throw new functions.https.HttpsError('unauthenticated', 'Invalid password');
    }
  } catch (error) {
    if (error.code === 'not-found' || error.code === 'unauthenticated') {
      throw error;
    }
    console.error('Password verification error:', error);
    throw new functions.https.HttpsError('internal', 'Verification failed');
  }
});

// ============ 会员注册验证 API ============
// 检查手机号是否已注册
exports.checkMemberPhone = functions.https.onCall(async (data, context) => {
  const { merchantId, phone } = data;
  
  if (!merchantId || !phone) {
    throw new functions.https.HttpsError('invalid-argument', 'Missing required fields');
  }
  
  const membersRef = admin.firestore().collection('merchants').doc(merchantId).collection('members');
  const snapshot = await membersRef.where('phone', '==', phone).limit(1).get();
  
  return {
    exists: !snapshot.empty,
    memberId: snapshot.empty ? null : snapshot.docs[0].id
  };
});

// ============ 安全审计日志 ============
// 记录登录尝试（防暴力破解）
exports.logLoginAttempt = functions.https.onCall(async (data, context) => {
  const { merchantId, success, ip } = data;
  
  const logRef = admin.firestore().collection('security_logs');
  await logRef.add({
    event: 'login_attempt',
    merchantId,
    success,
    ip: ip || 'unknown',
    timestamp: admin.firestore.FieldValue.serverTimestamp()
  });
  
  return { logged: true };
});

// ============ 部署说明 ============
/*
部署步骤:

1. 确保 Firebase CLI 已安装
   npm install -g firebase-tools

2. 登录 Firebase
   firebase login

3. 初始化 Cloud Functions（如果尚未初始化）
   firebase init functions

4. 部署所有函数
   firebase deploy --only functions

5. 或者部署单个函数
   firebase deploy --only functions:verifyMerchantPassword

使用示例（前端调用）:
```javascript
const verifyPassword = firebase.functions().httpsCallable('verifyMerchantPassword');
try {
  const result = await verifyPassword({ 
    merchantId: 'merchant123', 
    password: 'userInputPassword' 
  });
  console.log('Login success:', result.data);
} catch (error) {
  console.error('Login failed:', error.message);
}
```
*/