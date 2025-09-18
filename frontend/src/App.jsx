import React, { useState, useEffect, useMemo } from "react";

// --- Configuration ---
// const API_BASE_URL = 'http://127.0.0.1:5000';
//Just base changes for testing
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000";
const ARTICLES_PER_PAGE = 5;

// --- Icon Components ---
const RefreshIcon = ({ className = "h-4 w-4" }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    className={className}
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M4 4v5h5M20 20v-5h-5M4 4a12 12 0 0116 16"
    />
  </svg>
);

const NewsIcon = () => (
  <svg
    className="h-6 w-6"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9.5a2.5 2.5 0 00-2.5-2.5H15"
    />
  </svg>
);

const ExternalLinkIcon = () => (
  <svg
    className="h-4 w-4 ml-1.5"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
    />
  </svg>
);

const Spinner = ({ size = "h-5 w-5" }) => (
  <div
    className={`animate-spin rounded-full ${size} border-2 border-transparent border-t-blue-600 border-r-blue-600`}
  ></div>
);

// ------ UI Components ----------

const SkeletonCard = () => (
  <div className="bg-white border border-gray-200 rounded-lg p-6 animate-pulse">
    <div className="h-4 bg-gray-200 rounded w-1/3 mb-3"></div>
    <div className="h-6 bg-gray-300 rounded w-3/4 mb-4"></div>
    <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
    <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
    <div className="h-4 bg-gray-200 rounded w-5/6"></div>
  </div>
);

