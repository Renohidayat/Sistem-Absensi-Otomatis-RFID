import codecs

with codecs.open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Update variables
css = css.replace('--hairline: #e2e8f0;', '--hairline: #cbd5e1;') # slate-300
css = css.replace('--text-muted: #64748b;', '--text-muted: #475569;') # slate-600 for better contrast

# 2. Update Card shadow & border
css = css.replace('box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.02);', 'box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -2px rgba(0,0,0,0.025);\n  border: 1px solid var(--hairline);')

# 3. Add mobile header & overlay styles
mobile_styles = '''
.mobile-header {
  display: none;
}
.mobile-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(2px);
  z-index: 45;
  opacity: 0;
  transition: opacity 0.3s ease;
}
.mobile-overlay.active {
  display: block;
  opacity: 1;
}

/* Button & interactive states */
.btn:active { transform: scale(0.97); }
input:focus, select:focus, textarea:focus { 
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px var(--primary-light) !important;
}
'''

# insert before @media
css = css.replace('/* Responsive */', mobile_styles + '\n/* Responsive */')

# 4. Rewrite @media (max-width: 768px)
old_media = '''@media (max-width: 768px) {
  .app-layout {
    grid-template-columns: 1fr;
  }
  aside {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    top: auto;
    height: auto;
    z-index: 40;
    border-right: none;
    border-top: 1px solid var(--hairline);
    box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  }
  aside .tabs {
    flex-direction: row;
    overflow-x: auto;
    padding: 0.5rem;
    gap: 0.125rem;
  }
  aside .tabs .tab-btn {
    flex-direction: column;
    font-size: 0.625rem;
    padding: 0.375rem 0.5rem;
    gap: 0.25rem;
    min-width: max-content;
  }
  main {
    padding: 1.25rem;
    padding-bottom: 5rem;
  }
  .siswa-profile-card {
    flex-direction: column;
    text-align: center;
  }
}'''

new_media = '''@media (max-width: 768px) {
  .app-layout {
    display: block;
  }
  aside {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    height: 100vh;
    width: 260px;
    z-index: 50;
    transform: translateX(-100%);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 4px 0 24px rgba(0,0,0,0.1);
    border-right: 1px solid var(--hairline);
  }
  aside.mobile-open {
    transform: translateX(0);
  }
  aside .tabs {
    flex-direction: column;
    padding: 1rem;
    gap: 0.25rem;
  }
  aside .tabs .tab-btn {
    flex-direction: row;
    font-size: 0.875rem;
    padding: 0.75rem 1rem;
  }
  
  .mobile-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 60px;
    padding: 0 1.25rem;
    background: var(--surface-1);
    border-bottom: 1px solid var(--hairline);
    position: sticky;
    top: 0;
    z-index: 40;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  
  main {
    padding: 1rem;
  }
  .siswa-profile-card {
    flex-direction: column;
    text-align: center;
  }
}'''

css = css.replace(old_media, new_media)

with codecs.open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
