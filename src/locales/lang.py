import json
import os
from typing import Dict, Any, Set
from deep_translator import GoogleTranslator
from time import sleep
from tqdm import tqdm
import sys
import random
import re
import traceback  # 添加这行

GAME_NAME_RULES = {
    'ja': {
        'Sprunki': 'スプレンキー',
        'Phase': 'ステージ',
        'Retake': 'リメイク',
        'Cool As Ice': 'アイス',
        # 添加其他映射规则
    },
    'ko': {
        'Sprunki': '스프렁키',
        'Phase': '단계',
        # 添加其他映射规则  
    }
}

class JSONTranslator:
    def __init__(self):
        # 定义目标语言列表
        self.target_languages = {
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh-CN': 'Simplified Chinese',
            'zh-TW': 'Traditional Chinese',
            'fr': 'French',
            'de': 'German',
            'es': 'Spanish',
            'it': 'Italian',
            'ru':'Russisan'
        }

        self.update_paths = []
        
        self.technical_keys = {
            # 网站技术字段
            'ogType',
            'ogUrl',
            'ogImage',
            'twitterCard',
            'twitterImage',
            'siteUrl',
            'robots',
            'canonical',
            'googleSiteVerification',
            'googleAnalyticsId',
            'direction',
            'fontFamily',
            'language'
        }

        self.title_fields = {
            'title',
            'seoTitle',
            'ogTitle',
            'twitterTitle',
            'howToPlay',
            'keyFeatures',
            'whyPlay'
        }

        # 添加固定值映射
        self.fixed_values = {
            'ogType': 'website',
            'twitterCard': 'summary_large_image',
            'robots': 'index, follow',
            'direction': 'ltr',
            'fontFamily': 'Inter',
            'language': {
                'zh-CN': 'zh',
                'ja': 'ja',
                'ko': 'ko',
                'de': 'de',
                'fr': 'fr',
                'it': 'it',
                'es': 'es',
                'zh-TW': 'zh-tw',
                'ru': 'ru',
            }
        }

        # URL模式
        self.url_patterns = [
            r'https?://[^\s<>"]+|www\.[^\s<>"]+',
            r'\.svg$',
            r'\.com',
            r'\.app'
        ]

        # 格式模式
        self.format_patterns = [
            r'G-[A-Z0-9]+',
            r'gp8OOTgtImSxvl5BNocZiHeMKwXw5QP6e7SaeCVQjEQ'  # 保护 Mix & Create
        ]
        # 品牌词和专有名词（不翻译）
        self.brand_names = {
            "PC",
            "Incredibox",
            "Sprunki Phase 4",
            # 在这里添加更多品牌词
        }
        
        # 特定翻译词典
        self.custom_translations = {
            # 简体中文
            'zh-CN': {
                'home': '主页',
                'about': '关于我们',
                'contact': '联系我们',
                'products': '产品中心',
                'services': '服务支持',
                'news': '新闻动态',
                'search': '搜索',
                'login': '登录',
                'register': '注册',
                'account': '账户中心',
                'cart': '购物车',
                'checkout': '结账',
                'logout': '退出登录',
                'profile': '个人资料',
                'settings': '设置',
                'dashboard': '控制台',
                'orders': '订单管理',
                'wishlist': '收藏夹',
                'help': '帮助中心',
                'faq': '常见问题',
                'privacy': '隐私政策',
                'terms': '使用条款',
                'shipping': '配送说明',
                'returns': '退换政策',
                'categories': '商品分类',
                'subscribe': '订阅',
                'more': '更多',
                'menu': '菜单',
                'close': '关闭',
                'back': '返回',
                'submit': '提交',
                'cancel': '取消',
                'save': '保存',
                'delete': '删除',
                'edit': '编辑',
                'update': '更新',
                'welcome': '欢迎',
                'password': '密码',
                'email': '邮箱',
                'phone': '电话',
                'address': '地址'
            },
            'ru': {
    'home': 'Главная',
    'about': 'О нас',
    'contact': 'Контакты',
    'products': 'Продукты',
    'services': 'Услуги', 
    'news': 'Новости',
    'search': 'Поиск',
    'login': 'Вход',
    'register': 'Регистрация',
    'account': 'Аккаунт',
    'cart': 'Корзина',
    'checkout': 'Оформление заказа',
    'logout': 'Выход',
    'profile': 'Профиль',
    'settings': 'Настройки',
    'dashboard': 'Панель управления',
    'orders': 'Заказы',
    'wishlist': 'Избранное',
    'help': 'Помощь',
    'faq': 'Частые вопросы',
    'privacy': 'Конфиденциальность',
    'terms': 'Условия использования',
    'shipping': 'Доставка',
    'returns': 'Возвраты',
    'categories': 'Категории',
    'subscribe': 'Подписаться',
    'more': 'Ещё',
    'menu': 'Меню',
    'close': 'Закрыть',
    'back': 'Назад',
    'submit': 'Отправить',
    'cancel': 'Отмена',
    'save': 'Сохранить',
    'delete': 'Удалить',
    'edit': 'Редактировать',
    'update': 'Обновить',
    'welcome': 'Добро пожаловать',
    'password': 'Пароль',
    'email': 'Эл. почта',
    'phone': 'Телефон',
    'address': 'Адрес'
},
            # 日语
            'ja': {
                'home': 'ホーム',
                'about': '会社概要',
                'contact': 'お問い合わせ',
                'products': '製品情報',
                'services': 'サービス',
                'news': 'ニュース',
                'search': '検索',
                'login': 'ログイン',
                'register': '新規登録',
                'account': 'アカウント',
                'cart': 'カート',
                'checkout': '購入手続き',
                'logout': 'ログアウト',
                'profile': 'プロフィール',
                'settings': '設定',
                'dashboard': 'ダッシュボード',
                'orders': '注文履歴',
                'wishlist': 'お気に入り',
                'help': 'ヘルプ',
                'faq': 'よくある質問',
                'privacy': 'プライバシーポリシー',
                'terms': '利用規約',
                'shipping': '配送について',
                'returns': '返品・交換',
                'categories': 'カテゴリー',
                'subscribe': '登録',
                'more': 'もっと見る',
                'menu': 'メニュー',
                'close': '閉じる',
                'back': '戻る',
                'submit': '送信',
                'cancel': 'キャンセル',
                'save': '保存',
                'delete': '削除',
                'edit': '編集',
                'update': '更新',
                'welcome': 'ようこそ',
                'password': 'パスワード',
                'email': 'メール',
                'phone': '電話番号',
                'address': '住所'
            },
            # 韩语
            'ko': {
                'home': '홈',
                'about': '회사 소개',
                'contact': '문의하기',
                'products': '제품',
                'services': '서비스',
                'news': '뉴스',
                'search': '검색',
                'login': '로그인',
                'register': '회원가입',
                'account': '계정',
                'cart': '장바구니',
                'checkout': '결제하기',
                'logout': '로그아웃',
                'profile': '프로필',
                'settings': '설정',
                'dashboard': '대시보드',
                'orders': '주문내역',
                'wishlist': '위시리스트',
                'help': '도움말',
                'faq': '자주 묻는 질문',
                'privacy': '개인정보처리방침',
                'terms': '이용약관',
                'shipping': '배송안내',
                'returns': '반품/교환',
                'categories': '카테고리',
                'subscribe': '구독하기',
                'more': '더 보기',
                'menu': '메뉴',
                'close': '닫기',
                'back': '뒤로',
                'submit': '제출',
                'cancel': '취소',
                'save': '저장',
                'delete': '삭제',
                'edit': '편집',
                'update': '업데이트',
                'welcome': '환영합니다',
                'password': '비밀번호',
                'email': '이메일',
                'phone': '전화번호',
                'address': '주소'
            },
            # 繁体中文
            'zh-TW': {
                'home': '首頁',
                'about': '關於我們',
                'contact': '聯絡我們',
                'products': '產品中心',
                'services': '服務支援',
                'news': '新聞動態',
                'search': '搜尋',
                'login': '登入',
                'register': '註冊',
                'account': '帳戶中心',
                'cart': '購物車',
                'checkout': '結帳',
                'logout': '登出',
                'profile': '個人資料',
                'settings': '設定',
                'dashboard': '控制台',
                'orders': '訂單管理',
                'wishlist': '收藏夾',
                'help': '幫助中心',
                'faq': '常見問題',
                'privacy': '隱私政策',
                'terms': '使用條款',
                'shipping': '配送說明',
                'returns': '退換政策',
                'categories': '商品分類',
                'subscribe': '訂閱',
                'more': '更多',
                'menu': '選單',
                'close': '關閉',
                'back': '返回',
                'submit': '提交',
                'cancel': '取消',
                'save': '保存',
                'delete': '刪除',
                'edit': '編輯',
                'update': '更新',
                'welcome': '歡迎',
                'password': '密碼',
                'email': '電子郵件',
                'phone': '電話',
                'address': '地址'
            },
            # 法语
            'fr': {
                'home': 'Accueil',
                'about': 'À propos',
                'contact': 'Contact',
                'products': 'Produits',
                'services': 'Services',
                'news': 'Actualités',
                'search': 'Rechercher',
                'login': 'Connexion',
                'register': "S'inscrire",
                'account': 'Mon compte',
                'cart': 'Panier',
                'checkout': 'Paiement',
                'logout': 'Déconnexion',
                'profile': 'Profil',
                'settings': 'Paramètres',
                'dashboard': 'Tableau de bord',
                'orders': 'Commandes',
                'wishlist': 'Liste de souhaits',
                'help': 'Aide',
                'faq': 'FAQ',
                'privacy': 'Confidentialité',
                'terms': "Conditions d'utilisation",
                'shipping': 'Livraison',
                'returns': 'Retours',
                'categories': 'Catégories',
                'subscribe': "S'abonner",
                'more': 'Plus',
                'menu': 'Menu',
                'close': 'Fermer',
                'back': 'Retour',
                'submit': 'Envoyer',
                'cancel': 'Annuler',
                'save': 'Enregistrer',
                'delete': 'Supprimer',
                'edit': 'Modifier',
                'update': 'Mettre à jour',
                'welcome': 'Bienvenue',
                'password': 'Mot de passe',
                'email': 'E-mail',
                'phone': 'Téléphone',
                'address': 'Adresse'
            },
            # 德语
            'de': {
                'home': 'Startseite',
                'about': 'Über uns',
                'contact': 'Kontakt',
                'products': 'Produkte',
                'services': 'Dienstleistungen',
                'news': 'Neuigkeiten',
                'search': 'Suche',
                'login': 'Anmelden',
                'register': 'Registrieren',
                'account': 'Konto',
                'cart': 'Warenkorb',
                'checkout': 'Zur Kasse',
                'logout': 'Abmelden',
                'profile': 'Profil',
                'settings': 'Einstellungen',
                'dashboard': 'Dashboard',
                'orders': 'Bestellungen',
                'wishlist': 'Wunschliste',
                'help': 'Hilfe',
                'faq': 'FAQ',
                'privacy': 'Datenschutz',
                'terms': 'Nutzungsbedingungen',
                'shipping': 'Versand',
                'returns': 'Rückgabe',
                'categories': 'Kategorien',
                'subscribe': 'Abonnieren',
                'more': 'Mehr',
                'menu': 'Menü',
                'close': 'Schließen',
                'back': 'Zurück',
                'submit': 'Absenden',
                'cancel': 'Abbrechen',
                'save': 'Speichern',
                'delete': 'Löschen',
                'edit': 'Bearbeiten',
                'update': 'Aktualisieren',
                'welcome': 'Willkommen',
                'password': 'Passwort',
                'email': 'E-Mail',
                'phone': 'Telefon',
                'address': 'Adresse'
            },
            # 西班牙语
            'es': {
                'home': 'Inicio',
                'about': 'Sobre nosotros',
                'contact': 'Contacto',
                'products': 'Productos',
                'services': 'Servicios',
                'news': 'Noticias',
                'search': 'Buscar',
                'login': 'Iniciar sesión',
                'register': 'Registrarse',
                'account': 'Mi cuenta',
                'cart': 'Carrito',
                'checkout': 'Finalizar compra',
                'logout': 'Cerrar sesión',
                'profile': 'Perfil',
                'settings': 'Configuración',
                'dashboard': 'Panel de control',
                'orders': 'Pedidos',
                'wishlist': 'Lista de deseos',
                'help': 'Ayuda',
                'faq': 'Preguntas frecuentes',
                'privacy': 'Privacidad',
                'terms': 'Términos de uso',
                'shipping': 'Envío',
                'returns': 'Devoluciones',
                'categories': 'Categorías',
                'subscribe': 'Suscribirse',
                'more': 'Más',
                'menu': 'Menú',
                'close': 'Cerrar',
                'back': 'Volver',
                'submit': 'Enviar',
                'cancel': 'Cancelar',
                'save': 'Guardar',
                'delete': 'Eliminar',
                'edit': 'Editar',
                'update': 'Actualizar',
                'welcome': 'Bienvenido',
                'password': 'Contraseña',
                'email': 'Correo electrónico',
                'phone': 'Teléfono',
                'address': 'Dirección'
            },
            # 意大利语
            'it': {
                'home': 'Home',
                'about': 'Chi siamo',
                'contact': 'Contatti',
                'products': 'Prodotti',
                'services': 'Servizi',
                'news': 'Notizie',
                'search': 'Cerca',
                'login': 'Accedi',
                'register': 'Registrati',
                'account': 'Account',
                'cart': 'Carrello',
                'checkout': 'Checkout',
                'logout': 'Esci',
                'profile': 'Profilo',
                'settings': 'Impostazioni',
                'dashboard': 'Dashboard',
                'orders': 'Ordini',
                'wishlist': 'Lista dei desideri',
                'help': 'Aiuto',
                'faq': 'FAQ',
                'privacy': 'Privacy',
                'terms': 'Termini e condizioni',
                'shipping': 'Spedizione',
                'returns': 'Resi',
                'categories': 'Categorie',
                'subscribe': 'Iscriviti',
                'more': 'Altro',
                'menu': 'Menu',
                'close': 'Chiudi',
                'back': 'Indietro',
                'submit': 'Invia',
                'cancel': 'Annulla',
                'save': 'Salva',
                'delete': 'Elimina',
                'edit': 'Modifica',
                'update': 'Aggiorna',
                'welcome': 'Benvenuto',
                'password': 'Password',
                'email': 'Email',
                'phone': 'Telefono',
                'address': 'Indirizzo'
            }
        }
        
        self.max_retries = 3
        self.chunk_size = 4500
        
        # 加载外部词典文件（如果存在）
        self.load_dictionaries()
    
    def should_skip_translation(self, text: str, key: str = None) -> bool:
        """检查是否应该跳过翻译"""
        # 检查键名是否在技术字段列表中
        if key in self.technical_keys:
            return True
            
        # 检查是否是固定值
        if key in self.fixed_values:
            return True
            
        # 检查是否包含需要保持的URL
        for pattern in self.url_patterns:
            if re.search(pattern, text):
                return True
                
        # 检查是否包含需要保持格式的内容
        for pattern in self.format_patterns:
            if re.search(pattern, text):
                return True
                
        # 不再在这里检查品牌名，移到 translate_with_retry
        return False

    def process_game_name(self, name: str, target_lang: str) -> str:
        if target_lang not in ['ja', 'ko']:
            return name
            
        rules = self.GAME_NAME_RULES.get(target_lang, {})
        for en, translated in rules.items():
            name = name.replace(en, translated)
        return name

    def load_dictionaries(self):
        """从外部文件加载词典"""
        try:
            # 加载品牌词
            brand_file = 'brand_names.txt'
            if os.path.exists(brand_file):
                with open(brand_file, 'r', encoding='utf-8') as f:
                    self.brand_names.update(line.strip() for line in f if line.strip())
            
            # 加载特定翻译词典
            custom_dict_file = 'custom_translations.json'
            if os.path.exists(custom_dict_file):
                with open(custom_dict_file, 'r', encoding='utf-8') as f:
                    custom_dict = json.load(f)
                    for lang, translations in custom_dict.items():
                        if lang in self.custom_translations:
                            self.custom_translations[lang].update(translations)
                        else:
                            self.custom_translations[lang] = translations
            
        except Exception as e:
            print(f"加载词典文件时出错: {str(e)}")
    
    def is_brand_name(self, text: str) -> bool:
        """检查文本是否包含品牌词"""
        return text in self.brand_names
    
    def get_custom_translation(self, text: str, target_lang: str) -> str:
        """获取特定翻译，如果存在的话"""
        if target_lang in self.custom_translations:
            return self.custom_translations[target_lang].get(text.lower())
        return None
    
    def translate_with_retry(self, text: str, target_lang: str) -> str:
        """带有重试机制的翻译函数"""
        if not isinstance(text, str) or not text.strip():
            return text
        
        # 检查是否是品牌词
        if self.is_brand_name(text):
            return text
        
        # 检查是否有特定翻译
        custom_translation = self.get_custom_translation(text, target_lang)
        if custom_translation:
            return custom_translation
        
        # 提取需要保护的品牌词
        protected_words = []
        for brand in self.brand_names:
            if brand in text:
                protected_words.append(brand)
        
        # 使用占位符替换品牌词
        placeholder_map = {}
        modified_text = text
        for i, word in enumerate(protected_words):
            placeholder = f"BRAND_{i}"
            placeholder_map[placeholder] = word
            modified_text = modified_text.replace(word, placeholder)
        
        # 翻译处理
        for attempt in range(self.max_retries):
            try:
                if len(modified_text) > self.chunk_size:
                    chunks = self.chunk_text(modified_text)
                    translated_chunks = []
                    for chunk in chunks:
                        translator = GoogleTranslator(source='en', target=target_lang)
                        translated_chunk = translator.translate(chunk)
                        translated_chunks.append(translated_chunk)
                        sleep(random.uniform(1, 2))
                    translated_text = ' '.join(translated_chunks)
                else:
                    translator = GoogleTranslator(source='en', target=target_lang)
                    translated_text = translator.translate(modified_text)
                
                # 还原品牌词
                for placeholder, original in placeholder_map.items():
                    translated_text = translated_text.replace(placeholder, original)
                
                return translated_text
                
            except Exception as e:
                if attempt == self.max_retries - 1:
                    print(f"\n警告: 翻译失败 ({e}), 返回原文")
                    return text
                sleep(random.uniform(2, 4))
        
        return text

    def chunk_text(self, text: str) -> list:
        """将长文本分成更小的块"""
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        current_chunk = ""
        words = text.split()
        
        for word in words:
            if len(current_chunk) + len(word) + 1 <= self.chunk_size:
                current_chunk += " " + word if current_chunk else word
            else:
                chunks.append(current_chunk)
                current_chunk = word
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks

    def translate_value(self, value: Any, target_lang: str, pbar: tqdm, key: str = None) -> Any:
        """翻译字符串值，保持特定值不变"""
        # 如果是技术字段，使用固定值或保持原值
        if isinstance(value, str):
            if self.should_skip_translation(value, key):
                return value
            result = self.translate_with_retry(value, target_lang)
            pbar.update(1)
            return result

        if key in self.technical_keys:
            if key in self.fixed_values:
                return self.fixed_values[key]
            return value
            
        if key in ['title', 'seoTitle'] and target_lang in ['ja', 'ko']:
            return self.process_game_name(value, target_lang)

        if isinstance(value, str):
            result = self.translate_with_retry(value, target_lang)
            pbar.update(1)
            return result
        elif isinstance(value, dict):
            return self.translate_dict(value, target_lang, pbar)
        elif isinstance(value, list):
            return [self.translate_value(item, target_lang, pbar) for item in value]
        else:
            return value


    def count_translatable_items(self, data: Any, current_path: str = '') -> int:
        """计算指定路径中需要翻译的字符串数量"""
        if isinstance(data, str):
            if self.should_translate_path(current_path):
                return 1
            return 0
        elif isinstance(data, dict):
            count = 0
            for key, value in data.items():
                new_path = f"{current_path}.{key}" if current_path else key
                count += self.count_translatable_items(value, new_path)
            return count
        elif isinstance(data, list):
            count = 0
            # 修复这里的 value 引用错误
            for i, item in enumerate(data):  # 改 value 为 data
                count += self.count_translatable_items(item, f"{current_path}[{i}]")
            return count
        return 0

     
    def should_translate_path(self, current_path: str) -> bool:
        """检查当前路径是否需要翻译"""
        print(f"\n当前检查路径: {current_path}")
        print(f"目标路径: {self.update_paths}")
        return current_path.startswith('games.sprunki-phase-5')

    def translate_dict(self, data: Dict, target_lang: str, pbar: tqdm, current_path: str = '') -> Dict:
        """递归翻译字典中的指定路径的值"""
        translated_data = {}
        
        for key, value in data.items():
            new_path = f"{current_path}.{key}" if current_path else key
            print(f"正在处理: {new_path}")

            # 检查是否是目标路径
            if new_path == 'games.sprunki-phase-5':
                print(f"\n找到目标节点: {new_path}")
                print("开始翻译内容...")
                if isinstance(value, dict):
                    translated_data[key] = self.translate_content(value, target_lang, pbar)
                else:
                    translated_data[key] = value
            elif isinstance(value, dict):
                translated_data[key] = self.translate_dict(value, target_lang, pbar, new_path)
            else:
                translated_data[key] = value

        return translated_data


    def translate_dict_content(self, data: Dict, target_lang: str, pbar: tqdm) -> Dict:
        """翻译字典中的所有内容"""
        translated = {}
        for key, value in data.items():
            if isinstance(value, dict):
                translated[key] = self.translate_dict_content(value, target_lang, pbar)
            elif isinstance(value, list):
                translated[key] = [self.translate_value(item, target_lang, pbar) for item in value]
            elif isinstance(value, str):
                print(f"翻译文本: {value}")
                translated[key] = self.translate_value(value, target_lang, pbar)
            else:
                translated[key] = value
        return translated
        
    def translate_value(self, value: Any, target_lang: str, pbar: tqdm, current_path: str = '') -> Any:
        """翻译值，考虑路径"""
        if not isinstance(value, str):
            return value
            
        if self.should_skip_translation(value, current_path):
            return value
            
        try:
            print(f"正在翻译: {value[:50]}...")  # 添加调试信息
            result = self.translate_with_retry(value, target_lang)
            pbar.update(1)
            return result
        except Exception as e:
            print(f"翻译错误: {str(e)}")
            return value

        
    def translate_all(self, input_dir: str = '.'):
        try:
            # 读取英文源文件
            input_file = os.path.join(input_dir, 'en.json')
            with open(input_file, 'r', encoding='utf-8') as f:
                en_data = json.load(f)

            # 是否指定了特定路径
            is_specific_translation = len(self.update_paths) > 0
            if is_specific_translation:
                print(f"指定翻译路径: {self.update_paths}")
            else:
                print("全量翻译模式")

            for lang_code, lang_name in self.target_languages.items():
                print(f"\n[{lang_name}] 开始翻译...")
                
                output_filename = 'zh.json' if lang_code in ['zh', 'zh-CN'] else f"{lang_code.lower()}.json"
                # 读取目标语言文件（如果存在）
                target_file = os.path.join(input_dir, output_filename)
                if os.path.exists(target_file):
                    with open(target_file, 'r', encoding='utf-8') as f:
                        target_data = json.load(f)
                else:
                    target_data = {}

                if is_specific_translation:
                    # 特定路径翻译
                    for path in self.update_paths:
                        keys = path.split('.')
                        # 获取源数据
                        source_content = en_data
                        for key in keys:
                            source_content = source_content[key]
                        
                        print(f"\n更新路径 {path} 的内容:")
                        print(json.dumps(source_content, indent=2))
                        
                        # 在目标数据中创建或更新路径
                        current = target_data
                        for key in keys[:-1]:
                            if key not in current:
                                current[key] = {}
                            current = current[key]
                        
                        # 翻译并覆盖特定路径的内容
                        with tqdm(total=len(str(source_content).split()), desc="翻译进度") as pbar:
                            current[keys[-1]] = self.translate_content(
                                source_content,
                                lang_code,
                                pbar
                            )
                else:
                    # 全量翻译
                    with tqdm(total=len(str(en_data).split()), desc="翻译进度") as pbar:
                        target_data = self.translate_content(
                            en_data,
                            lang_code,
                            pbar
                        )

                # 保存翻译结果
                with open(target_file, 'w', encoding='utf-8') as f:
                    json.dump(target_data, f, ensure_ascii=False, indent=2)

                print(f"✓ 已完成 {lang_name} 翻译")

        except Exception as e:
            print(f"错误: {str(e)}")
            traceback.print_exc()
            sys.exit(1)

    def translate_content(self, data: Any, target_lang: str, pbar: tqdm) -> Any:
        """递归翻译内容"""
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                print(f"处理key: {key}")
                result[key] = self.translate_content(value, target_lang, pbar)
            return result
            
        elif isinstance(data, list):
            # 修复这里的 value 引用错误
            return [self.translate_content(item, target_lang, pbar) for item in data]  # 改 value 为 data
            
        elif isinstance(data, str):
            if not self.should_skip_translation(data):
                print(f"翻译: {data}")
                translated = self.translate_with_retry(data, target_lang)
                pbar.update(1)
                return translated
            return data
            
        return data

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='翻译内容')
    parser.add_argument('game_id', type=str, nargs='?', help='要翻译的游戏ID（可选）')
    
    args = parser.parse_args()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    translator = JSONTranslator()
    
    try:
        with open(os.path.join(current_dir, 'en.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            if args.game_id:
                if 'games' in data and args.game_id in data['games']:
                    target_content = data['games'][args.game_id]
                    print(f"\n需要翻译的游戏ID: {args.game_id}")
                    print("\n需要翻译的内容:")
                    print(json.dumps(target_content, indent=2))
                    translator.update_paths = [f'games.{args.game_id}']
                else:
                    print(f"未找到游戏 {args.game_id} 的内容！")
                    return
            else:
                print("\n全文翻译模式")
                translator.update_paths = []
                
            print("\n开始翻译，目标路径:", translator.update_paths if translator.update_paths else "全文")
            translator.translate_all(current_dir)
            
    except FileNotFoundError:
        print("错误：未找到 en.json 文件")
    except json.JSONDecodeError:
        print("错误：en.json 文件格式不正确")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()