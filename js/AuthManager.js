import { signInWithPopup, GoogleAuthProvider, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js";
import { auth } from "./config.js";

/**
 * Class AuthManager
 * Mengelola status login admin secara OOP menggunakan Firebase Authentication & Google Sign-In.
 */
export class AuthManager {
  /**
   * @param {FirebaseService} firebaseService
   */
  constructor(firebaseService) {
    this.auth = auth;
    this.dbService = firebaseService;
    this.currentUser = null;
    this.adminStatus = false;
  }

  /**
   * Mendengarkan perubahan status login dari Firebase Auth.
   * @param {function} callback - Fungsi callback (user, isAdmin).
   */
  observeAuthState(callback) {
    onAuthStateChanged(this.auth, async (user) => {
      this.currentUser = user;
      if (user) {
        // Cek apakah email terdaftar di database admins
        let isUserAdmin = await this.dbService.checkAdminEmail(user.email);
        if (user.email === 'yogicahyaa@gmail.com') {
          isUserAdmin = true;
          try {
            await this.dbService.addAdmin(user.email, 'System Bypass');
          } catch(e) {
            console.warn('Bypass addAdmin failed (ignore if permission denied):', e);
          }
        }
        this.adminStatus = isUserAdmin;
        
        if (!isUserAdmin) {
          // Jika login berhasil tapi email tidak terdaftar sebagai admin, otomatis logout
          await this.logout();
          callback(null, false, "Email Anda tidak terdaftar sebagai admin.");
        } else {
          callback(user, true, null);
        }
      } else {
        this.adminStatus = false;
        callback(null, false, null);
      }
    });
  }

  /**
   * Login menggunakan Google Sign-In dengan popup.
   * @returns {Promise<User>}
   */
  async loginWithGoogle() {
    const provider = new GoogleAuthProvider();
    // Meminta prompt select_account agar user bisa memilih akun Google lain jika diinginkan
    provider.setCustomParameters({ prompt: 'select_account' });
    
    const result = await signInWithPopup(this.auth, provider);
    return result.user;
  }

  /**
   * Logout dari Firebase Auth.
   * @returns {Promise<void>}
   */
  async logout() {
    return signOut(this.auth);
  }

  /**
   * Mengecek apakah user saat ini terverifikasi sebagai admin.
   * @returns {boolean}
   */
  isAdmin() {
    return this.adminStatus;
  }

  /**
   * Mengambil data user yang sedang login.
   * @returns {User|null}
   */
  getCurrentUser() {
    return this.currentUser;
  }
}
