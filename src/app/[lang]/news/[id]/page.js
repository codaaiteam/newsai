'use client';

import { useParams } from 'next/navigation';
import styles from './page.module.css';
import SEO from '@/app/components/SEO';
import Footer from '@/app/components/Footer';
import LanguageSwitcher from '@/app/components/LanguageSwitcher';
import NewsGrid from '@/app/components/NewsList';
import Link from 'next/link';
import Header from '@/app/components/Header';
import { useTranslations } from '@/hooks/useTranslations';
import Comments from '@/app/components/Comments';

export default function NewsPage() {
  const params = useParams();
  const { t, currentLocale } = useTranslations();
  const { id } = params;

  // Get article from translations
  const article = t?.news?.[id];

  if (!article) {
    return (
      <div className={styles.errorContainer}>
        <h1>{t?.common?.error?.notFound || "Article not found"}</h1>
        <p>{t?.common?.error?.loadingFailed || "The requested article could not be found."}</p>
        <Link href={`/${currentLocale}`} className={styles.backButton}>
          {t?.common?.navigation?.backToHome || "Back to Home"}
        </Link>
      </div>
    );
  }

  return (
    <>
      <LanguageSwitcher />
      <Header />
      <main className={styles.main}>
        <article className={styles.article}>
          <header className={styles.articleHeader}>
            <div className={styles.articleMeta}>
              <span className={styles.articleCategory}>{article.category}</span>
              <time className={styles.articleDate}>
                {new Date(article.publishDate).toLocaleDateString(currentLocale)}
              </time>
            </div>
            <h1 className={styles.articleTitle}>{article.title}</h1>
            <p className={styles.articleDescription}>{article.description}</p>
            <div className={styles.articleInfo}>
              <span className={styles.articleAuthor}>{article.author}</span>
              <span className={styles.readingTime}>{article.readingTime}</span>
            </div>
            <div className={styles.articleTags}>
              {article.tags?.map(tag => (
                <span key={tag} className={styles.tag}>{tag}</span>
              ))}
            </div>
          </header>

          <div 
            className={styles.articleContent}
            dangerouslySetInnerHTML={{ __html: article.content }}
          />

          {/* Comments Section */}
          <section className={styles.commentsSection}>
            <h2>{t?.common?.comments || "Comments"}</h2>
            <Comments articleId={id} />
          </section>
        </article>

        {/* Related Articles */}
        <section className={styles.relatedArticles}>
          <h2>{t?.common?.relatedNews || "Related News"}</h2>
          <NewsGrid t={t} excludeId={id} />
        </section>

        <Footer />
      </main>
    </>
  );
}