import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { getDatabase } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-database.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyB04fDCs9A8tXJtpZuzrDlIe6WyB6fkShk",
  authDomain: "absensirfid-6c124.firebaseapp.com",
  databaseURL: "https://absensirfid-6c124-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "absensirfid-6c124",
  storageBucket: "absensirfid-6c124.firebasestorage.app",
  messagingSenderId: "334833959957",
  appId: "1:334833959957:web:2f0e1f0f2b247a5165ba1c"
};

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);
const auth = getAuth(app);

export { db, auth };
