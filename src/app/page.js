'use client'

import { useState, useEffect } from "react";
import { useParams } from 'next/navigation';
import styles from "./page.module.css";
import SEO from './components/SEO';
import Footer from './components/Footer';
import LanguageSwitcher from './components/LanguageSwitcher';
import Header from '@/app/components/Header';
import { useTranslations } from '@/hooks/useTranslations';
import { getAllNews } from '@/app/utils/newsUtils';
import Link from 'next/link';

export default function Home() {
  const params = useParams();
  const { t, currentLocale } = useTranslations();
  const [latestNews, setLatestNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadNews() {
      try {
        const news = await getAllNews(t);
        setLatestNews(news);
      } catch (error) {
        console.error('Failed to load news:', error);
      } finally {
        setLoading(false);
      }
    }

    loadNews();
  }, [t]);

  if (loading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  // 获取头条新闻和其他新闻
  const featuredNews = latestNews[0];
  const otherNews = latestNews.slice(1);

  return (
    <>
      <SEO 
        title={t?.seo?.title || "Latest News"}
        description={t?.seo?.description || "Latest news and updates"}
      />
      
      <Header />
      <LanguageSwitcher />
      
      <main className={styles.main}>
        {/* 头条新闻 */}
        {featuredNews && (
          <section className={styles.featuredNews}>
            <Link href={`/${currentLocale}/news/${featuredNews.id}`}>
              <div className={styles.featuredNewsCard}>
                <img 
                  src={featuredNews.image} 
                  alt={featuredNews.title}
                  className={styles.featuredImage}
                />
                <div className={styles.featuredContent}>
                  <h1>{featuredNews.title}</h1>
                  <p>{featuredNews.description}</p>
                  <div className={styles.newsInfo}>
                    <span>{new Date(featuredNews.publishDate).toLocaleDateString()}</span>
                    <span>{featuredNews.readingTime}</span>
                  </div>
                </div>
              </div>
            </Link>
          </section>
        )}

        {/* 新闻列表 */}
        <section className={styles.newsSection}>
          <h2>{t?.news?.latestNews || "Latest News"}</h2>
          <div className={styles.newsGrid}>
            {otherNews.map(news => (
              <Link 
                key={news.id}
                href={`/${currentLocale}/news/${news.id}`}
                className={styles.newsCard}
              >
                <img 
                  src={news.image} 
                  alt={news.title}
                  className={styles.newsImage}
                />
                <div className={styles.newsContent}>
                  <h3>{news.title}</h3>
                  <p>{news.description}</p>
                  <div className={styles.newsInfo}>
                    <span>{new Date(news.publishDate).toLocaleDateString()}</span>
                    <span>{news.readingTime}</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </section>
        
        <Footer />
      </main>
    </>
  );
}