import { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import AnalyzeSection from './components/AnalyzeSection';
import Scenarios from './components/Scenarios';
import HowItWorks from './components/HowItWorks';
import Trust from './components/Trust';
import CTA from './components/CTA';
import Footer from './components/Footer';
import LoginModal from './components/LoginModal';
import './deepguard.css';

// Buttons that used to open MediaModal now scroll to the new
// Upload/Result section (id="tools") instead — same destination
// the "Tools" nav link already pointed to.
function scrollToAnalyze() {
  document.getElementById('tools')?.scrollIntoView({ behavior: 'smooth' });
}

export default function App() {
  const [isLoginModalOpen, setLoginModalOpen] = useState(false);

  return (
    <>
      <Navbar onLoginClick={() => setLoginModalOpen(true)} />

      <Hero onAnalyzeClick={scrollToAnalyze} />

      <AnalyzeSection />

      <Scenarios />

      <HowItWorks onTryClick={scrollToAnalyze} />

      <Trust />

      <CTA onTryClick={scrollToAnalyze} />

      <Footer />

      <LoginModal isOpen={isLoginModalOpen} onClose={() => setLoginModalOpen(false)} />
    </>
  );
}
