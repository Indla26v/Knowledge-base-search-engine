import React, { useState } from 'react';
import { Upload, Search, FileText, Brain, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import FileUpload from './components/FileUpload';
import QueryInterface from './components/QueryInterface';
import ResultsDisplay from './components/ResultsDisplay';
import StatsDisplay from './components/StatsDisplay';

function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [queryResult, setQueryResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [stats, setStats] = useState(null);

  const handleQueryResult = (result) => {
    setQueryResult(result);
  };

  const handleLoading = (loading) => {
    setIsLoading(loading);
  };

  const handleStatsUpdate = (newStats) => {
    setStats(newStats);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <Brain className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">
                Knowledge-base Search Engine
              </h1>
            </div>
            <div className="text-sm text-gray-500">
              RAG-powered document search & Q&A
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('upload')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'upload'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <Upload className="h-4 w-4" />
                <span>Upload Documents</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('query')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'query'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <Search className="h-4 w-4" />
                <span>Ask Questions</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('stats')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'stats'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-2">
                <FileText className="h-4 w-4" />
                <span>Database Stats</span>
              </div>
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Loading Indicator */}
          {isLoading && (
            <div className="fixed top-4 right-4 bg-white rounded-lg shadow-lg p-4 flex items-center space-x-2 z-50">
              <Loader2 className="h-5 w-5 animate-spin text-blue-600" />
              <span className="text-sm font-medium">Processing...</span>
            </div>
          )}

          {/* Tab Content */}
          {activeTab === 'upload' && (
            <div className="fade-in">
              <FileUpload onStatsUpdate={handleStatsUpdate} onLoading={handleLoading} />
            </div>
          )}

          {activeTab === 'query' && (
            <div className="fade-in">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <QueryInterface 
                  onQueryResult={handleQueryResult} 
                  onLoading={handleLoading}
                />
                <ResultsDisplay result={queryResult} />
              </div>
            </div>
          )}

          {activeTab === 'stats' && (
            <div className="fade-in">
              <StatsDisplay stats={stats} onStatsUpdate={handleStatsUpdate} />
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <div className="text-center text-sm text-gray-500">
            <p>Built with FastAPI, ChromaDB, and React • Powered by RAG</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;



