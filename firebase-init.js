// Firebase 10.x (modular) via CDN
console.log("[firebase-init.js] 开始加载 Firebase 模块...");

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-app.js";

// Firestore APIs (from firebase-firestore.js)
import {
  getFirestore,
  doc,
  getDoc,
  setDoc,
  runTransaction,
  updateDoc,
  increment,
  collection,
  deleteDoc, getDocs,
  writeBatch,
  onSnapshot,
  query,
  where,
} from "https://www.gstatic.com/firebasejs/10.14.1/firebase-firestore.js";

// Auth APIs (from firebase-auth.js)
import {
  getAuth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut as fbSignOut,
  onAuthStateChanged,
  signInWithPhoneNumber,
  RecaptchaVerifier,
} from "https://www.gstatic.com/firebasejs/10.14.1/firebase-auth.js";

// Messaging APIs (from firebase-messaging.js)
import {
  getMessaging,
  getToken,
  onMessage,
} from "https://www.gstatic.com/firebasejs/10.14.1/firebase-messaging.js";

// Provided by user (public client config)
const firebaseConfig = {
  apiKey: "AIzaSyAlHVGBROFf3aOjaMUSJy4nzomLHfXMcgg",
  authDomain: "loyalbrew-app-2f8c7.firebaseapp.com",
  projectId: "loyalbrew-app-2f8c7",
  storageBucket: "loyalbrew-app-2f8c7.firebasestorage.app",
  messagingSenderId: "974851821194",
  appId: "1:974851821194:web:770042fd50d656b1c5a773",
  measurementId: "G-ENBFFQ25R9",
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);

// Initialize Firebase Messaging (lazy — only if VAPID key provided)
let messaging = null;
try {
  const VAPID_KEY = 'BEl62iUYgUivxIkv69yViEuiBIa-Ib9-SkvMeAtA3LFgDzkrxZJjSgSnfckjBJuBkr3qBUYIHBQFLXYP5KkshDYU';
  messaging = getMessaging(app);
  window.__lbFCMMessaging = messaging;
  console.log("[firebase-init.js] ✅ Firebase Messaging 已初始化");
} catch(e) {
  console.warn("[firebase-init.js] Messaging 初始化失败（正常如果没有VAPID key）:", e.message);
}

// Make Firebase APIs available to non-module app.js
window.__lbFirebase = {
  app,
  auth: () => auth,          // Auth service (function for lazy access)
  db,
  // Firestore
  doc,
  getDoc,
  setDoc,
  runTransaction,
  updateDoc,
  increment,
  collection,
  deleteDoc,
  getDocs,
  writeBatch,
  onSnapshot,
  query,
  where,
  // Auth - Email/Password
  createUserWithEmailAndPassword: (email, pass) => createUserWithEmailAndPassword(auth, email, pass),
  signInWithEmailAndPassword: (email, pass) => signInWithEmailAndPassword(auth, email, pass),
  // Auth - Phone
  signInWithPhoneNumber: (phone, verifier) => signInWithPhoneNumber(auth, phone, verifier),
  RecaptchaVerifier: (elementId) => new RecaptchaVerifier(elementId, { size: 'invisible' }, auth),
  signOut: () => fbSignOut(auth),
  onAuthStateChanged: (callback) => onAuthStateChanged(auth, callback),
  // Messaging
  messaging: () => messaging,
  getToken: messaging ? (opts) => getToken(messaging, opts) : null,
  onMessage: messaging ? (cb) => onMessage(messaging, cb) : null,
};

// Ensure all Firebase APIs are on window before any app.js code runs
window.__lbFirebaseReady = true;
console.log("[firebase-init.js] ✅ Firebase 模块加载成功, __lbFirebase 已挂载到 window");
