// components/Footer.js
import Link from 'next/link';
import styles from '../page.module.css'; // 更新为正确的相对路径

const Footer = () => {
  return (
    <footer className={styles.footer}>
      <Link href="/terms">Terms and Conditions</Link>
      <Link href="/privacy">Privacy Policy</Link>
      <Link href="/license">License Agreement</Link>
      
      <div className={styles.externalLinks}>
        <a href="https://c2story.com/" target="_blank" rel="noopener noreferrer">AI Generate Story</a>
        <span className={styles.separator}>·</span>
        <a href="https://mochi1preview.com/" target="_blank" rel="noopener noreferrer">Mochi 1 Preview</a>
        <span className={styles.separator}>·</span>
        <a href="https://www.blockblastsolvers.org" target="_blank" rel="noopener noreferrer">Block Blast Solver</a>
        <span className={styles.separator}>·</span>
        <a href="https://www.miside-online.org" target="_blank" rel="noopener noreferrer">Miside Online</a>
        <span className={styles.separator}>·</span>
        <a href="https://www.hailuoai.work" target="_blank" rel="noopener noreferrer">Hailuo AI</a>
        <span className={styles.separator}>·</span>
        <a href="https://www.playsprunkiphase4.com" target="_blank" rel="noopener noreferrer">Play Sprungki Phase 4</a>
      
        <a href="https://www.aireword.win" target="_blank" rel="noopener noreferrer">AI  Reword Tools</a>
   
        <span>·</span>
        <a href="https://www.vo3ai.com" target="_blank" rel="noopener noreferrer">
        VO3 AI
        </a>
        <span>·</span>
        <a href="https://www.orpheus-tts.org/" target="_blank" rel="noopener noreferrer">
        Orpheus TTS
        </a>
        <span>·</span>
        <a href="https://www.ghibligen.org/" target="_blank" rel="noopener noreferrer">
        Ghibli Gen
        </a>
        <span>·</span>
        <a href="https://www.orpheus-tts.org/" target="_blank" rel="noopener noreferrer">
        Orpheus TTS
        </a>
        <span>·</span>
        <a href="https://www.ghibligen.org/" target="_blank" rel="noopener noreferrer">
        Ghibli Gen
        </a>
        <span>·</span>
        <a href="https://www.beautytestai.com/" target="_blank" rel="noopener noreferrer">
        Beauty Test AI
        </a>
        </div>

    </footer>
  );
};

export default Footer;