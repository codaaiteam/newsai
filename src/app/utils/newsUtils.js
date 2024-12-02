// utils/newsUtils.js
import newsData from '@/data/news.json';

export async function getAllNews(t) {
  try {
    if (!t?.news) {
      return [];
    }

    const newsItems = Object.entries(t.news).map(([id, article]) => ({
      id,
      title: article.title,
      description: article.description,
      image: article.image || '/placeholder.jpg', // 匹配你的目录结构
      publishDate: article.publishDate,
      readingTime: article.readingTime ? `${article.readingTime} min read` : '3 min read',
      category: article.category,
      tags: article.tags || [],
      author: article.author || 'PulseAI Team',
      slug: id,
      searchVolume: article.searchStats?.searchVolume || '',
      trendRank: article.searchStats?.trendRank || null
    }));

    return newsItems.sort((a, b) => 
      new Date(b.publishDate) - new Date(a.publishDate)
    );
  } catch (error) {
    console.error("Error in getAllNews:", error);
    return [{
      id: 'texas-longhorns-vs-am-2024',
      title: "Texas Longhorns vs Texas A&M: Historic Rivalry",
      description: "Major matchup in college football as historic rivals face off",
      image: '/placeholder.jpg',
      publishDate: "2024-12-01T16:50:00Z",
      readingTime: "4 min read",
      category: "Sports",
      tags: ["Football", "College Sports"],
      author: "Sports Team",
      searchVolume: "1000000+",
      trendRank: 1
    }];
  }
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