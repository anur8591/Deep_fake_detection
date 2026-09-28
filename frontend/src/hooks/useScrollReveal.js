import { useEffect, useRef } from 'react';

/**
 * Observes all elements matching `selector` inside the returned container ref
 * and adds `revealClass` (default: "reveal") when they scroll into view.
 *
 * Mirrors the original vanilla-JS IntersectionObserver blocks used for the
 * feature cards, step cards, trust cards, footer items, etc.
 *
 * @param {string} selector - CSS selector for the children to observe (relative to container)
 * @param {object} options
 * @param {number} options.threshold
 * @param {string} options.revealClass
 * @param {number} options.stagger - ms delay multiplied by index, for staggered reveals
 * @param {boolean} options.once - unobserve after first reveal (default true)
 * @param {boolean} options.inlineStyle - set opacity/transform inline instead of a class
 *   (matches the original feature-card behaviour, whose CSS starts at opacity:0 / translateY(40px))
 */
export default function useScrollReveal(
  selector,
  {
    threshold = 0.2,
    revealClass = 'reveal',
    stagger = 0,
    once = true,
    inlineStyle = false,
  } = {}
) {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const targets = Array.from(container.querySelectorAll(selector));
    if (targets.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const index = targets.indexOf(entry.target);
            const delay = stagger * Math.max(index, 0);

            setTimeout(() => {
              if (inlineStyle) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
              } else {
                entry.target.classList.add(revealClass);
              }
            }, delay);

            if (once) observer.unobserve(entry.target);
          }
        });
      },
      { threshold }
    );

    targets.forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, [selector, threshold, revealClass, stagger, once, inlineStyle]);

  return containerRef;
}
