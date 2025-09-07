import React, { useState, useEffect, useMemo } from 'react';

// --- Configuration ---
const API_BASE_URL = 'http://127.0.0.1:5000';
const ARTICLES_PER_PAGE = 5;

// --- Enhanced Icons ---
const RefreshIcon = ({ className = "h-4 w-4" }) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h5M20 20v-5h-5M4 4a12 12 0 0116 16" />
  </svg>
);

const NewsIcon = () => (
  <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9.5a2.5 2.5 0 00-2.5-2.5H15" />
  </svg>
);

const ExternalLinkIcon = () => (
  <svg className="h-4 w-4 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
  </svg>
);

const PlusIcon = () => (
  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
  </svg>
);

// Enhanced Loading Spinner with pulse effect
const Spinner = ({ size = "h-5 w-5" }) => (
  <div className={`animate-spin rounded-full ${size} border-2 border-transparent border-t-current border-r-current`}></div>
);

// Floating particles background
const FloatingParticles = () => (
  <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
    {[...Array(20)].map((_, i) => (
      <div
        key={i}
        className="absolute w-1 h-1 bg-green-300 rounded-full opacity-30 animate-pulse"
        style={{
          left: `${Math.random() * 100}%`,
          top: `${Math.random() * 100}%`,
          animationDelay: `${Math.random() * 2}s`,
          animationDuration: `${3 + Math.random() * 2}s`
        }}
      />
    ))}
  </div>
);

