import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';

// --- Configuration ---
const API_BASE_URL = 'http://127.0.0.1:5000'; // Your Flask backend URL
const ARTICLES_PER_PAGE = 5;

// --- Helper Components ---

// SVG Icon for Refresh
const RefreshIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h5M20 20v-5h-5M4 4a12 12 0 0116 16" />
  </svg>
);

// Loading Spinner
const Spinner = () => (
  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-gray-900"></div>
);

// --- Main Components ---

const ArticleCard = ({ article }) => {
  const formattedDate = article.published_at 
    ? new Date(article.published_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
    : 'Date not available';

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 transition-transform transform hover:scale-[1.02]">
      <div className="mb-4">
        <p className="text-sm text-gray-500">{article.source_name} • {formattedDate}</p>
        <h2 className="text-2xl font-bold text-gray-800 mt-1">{article.headline}</h2>
      </div>
      <p className="text-gray-600 leading-relaxed mb-4">{article.summary}</p>
      <a href={article.source_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline font-semibold">
        Read Full Article &rarr;
      </a>
    </div>
  );
};

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  if (totalPages <= 1) return null;

  const pageNumbers = Array.from({ length: totalPages }, (_, i) => i + 1);

  return (
    <div className="flex justify-center items-center space-x-2 mt-8">
      {pageNumbers.map(number => (
        <button
          key={number}
          onClick={() => onPageChange(number)}
          className={`px-4 py-2 rounded-md text-sm font-medium ${
            currentPage === number 
            ? 'bg-blue-600 text-white' 
            : 'bg-white text-gray-700 hover:bg-gray-100'
          }`}
        >
          {number}
        </button>
      ))}
    </div>
  );
};

const App = () => {
  // State management
  const [articles, setArticles] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('general');
  const [newCategory, setNewCategory] = useState('');
  const [loading, setLoading] = useState({ articles: true, categories: true, refresh: null });
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);

  // --- Data Fetching ---
  const fetchCategories = async () => {
    try {
      setLoading(prev => ({ ...prev, categories: true }));
      const response = await axios.get(`${API_BASE_URL}/articles/categories`);
      setCategories(response.data);
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
      const url = category === 'general'
        ? `${API_BASE_URL}/articles/`
        : `${API_BASE_URL}/articles/by-category/${category}`;
      const response = await axios.get(url);
      setArticles(response.data);
      setCurrentPage(1); // Reset to first page on new data
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

  // --- Event Handlers ---
  const handleCategorySelect = (categoryName) => {
    setSelectedCategory(categoryName);
    fetchArticles(categoryName);
  };

  const handleRefresh = async (categoryName) => {
    try {
      setError(null);
      setLoading(prev => ({ ...prev, refresh: categoryName }));
      await axios.get(`${API_BASE_URL}/news/process/${categoryName}`);
      // After a successful refresh, refetch the articles for the current view
      await fetchArticles(selectedCategory);
    } catch (err) {
      console.error(`Error refreshing category ${categoryName}:`, err);
      if (err.response && err.response.status === 429) {
        setError(err.response.data.message); // Display the 30-min warning
      } else {
        setError(`Could not refresh "${categoryName}". Please try again later.`);
      }
    } finally {
      setLoading(prev => ({ ...prev, refresh: null }));
    }
  };

  const handleAddCategory = async (e) => {
    e.preventDefault();
    if (!newCategory.trim()) return;
    const categoryName = newCategory.trim().toLowerCase();
    
    try {
      setError(null);
      setLoading(prev => ({ ...prev, refresh: categoryName }));
      await axios.get(`${API_BASE_URL}/news/process/${categoryName}`);
      setNewCategory('');
      await fetchCategories(); // Refresh the category list to show the new one
      handleCategorySelect(categoryName); // Automatically switch to the new category view
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
  
  // --- Memoized Pagination Logic ---
  const paginatedArticles = useMemo(() => {
    const startIndex = (currentPage - 1) * ARTICLES_PER_PAGE;
    return articles.slice(startIndex, startIndex + ARTICLES_PER_PAGE);
  }, [articles, currentPage]);

  const totalPages = Math.ceil(articles.length / ARTICLES_PER_PAGE);

  return (
    <div className="bg-gray-50 min-h-screen font-sans">
      <div className="container mx-auto p-4 md:p-8">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-extrabold text-gray-800">News-Man</h1>
          <p className="text-lg text-gray-500 mt-2">Your Personal AI News Curator</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <aside className="lg:col-span-1">
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 sticky top-8">
              <h3 className="font-bold text-lg mb-4">Categories</h3>
              <ul className="space-y-2">
                <li>
                  <button onClick={() => handleCategorySelect('general')} className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors ${selectedCategory === 'general' ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'}`}>
                    General Feed
                  </button>
                </li>
                {categories.map(cat => (
                  <li key={cat.id} className="flex items-center justify-between">
                    <button onClick={() => handleCategorySelect(cat.category_name)} className={`flex-grow text-left px-3 py-2 rounded-md text-sm font-medium transition-colors ${selectedCategory === cat.category_name ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'}`}>
                      {cat.category_name.charAt(0).toUpperCase() + cat.category_name.slice(1)}
                    </button>
                    <button onClick={() => handleRefresh(cat.category_name)} className="p-2 rounded-full hover:bg-gray-200 text-gray-500" title={`Refresh ${cat.category_name}`}>
                      {loading.refresh === cat.category_name ? <Spinner /> : <RefreshIcon />}
                    </button>
                  </li>
                ))}
              </ul>
              
              <form onSubmit={handleAddCategory} className="mt-6 border-t pt-4">
                 <input
                  type="text"
                  value={newCategory}
                  onChange={(e) => setNewCategory(e.target.value)}
                  placeholder="Add new category..."
                  className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
                <button type="submit" className="w-full bg-blue-600 text-white rounded-md px-3 py-2 text-sm font-semibold mt-2 hover:bg-blue-700 transition-colors" disabled={loading.refresh}>
                  {loading.refresh && loading.refresh === newCategory.trim().toLowerCase() ? 'Processing...' : 'Add & Fetch'}
                </button>
              </form>
            </div>
          </aside>

          {/* Main Content */}
          <main className="lg:col-span-3">
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg relative mb-6" role="alert">
                <strong className="font-bold">Error: </strong>
                <span className="block sm:inline">{error}</span>
              </div>
            )}
            
            {loading.articles ? (
              <div className="text-center p-10">
                <Spinner />
                <p className="mt-2 text-gray-500">Loading Articles...</p>
              </div>
            ) : (
              <div className="space-y-6">
                {paginatedArticles.length > 0 ? (
                  paginatedArticles.map(article => <ArticleCard key={article.id} article={article} />)
                ) : (
                  <div className="text-center bg-white p-10 rounded-lg shadow-sm border">
                    <p className="text-gray-500">No articles found for "{selectedCategory}".</p>
                  </div>
                )}
                <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} />
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
};

export default App;

