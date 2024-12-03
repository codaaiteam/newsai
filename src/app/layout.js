import './globals.css'
import { Inter } from 'next/font/google'
import Script from 'next/script'
import en from '../locales/en.json'
import ja from '../locales/ja.json'
import ko from '../locales/ko.json'
import de from '../locales/de.json'
import fr from '../locales/fr.json'
import it from '../locales/it.json'
import es from '../locales/es.json'
import zh from '../locales/zh.json'
import ru from '../locales/ru.json'
import zhtw from '../locales/zh-tw.json'

const translations = { en, ja, ko, de, fr, it, es, zh, ru, zhtw }
const locales = Object.keys(translations)
const inter = Inter({ subsets: ['latin'] })

const langMap = {
  'en': 'en',
  'ja': 'ja',
  'ko': 'ko',
  'de': 'de',
  'fr': 'fr',
  'it': 'it',
  'es': 'es',
  'zh': 'zh',
  'zh-tw': 'zh-TW',
  'ru': 'ru'
}

export async function generateMetadata({ params }) {
  const locale = params?.lang || 'en'
  const t = translations[locale]
  
  const baseUrl = t?.seo?.siteUrl || 'https://www.ainews.hk'
  const currentUrl = `${baseUrl}/${locale}`
  
  const languageAlternates = locales.reduce((acc, lang) => {
    acc[lang] = `${baseUrl}/${lang}`
    return acc
  }, {})

  return {
    metadataBase: new URL(baseUrl),
    title: t?.seo?.title || 'AI Technology News and Updates',
    description: t?.seo?.description || 'Latest news and insights about artificial intelligence, technology, and digital innovation',
    keywords: t?.seo?.keywords || 'AI news, technology news, artificial intelligence, digital innovation, tech updates',
    openGraph: {
      title: t?.seo?.title || 'AI Technology News and Updates',
      description: t?.seo?.description || 'Latest news and insights about artificial intelligence',
      type: 'website',
      url: currentUrl,
      siteName: 'AI News',
      locale: locale,
      alternateLocales: locales.filter(l => l !== locale),
    },
    twitter: {
      card: 'summary_large_image',
      title: t?.seo?.title || 'AI Technology News and Updates',
      description: t?.seo?.description || 'Latest news and insights about artificial intelligence',
    },
    alternates: {
      canonical: currentUrl,
      languages: languageAlternates,
    },
    robots: 'index, follow',
  }
}

export default function RootLayout({ children, params }) {
  const locale = params?.lang || 'en'
  const t = translations[locale] || translations.en
  const lang = langMap[locale] || 'en'

  return (
    <html lang={lang}>
      <head>
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="google-site-verification" content="EROOYLebq2EHxKvmMtmGO7sY1s8YOdWLqYNyU2JLQLA" />
      </head>
      <body className={inter.className}>
        {children}
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXX"
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-XXXXXXXX');
          `}
        </Script>
      </body>
    </html>
  )
}