// Enhanced Article Card with glassmorphism and hover effects
const ArticleCard = ({ article, index }) => {
  const formattedDate = article.published_at 
    ? new Date(article.published_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
    : 'Date not available';

  return (
    <div 
      className="group relative backdrop-blur-sm bg-white/60 border border-white/20 rounded-2xl p-6 shadow-xl hover:shadow-2xl transition-all duration-500 hover:scale-[1.02] hover:bg-white/80 animate-fade-in"
      style={{ animationDelay: `${index * 100}ms` }}
    >
      {/* Gradient border effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-green-400/20 to-red-400/20 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-sm"></div>
      
      <div className="relative z-10">
        <div className="mb-4">
          <div className="flex items-center justify-between mb-2">
            <span className="inline-flex items-center px-3 py-1 text-xs font-medium text-green-800 bg-green-100/70 rounded-full">
              {article.source_name}
            </span>
            <span className="text-sm text-gray-500">{formattedDate}</span>
          </div>
          <h2 className="text-xl font-bold text-gray-800 leading-tight group-hover:text-green-700 transition-colors duration-300">
            {article.headline}
          </h2>
        </div>
        
        <p className="text-gray-600 leading-relaxed mb-6 line-clamp-3">{article.summary}</p>
        
        <a 
          href={article.source_url} 
          target="_blank" 
          rel="noopener noreferrer" 
          className="inline-flex items-center text-green-600 hover:text-red-600 font-semibold transition-all duration-300 group-hover:translate-x-1"
        >
          Read Full Article
          <ExternalLinkIcon />
        </a>
      </div>
    </div>
  );
};

// Enhanced Pagination with modern design
const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  if (totalPages <= 1) return null;

  const pageNumbers = Array.from({ length: totalPages }, (_, i) => i + 1);

  return (
    <div className="flex justify-center items-center space-x-3 mt-12">
      <div className="flex items-center space-x-2 backdrop-blur-sm bg-white/80 rounded-2xl p-2 shadow-lg border border-white/20">
        {pageNumbers.map(number => (
          <button
            key={number}
            onClick={() => onPageChange(number)}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 ${
              currentPage === number 
                ? 'bg-gradient-to-r from-green-600 to-red-600 text-white shadow-lg scale-110' 
                : 'text-gray-700 hover:bg-green-50 hover:scale-105'
            }`}
          >
            {number}
          </button>
        ))}
      </div>
    </div>
  );
};


const App = () => {
  const [articles, setArticles] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('general');
  const [newCategory, setNewCategory] = useState('');
  const [loading, setLoading] = useState({ articles: true, categories: true, refresh: null });
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);

  const apiRequest = async (url) => {
    const response = await fetch(url);
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: "An unknown error occurred." }));
        const error = new Error(errorData.message || 'Request failed');
        error.response = { status: response.status, data: errorData };
        throw error;
    }
    return response.json();
  };

  const fetchCategories = async () => {
    try {
      setLoading(prev => ({ ...prev, categories: true }));
      const data = await apiRequest(`${API_BASE_URL}/articles/categories`);
      setCategories(data);
    } catch (err) {
      console.error("Error fetching categories:", err);
      setError('Could not load categories. Please try refreshing the page.');
    } finally {
      setLoading(prev => ({ ...prev, categories: false }));
    }
  };

  const fetchArticles = async (category) => {
    try {
      setError(null);
      setLoading(prev => ({ ...prev, articles: true }));
      const url = category === 'general' ? `${API_BASE_URL}/articles/` : `${API_BASE_URL}/articles/by-category/${category}`;
      const data = await apiRequest(url);
      setArticles(data);
      setCurrentPage(1);
    } catch (err) {
      console.error(`Error fetching articles for ${category}:`, err);
      setError(`Could not load articles for "${category}".`);
      setArticles([]);
    } finally {
      setLoading(prev => ({ ...prev, articles: false }));
    }
  };

  useEffect(() => {
    fetchCategories();
    fetchArticles('general');
  }, []);

  const handleCategorySelect = (categoryName) => {
    setSelectedCategory(categoryName);
    fetchArticles(categoryName);
  };

  const handleRefresh = async (categoryName) => {
    try {
      setError(null);
      setLoading(prev => ({ ...prev, refresh: categoryName }));
      await apiRequest(`${API_BASE_URL}/news/process-and-store/${categoryName}`);
      await fetchArticles(selectedCategory);
    } catch (err) {
      console.error(`Error refreshing category ${categoryName}:`, err);
      if (err.response && err.response.status === 429) {
        setError(err.response.data.message);
      } else {
        setError(`Could not refresh "${categoryName}". Please try again later.`);
      }
    } finally {
      setLoading(prev => ({ ...prev, refresh: null }));
    }
  };

  const handleAddCategory = async (e) => {
    if (e) e.preventDefault();
    if (!newCategory.trim()) return;
    const categoryName = newCategory.trim().toLowerCase();
    
    try {
      setError(null);
      setLoading(prev => ({ ...prev, refresh: categoryName }));
      await apiRequest(`${API_BASE_URL}/news/process-and-store/${categoryName}`);
      setNewCategory('');
      await fetchCategories();
      handleCategorySelect(categoryName);
    } catch (err) {
      console.error(`Error adding category ${categoryName}:`, err);
       if (err.response && err.response.status === 429) {
        setError(err.response.data.message);
      } else {
        setError(`Could not add "${categoryName}".`);
      }
    } finally {
      setLoading(prev => ({ ...prev, refresh: null }));
    }
  };
  
  const paginatedArticles = useMemo(() => {
    const startIndex = (currentPage - 1) * ARTICLES_PER_PAGE;
    return articles.slice(startIndex, startIndex + ARTICLES_PER_PAGE);
  }, [articles, currentPage]);

  const totalPages = Math.ceil(articles.length / ARTICLES_PER_PAGE);

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-red-50 relative overflow-hidden">
      <FloatingParticles />
      <div className="absolute inset-0 bg-gradient-to-r from-green-400/10 to-red-400/10 animate-pulse"></div>
      
      <div className="relative z-10 container mx-auto p-4 md:p-8">
        <header className="text-center mb-16 animate-fade-in">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-green-600 to-red-600 text-white mb-6 shadow-2xl">
            <NewsIcon />
          </div>
          <h1 className="text-6xl font-extrabold bg-gradient-to-r from-green-600 to-red-600 bg-clip-text text-transparent mb-4">
            News-Man
          </h1>
          <p className="text-xl text-gray-600 font-light">Your Personal AI News Curator</p>
          <div className="mt-4 w-32 h-1 bg-gradient-to-r from-green-600 to-red-600 mx-auto rounded-full"></div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <aside className="lg:col-span-1">
            <div className="backdrop-blur-sm bg-white/60 p-6 rounded-2xl shadow-xl border border-white/20 sticky top-8">
              <h3 className="font-bold text-xl mb-6 text-gray-800 flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                Categories
              </h3>
              
              <ul className="space-y-3">
                <li>
                  <button onClick={() => handleCategorySelect('general')} className={`w-full text-left px-4 py-3 rounded-xl text-sm font-medium transition-all duration-300 ${ selectedCategory === 'general' ? 'bg-gradient-to-r from-green-600 to-red-600 text-white shadow-lg scale-105' : 'text-gray-600 hover:bg-green-50 hover:scale-105'}`}>
                    🌍 General Feed
                  </button>
                </li>
                
                {categories.map((cat) => (
                  <li key={cat.id} className="flex items-center justify-between group">
                    <button onClick={() => handleCategorySelect(cat.category_name)} className={`flex-grow text-left px-4 py-3 rounded-xl text-sm font-medium transition-all duration-300 ${ selectedCategory === cat.category_name ? 'bg-gradient-to-r from-green-600 to-red-600 text-white shadow-lg scale-105' : 'text-gray-600 hover:bg-green-50 hover:scale-105'}`}>
                      📰 {cat.category_name.charAt(0).toUpperCase() + cat.category_name.slice(1)}
                    </button>
                    <button onClick={() => handleRefresh(cat.category_name)} className="ml-2 p-2 rounded-full hover:bg-green-100 text-gray-500 hover:text-green-600 transition-all duration-300 hover:scale-110" title={`Refresh ${cat.category_name}`}>
                      {loading.refresh === cat.category_name ? <Spinner size="h-4 w-4" /> : <RefreshIcon className="h-4 w-4" />}
                    </button>
                  </li>
                ))}
              </ul>
              
              <div className="mt-8 pt-6 border-t border-gray-200/50">
                  <div className="relative">
                    <input
                      type="text" value={newCategory} onChange={(e) => setNewCategory(e.target.value)}
                      placeholder="Add & Fetch Category..."
                      className="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300 bg-white/70 backdrop-blur-sm"
                      onKeyPress={(e) => { if (e.key === 'Enter') { handleAddCategory(e); } }}
                    />
                  </div>
              </div>
            </div>
          </aside>

          <main className="lg:col-span-3">
            {error && (
              <div className="bg-gradient-to-r from-red-100 to-pink-100 border-2 border-red-200 text-red-700 px-6 py-4 rounded-2xl relative mb-6 backdrop-blur-sm shadow-lg animate-fade-in" role="alert">
                <div className="flex items-center">
                  <div className="w-2 h-2 bg-red-500 rounded-full mr-3"></div>
                  <strong className="font-bold">Error: </strong>
                  <span className="ml-2">{error}</span>
                </div>
              </div>
            )}
            
            <div className="space-y-8">
              {loading.articles ? (
                Array.from({ length: 3 }).map((_, index) => <SkeletonCard key={index} />)
              ) : paginatedArticles.length > 0 ? (
                  paginatedArticles.map((article, index) => <ArticleCard key={article.id} article={article} index={index} />)
              ) : (
                <div className="text-center backdrop-blur-sm bg-white/80 p-16 rounded-2xl shadow-xl border border-white/20">
                  <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-6 text-gray-400">
                    <NewsIcon />
                  </div>
                  <p className="text-xl text-gray-500 mb-2">No articles found</p>
                  <p className="text-gray-400">for "{selectedCategory}" category</p>
                </div>
              )}
              <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} />
            </div>
          </main>
        </div>
      </div>
    </div>
  );
};

export default App;

