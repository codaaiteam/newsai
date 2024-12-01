import Analytics from '@/app/components/Analytics';
import { getTranslation } from '@/lib/cloudflare';

export async function generateMetadata({ params }) {
  const { lang, id } = params;
  
  try {
    // 获取翻译数据
    const t = await getTranslation(lang);
    
    // 从翻译文件中获取新闻数据
    const article = t?.news?.[id];
    
    if (!article) {
      console.log('Article not found:', id);
      return {
        title: t?.common?.error?.notFound || 'Article Not Found',
        description: t?.common?.error?.loadingFailed || 'The requested article could not be found'
      };
    }

    const baseUrl = t?.seo?.siteUrl || 'https://www.ainews.hk';
    const currentUrl = `${baseUrl}/${lang}/news/${id}`;

    return {
      metadataBase: new URL(baseUrl),
      title: `${article.title} - ${t?.seo?.title || 'AI News'}`,
      description: article.description,
      
      openGraph: {
        title: article.title,
        description: article.description,
        type: 'article',
        url: currentUrl,
        siteName: 'AI News',
        publishedTime: article.publishDate,
        authors: [article.author],
        tags: article.tags,
        locale: lang,
      },
      
      twitter: {
        card: 'summary_large_image',
        title: article.title,
        description: article.description,
      },
      
      keywords: article.tags?.join(', '),
      
      alternates: {
        canonical: currentUrl,
        languages: {
          'en': `${baseUrl}/en/news/${id}`,
          'zh': `${baseUrl}/zh/news/${id}`,
          'ja': `${baseUrl}/ja/news/${id}`,
          'ko': `${baseUrl}/ko/news/${id}`,
          'de': `${baseUrl}/de/news/${id}`,
          'fr': `${baseUrl}/fr/news/${id}`,
          'it': `${baseUrl}/it/news/${id}`,
          'es': `${baseUrl}/es/news/${id}`,
          'ru': `${baseUrl}/ru/news/${id}`,
          'zh-tw': `${baseUrl}/zh-tw/news/${id}`
        }
      },
      
      category: article.category
    };
  } catch (error) {
    console.error('Error in generateMetadata:', error);
    return {
      title: 'Error Loading Article',
      description: 'There was an error loading the article'
    };
  }
}

export default function NewsLayout({ children }) {
  return (
    <>
      <Analytics />
      {children}
    </>
  );
}