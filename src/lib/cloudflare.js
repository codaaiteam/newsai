// lib/cloudflare.js
import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3';

const R2 = new S3Client({
 region: 'auto',
 endpoint: `https://${process.env.CF_ACCOUNT_ID}.r2.cloudflarestorage.com`,
 credentials: {
   accessKeyId: process.env.R2_ACCESS_KEY_ID,
   secretAccessKey: process.env.R2_SECRET_ACCESS_KEY,
 },
});

export async function getNewsData() {
  try {
    const response = await R2.send(new GetObjectCommand({
      Bucket: 'news-assets',
      Key: 'data/news.json'
    }));
    const data = await response.Body?.transformToString();
    return JSON.parse(data);
  } catch {
    // 如果从 R2 获取失败，则从本地文件获取
    return import('@/data/news.json');
  }
}

export async function getTranslation(locale) {
  try {
    const response = await R2.send(new GetObjectCommand({
      Bucket: 'news-assets', 
      Key: `locales/${locale}.json`
    }));
    const data = await response.Body?.transformToString();
    return JSON.parse(data);
  } catch {
    return import(`@/locales/${locale}.json`);
  }
}