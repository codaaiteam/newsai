'use client'

import { useRouter, useParams } from 'next/navigation';
import styles from './NewsList.module.css';
import { useEffect, useState } from 'react';
import { getTranslation } from '@/lib/cloudflare';

export default function NewsGrid({ t, excludeId }) {
  const router = useRouter();
  const params = useParams();
  const currentLang = params?.lang || 'en';
  const [news, setNews] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    let isMounted = true;
    async function loadNews() {
      try {
        // Get news from translations
        const newsData = t?.news || {};
        
        if (!isMounted) return;
        
        // Map the news data to our desired format
        const mappedNews = Object.entries(newsData)
          .map(([id, article]) => ({
            id,
            title: article.title,
            description: article.description,
            category: article.category,
            publishDate: article.publishDate,
            author: article.author,
            readingTime: article.readingTime,
            tags: article.tags,
          }))
          .sort((a, b) => new Date(b.publishDate) - new Date(a.publishDate)); // Sort by date

        setNews(mappedNews);
      } catch (error) {
        console.error('Failed to load news:', error);
      }
    }
    loadNews();
    return () => {
      isMounted = false;
    };
  }, [t, excludeId]);

  const handleNewsClick = (newsId) => {
    router.push(`/${currentLang}/news/${newsId}`);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      router.push(`/${currentLang}/search?q=${encodeURIComponent(searchTerm)}`);
    }
  };

  const filteredNews = news.filter(article => 
    (article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    article.description.toLowerCase().includes(searchTerm.toLowerCase())) &&
    (excludeId ? article.id !== excludeId : true)
  );

  return (
    <section className={styles.newsGridSection}>
      <div className={styles.searchWrapper}>
        <form onSubmit={handleSearch} className={styles.searchForm}>
          <input
            type="search"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder={t?.common?.search || "Search news..."}
            className={styles.searchInput}
          />
          <button type="submit" className={styles.searchButton}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
          </button>
        </form>
      </div>

      <div className={styles.newsGrid}>
        {filteredNews.map((article) => (
          <div 
            key={article.id}
            className={styles.newsCard}
            onClick={() => handleNewsClick(article.id)}
            role="link"
            tabIndex={0}
          >
            <div className={styles.newsContent}>
              <div className={styles.newsHeader}>
                <span className={styles.newsCategory}>{article.category}</span>
                <span className={styles.newsDate}>
                  {new Date(article.publishDate).toLocaleDateString(currentLang)}
                </span>
              </div>
              <h3 className={styles.newsTitle}>{article.title}</h3>
              <p className={styles.newsDescription}>{article.description}</p>
              <div className={styles.newsFooter}>
                <span className={styles.newsAuthor}>{article.author}</span>
                <span className={styles.readingTime}>{article.readingTime}</span>
              </div>
              <div className={styles.newsTags}>
                {article.tags?.map(tag => (
                  <span key={tag} className={styles.tag}>{tag}</span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}