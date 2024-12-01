// utils/newsUtils.js
import newsData from '@/data/news.json';

export async function getAllNews(translations) {
  const news = Object.entries(newsData.news).map(([id, item]) => ({
    id,
    title: translations?.news?.[id]?.title || item.title,
    description: translations?.news?.[id]?.description || item.description,
    content: translations?.news?.[id]?.content || item.content,
    image: item.image,
    publishDate: item.publishDate,
    category: item.category,
    tags: item.tags,
    author: item.author,
    readingTime: item.readingTime
  }));

  return news.sort((a, b) => new Date(b.publishDate) - new Date(a.publishDate));
}

export async function getNewsById(id, translations) {
  const news = newsData.news[id];
  if (!news) return null;

  return {
    id,
    title: translations?.news?.[id]?.title || news.title,
    description: translations?.news?.[id]?.description || news.description,
    content: translations?.news?.[id]?.content || news.content,
    image: news.image,
    publishDate: news.publishDate,
    category: news.category,
    tags: news.tags,
    author: news.author,
    readingTime: news.readingTime
  };
}

export async function getRelatedNews(currentNewsId, translations, limit = 4) {
  const allNews = await getAllNews(translations);
  const currentNews = newsData.news[currentNewsId];
  
  if (!currentNews) return [];

  return allNews
    .filter(news => 
      news.id !== currentNewsId && 
      (news.category === currentNews.category || 
       news.tags.some(tag => currentNews.tags.includes(tag)))
    )
    .slice(0, limit);
}