document.getElementById('global-header').innerHTML = `
  <div class="main-header">
    <div class="nav-container">
      <a href="index.html"><div class="logo">🗣️ ಕನ್ನಡ ಮಾತು</div></a>
        <!-- Hamburger -->
      <div class="menu-toggle" onclick="toggleMenu()">☰</div>
      <nav class="nav-links" id="navLinks">
        <a href="index.html">ಮುಖಪುಟ</a>
        <a href="access.html">ಪ್ರವೇಶ ಆಯ್ಕೆ </a>
        <a href="admin-login.html" class="admin-link" title="ಆಡ್ಮಿನ್ ಪ್ರವೇಶ">👨‍💼</a>
      </nav>
    </div>
  </div>
`; 

function toggleMenu() {
  document.getElementById("navLinks").classList.toggle("open");
}



// <a href="age-selection.html">ವಯಸ್ಸನ ಆಯ್ಕೆ </a>
// <a href="reference.html">ಮೂಲದಂಡ</a>