import { useEffect, useRef } from 'react';

const SCENARIOS = [
  { img: '/img2.png', title: 'Social media clips', label: 'Video verification' },
  { img: '/img3.png', title: 'Public event footage', label: 'Video verification' },
  { img: '/img4.png', title: 'News and reports', label: 'Video verification' },
  { img: '/img5.png', title: 'Video calls', label: 'Video verification' },
];

export default function Scenarios() {
  const wrapperRef = useRef(null);

  useEffect(() => {
    const wrapper = wrapperRef.current;
    if (!wrapper) return;

    const cards = Array.from(wrapper.querySelectorAll('.scenario-card'));

    const onScroll = () => {
      const center = wrapper.scrollLeft + wrapper.offsetWidth / 2;

      cards.forEach((card) => {
        const cardCenter = card.offsetLeft + card.offsetWidth / 2;
        if (Math.abs(center - cardCenter) < card.offsetWidth / 2) {
          card.classList.add('active');
        } else {
          card.classList.remove('active');
        }
      });
    };

    wrapper.addEventListener('scroll', onScroll);
    return () => wrapper.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <section className="third-slide">
      <div className="third-header">
        <h1>Where Video Verification Helps</h1>
        <p>Examples of video contexts where an authenticity check can be useful.</p>
      </div>

      <div className="scenario-wrapper" ref={wrapperRef}>
        {SCENARIOS.map((s) => (
          <div className="scenario-card" key={s.title}>
            <img src={s.img} alt={s.title} />
            <h3>{s.title}</h3>
            <p className="risk">{s.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
