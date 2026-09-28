export default function LoginModal({ isOpen, onClose }) {
  const continueWithGoogle = () => {
    alert('Redirecting to Google Sign-In...');
  };

  return (
    <div className="login-overlay" id="loginModal" style={{ display: isOpen ? 'flex' : 'none' }}>
      <div className="login-box">
        <button className="close-btn" onClick={onClose}>✕</button>

        <h2>Sign in to DeepGuard</h2>
        <p>Continue securely using your Google account</p>

        <button className="google-login-btn" onClick={continueWithGoogle}>
          <img src="https://www.svgrepo.com/show/475656/google-color.svg" alt="Google" />
          Continue with Google
        </button>

        <small className="login-note">
          We don't store passwords. Secure OAuth login.
        </small>
      </div>
    </div>
  );
}
