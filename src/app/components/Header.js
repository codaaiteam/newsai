'use client'

import Link from 'next/link';
import Image from 'next/image';
import { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useTranslations } from '@/hooks/useTranslations';
import styles from './Header.module.css';

export default function Header() {
  const [searchTerm, setSearchTerm] = useState('');
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const router = useRouter();
  const params = useParams();
  const { t } = useTranslations();
  const currentLang = params?.lang || 'en';

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      router.push(`/${currentLang}/search?q=${encodeURIComponent(searchTerm)}`);
    }
  };

  const categories = t?.categories || {
    ai: "AI",
    technology: "Technology",
    innovation: "Innovation",
    research: "Research"
  };

  return (
    <header className={styles.header}>
      <div className={styles.headerContent}>
        <Link href={`/${currentLang}`} className={styles.logoLink}>
          <div className={styles.logo}>
            <Image
              src="/logo.svg"
              alt="PulseAI"
              width={150}
              height={40}
              priority
              className={styles.logoFull}
            />
          </div>
        </Link>

        <nav className={styles.navigation}>
          {Object.entries(categories).map(([key, value]) => (
            <Link 
              key={key}
              href={`/${currentLang}/category/${key}`}
              className={styles.navLink}
            >
              {value}
            </Link>
          ))}
        </nav>

        <div className={styles.searchContainer}>
          <button 
            className={styles.searchToggle}
            onClick={() => setIsSearchOpen(!isSearchOpen)}
            aria-label={t?.common?.search || "Toggle search"}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
          </button>
          <form 
            className={`${styles.searchForm} ${isSearchOpen ? styles.open : ''}`}
            onSubmit={handleSearch}
          >
            <input
              type="search"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder={t?.common?.search || "Search..."}
              className={styles.searchInput}
            />
          </form>
        </div>
      </div>
    </header>
  );
}