const ArticleCard = ({ article }) => {
  const formattedDate = article.published_at
    ? new Date(article.published_at).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      })
    : "Date not available";

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 transition-shadow hover:shadow-lg">
      <div className="mb-3">
        <div className="flex items-center justify-between text-sm text-gray-500 mb-2">
          <span>{article.source_name}</span>
          <span>{formattedDate}</span>
        </div>
        <h2 className="text-2xl font-bold text-gray-900 leading-tight">
          {article.headline}
        </h2>
      </div>
      <p className="text-gray-600 leading-relaxed mb-5 line-clamp-3">
        {article.summary}
      </p>
      <a
        href={article.source_url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center text-blue-600 hover:text-blue-800 font-semibold transition-colors group"
      >
        Read Full Article
        <span className="transition-transform group-hover:translate-x-1">
          <ExternalLinkIcon />
        </span>
      </a>
    </div>
  );
};

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  if (totalPages <= 1) return null;
  const pageNumbers = Array.from({ length: totalPages }, (_, i) => i + 1);

  return (
    <nav className="flex justify-center items-center space-x-2 mt-10">
      {pageNumbers.map((number) => (
        <button
          key={number}
          onClick={() => onPageChange(number)}
          className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            currentPage === number
              ? "bg-blue-600 text-white shadow-sm"
              : "bg-white text-gray-700 hover:bg-gray-100 border"
          }`}
        >
          {number}
        </button>
      ))}
    </nav>
  );
};

//splitting Components for Better UI Control

//Another Contribution

const App = () => {
  const [articles, setArticles] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("general");
  const [newCategory, setNewCategory] = useState("");
  const [loading, setLoading] = useState({
    articles: true,
    categories: true,
    refresh: null,
  });
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);

  const apiRequest = async (url) => {
    const response = await fetch(url);
    if (!response.ok) {
      const errorData = await response
        .json()
        .catch(() => ({ message: "An unknown error occurred." }));
      const error = new Error(errorData.message || "Request failed");
      error.response = { status: response.status, data: errorData };
      throw error;
    }
    return response.json();
  };

  const fetchCategories = async () => {
    try {
      setLoading((prev) => ({ ...prev, categories: true }));
      const data = await apiRequest(`${API_BASE_URL}/articles/categories`);
      setCategories(data);
    } catch (err) {
      console.error("Error fetching categories:", err);
      setError("Could not load categories. Please try refreshing the page.");
    } finally {
      setLoading((prev) => ({ ...prev, categories: false }));
    }
  };

  const fetchArticles = async (category) => {
    try {
      setError(null);
      setLoading((prev) => ({ ...prev, articles: true }));
      const url =
        category === "general"
          ? `${API_BASE_URL}/articles/`
          : `${API_BASE_URL}/articles/by-category/${category}`;
      const data = await apiRequest(url);
      setArticles(data);
      setCurrentPage(1);
    } catch (err) {
      console.error(`Error fetching articles for ${category}:`, err);
      setError(`Could not load articles for "${category}".`);
      setArticles([]);
    } finally {
      setLoading((prev) => ({ ...prev, articles: false }));
    }
  };

  useEffect(() => {
    fetchCategories();
    fetchArticles("general");
  }, []);

  const handleCategorySelect = (categoryName) => {
    setSelectedCategory(categoryName);
    fetchArticles(categoryName);
  };

  const handleRefresh = async (categoryName) => {
    try {
      setError(null);
      setLoading((prev) => ({ ...prev, refresh: categoryName }));
      await apiRequest(`${API_BASE_URL}/news/process/${categoryName}`);
      await fetchArticles(selectedCategory);
    } catch (err) {
      console.error(`Error refreshing category ${categoryName}:`, err);
      if (err.response && err.response.status === 429) {
        setError(err.response.data.message);
      } else {
        setError(
          `Could not refresh "${categoryName}". Please try again later.`
        );
      }
    } finally {
      setLoading((prev) => ({ ...prev, refresh: null }));
    }
  };

  const handleAddCategory = async (e) => {
    if (e) e.preventDefault();
    if (!newCategory.trim()) return;
    const categoryName = newCategory.trim().toLowerCase();

    try {
      setError(null);
      setLoading((prev) => ({ ...prev, refresh: categoryName }));
      await apiRequest(`${API_BASE_URL}/news/process/${categoryName}`);
      setNewCategory("");
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
      setLoading((prev) => ({ ...prev, refresh: null }));
    }
  };

  const paginatedArticles = useMemo(() => {
    const startIndex = (currentPage - 1) * ARTICLES_PER_PAGE;
    return articles.slice(startIndex, startIndex + ARTICLES_PER_PAGE);
  }, [articles, currentPage]);

  const totalPages = Math.ceil(articles.length / ARTICLES_PER_PAGE);

  return (
    <div className="min-h-screen bg-slate-100 font-sans text-slate-800">
      <div className="container mx-auto p-4 md:p-8">
        <header className="text-left mb-10 pb-4 border-b border-slate-300">
          <div className="flex items-center space-x-3">
            <NewsIcon />
            <h1 className="text-3xl font-bold text-slate-900">News-Man</h1>
          </div>
          <p className="text-md text-slate-500 mt-1">
            Your Personal AI News Curator
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <aside className="lg:col-span-1">
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 sticky top-8">
              <h3 className="font-bold text-lg mb-4 text-gray-900">
                Categories
              </h3>

              <ul className="space-y-2">
                <li>
                  <button
                    onClick={() => handleCategorySelect("general")}
                    className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      selectedCategory === "general"
                        ? "bg-blue-600 text-white"
                        : "text-gray-600 hover:bg-slate-100"
                    }`}
                  >
                    All News
                  </button>
                </li>

                {categories.map((cat) => (
                  <li
                    key={cat.id}
                    className="flex items-center justify-between group"
                  >
                    <button
                      onClick={() => handleCategorySelect(cat.category_name)}
                      className={`flex-grow text-left px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                        selectedCategory === cat.category_name
                          ? "bg-blue-600 text-white"
                          : "text-gray-600 hover:bg-slate-100"
                      }`}
                    >
                      {cat.category_name.charAt(0).toUpperCase() +
                        cat.category_name.slice(1)}
                    </button>
                    <button
                      onClick={() => handleRefresh(cat.category_name)}
                      className="ml-2 p-1.5 rounded-md hover:bg-slate-200 text-gray-500 hover:text-blue-600 transition-colors"
                      title={`Refresh ${cat.category_name}`}
                    >
                      {loading.refresh === cat.category_name ? (
                        <Spinner size="h-4 w-4" />
                      ) : (
                        <RefreshIcon className="h-4 w-4" />
                      )}
                    </button>
                  </li>
                ))}
              </ul>

              <div className="mt-6 pt-6 border-t border-gray-200">
                <form onSubmit={handleAddCategory}>
                  <input
                    type="text"
                    value={newCategory}
                    onChange={(e) => setNewCategory(e.target.value)}
                    placeholder="Add & Fetch Category..."
                    className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  />
                  <button
                    type="submit"
                    className="w-full mt-2 bg-slate-800 text-white rounded-md px-3 py-2 text-sm font-semibold hover:bg-slate-900 transition-colors disabled:opacity-50 flex items-center justify-center"
                    disabled={loading.refresh || !newCategory.trim()}
                  >
                    {loading.refresh &&
                    loading.refresh === newCategory.trim().toLowerCase() ? (
                      <Spinner size="h-4 w-4" />
                    ) : (
                      "Add Category"
                    )}
                  </button>
                </form>
              </div>
            </div>
          </aside>

          <main className="lg:col-span-3">
            {error && (
              <div
                className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md mb-6"
                role="alert"
              >
                <p className="font-bold">An Error Occurred</p>
                <p>{error}</p>
              </div>
            )}

            <div className="space-y-6">
              {loading.articles ? (
                Array.from({ length: 3 }).map((_, index) => (
                  <SkeletonCard key={index} />
                ))
              ) : paginatedArticles.length > 0 ? (
                paginatedArticles.map((article) => (
                  <ArticleCard key={article.id} article={article} />
                ))
              ) : (
                <div className="text-center bg-white p-12 rounded-lg shadow-sm border">
                  <h3 className="text-xl font-semibold text-gray-700">
                    No Articles Found
                  </h3>
                  <p className="text-gray-500 mt-2">
                    There are no articles available for "{selectedCategory}".
                  </p>
                </div>
              )}
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={setCurrentPage}
              />
            </div>
          </main>
        </div>
      </div>
    </div>
  );
};

export default App;
