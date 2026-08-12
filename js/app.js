import { AuthManager } from "./AuthManager.js?v=9";
import { FirebaseService } from "./FirebaseService.js?v=9";
import { UIManager } from "./UIManager.js?v=9";

const dbService = new FirebaseService();
const auth = new AuthManager(dbService);
const ui = new UIManager(auth, dbService);

// Memulai aplikasi saat DOM selesai dimuat
document.addEventListener('DOMContentLoaded', () => {
    ui.init();
});
