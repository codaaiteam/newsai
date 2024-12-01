'use client'
import Link from 'next/link';
import styles from './NewsList.module.css';
import { useState } from 'react';

export default function NewsList({ news, locale = 'en', showPagination = true }) {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  // Convert news object to array and sort by date
  const newsArray = Object.entries(news || {}).map(([id, item]) => ({
    id,
    ...item
  })).sort((a, b) => new Date(b.publishDate) - new Date(a.publishDate));

  // Calculate pagination
  const totalPages = Math.ceil(newsArray.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const displayedNews = newsArray.slice(startIndex, startIndex + itemsPerPage);

  return (
    <div className={styles.newsListContainer}>
      <div className={styles.newsList}>
        {displayedNews.map((item) => (
          <article key={item.id} className={styles.newsItem}>
            <Link href={`/${locale}/news/${item.id}`} className={styles.newsLink}>
              <div className={styles.newsImage}>
                <img
                  src={item.image || '/placeholder-news.jpg'}
                  alt={item.title}
                  loading="lazy"
                />
              </div>
              <div className={styles.newsContent}>
                <h3 className={styles.newsTitle}>{item.title}</h3>
                <p className={styles.newsDescription}>{item.description}</p>
                <div className={styles.newsInfo}>
                  <span className={styles.newsDate}>
                    {new Date(item.publishDate).toLocaleDateString()}
                  </span>
                  <span className={styles.newsReadTime}>{item.readingTime}</span>
                </div>
              </div>
            </Link>
          </article>
        ))}
      </div>

      {showPagination && totalPages > 1 && (
        <div className={styles.pagination}>
          <button
            onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
            disabled={currentPage === 1}
            className={styles.pageButton}
          >
            Previous
          </button>
          <span className={styles.pageInfo}>
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
            className={styles.pageButton}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}