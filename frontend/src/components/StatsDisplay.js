import React, { useState, useEffect } from 'react';
import { Database, FileText, RefreshCw, Loader2, AlertCircle, Trash2, X } from 'lucide-react';
import axios from 'axios';

const StatsDisplay = ({ stats, onStatsUpdate }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showClearDialog, setShowClearDialog] = useState(false);
  const [isClearing, setIsClearing] = useState(false);

  const fetchStats = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.get('/stats');
      onStatsUpdate(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
      setError('Failed to fetch database statistics');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (!stats) {
      fetchStats();
    }
  }, [stats, onStatsUpdate]);

  const handleRefresh = () => {
    fetchStats();
  };

  const handleClearDatabase = async () => {
    setIsClearing(true);
    setError(null);

    try {
      const response = await axios.delete('/clear-database');
      if (response.data.status === 'success') {
        // Refresh stats after clearing
        await fetchStats();
        setShowClearDialog(false);
        // Show success message (you could add a toast notification here)
        console.log('Database cleared successfully:', response.data.message);
      }
    } catch (error) {
      console.error('Error clearing database:', error);
      setError('Failed to clear database');
    } finally {
      setIsClearing(false);
    }
  };

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="p-6">
          <div className="text-center">
            <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Error Loading Stats
            </h3>
            <p className="text-sm text-gray-600 mb-4">{error}</p>
            <button
              onClick={handleRefresh}
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <RefreshCw className="h-4 w-4 mr-2" />
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Database className="h-6 w-6 text-blue-600" />
              <h2 className="text-lg font-semibold text-gray-900">
                Database Statistics
              </h2>
            </div>
            <div className="flex items-center space-x-2">
              {stats && stats.total_chunks > 0 && (
                <button
                  onClick={() => setShowClearDialog(true)}
                  disabled={isClearing}
                  className="flex items-center space-x-2 px-3 py-2 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
                >
                  <Trash2 className="h-4 w-4" />
                  <span>Clear Database</span>
                </button>
              )}
              <button
                onClick={handleRefresh}
                disabled={isLoading}
                className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors disabled:opacity-50"
              >
                {isLoading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <RefreshCw className="h-4 w-4" />
                )}
                <span>Refresh</span>
              </button>
            </div>
          </div>
          <p className="text-sm text-gray-600 mt-2">
            Overview of your knowledge base and document collection
          </p>
        </div>
      </div>

      {/* Stats Grid */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Total Chunks */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <FileText className="h-8 w-8 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Chunks</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {stats.total_chunks || 0}
                </p>
              </div>
            </div>
          </div>

          {/* Collection Name */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Database className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Collection</p>
                <p className="text-lg font-semibold text-gray-900">
                  {stats.collection_name || 'N/A'}
                </p>
              </div>
            </div>
          </div>

          {/* Status */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className={`h-8 w-8 rounded-full flex items-center justify-center ${
                  stats.status === 'active' ? 'bg-green-100' : 'bg-gray-100'
                }`}>
                  <div className={`h-3 w-3 rounded-full ${
                    stats.status === 'active' ? 'bg-green-500' : 'bg-gray-400'
                  }`} />
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Status</p>
                <p className="text-lg font-semibold text-gray-900 capitalize">
                  {stats.status || 'Unknown'}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="text-center">
            <Loader2 className="h-8 w-8 text-blue-600 mx-auto animate-spin mb-4" />
            <p className="text-sm text-gray-600">Loading statistics...</p>
          </div>
        </div>
      )}

      {/* No Data State */}
      {stats && stats.total_chunks === 0 && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="text-center">
            <FileText className="h-12 w-12 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No Documents Yet
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Upload some documents to start building your knowledge base.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              Go to Upload
            </button>
          </div>
        </div>
      )}

      {/* Additional Info */}
      {stats && stats.total_chunks > 0 && (
        <div className="bg-blue-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-blue-900 mb-2">
            📊 Knowledge Base Overview
          </h4>
          <div className="text-sm text-blue-800 space-y-1">
            <p>• Your knowledge base contains {stats.total_chunks} document chunks</p>
            <p>• Each chunk is optimized for semantic search and retrieval</p>
            <p>• Chunks are automatically indexed for fast query responses</p>
            <p>• You can ask questions about any content in your uploaded documents</p>
          </div>
        </div>
      )}

      {/* Clear Database Confirmation Dialog */}
      {showClearDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="flex-shrink-0">
                    <div className="h-10 w-10 bg-red-100 rounded-full flex items-center justify-center">
                      <Trash2 className="h-5 w-5 text-red-600" />
                    </div>
                  </div>
                  <h3 className="text-lg font-medium text-gray-900">
                    Clear Database
                  </h3>
                </div>
                <button
                  onClick={() => setShowClearDialog(false)}
                  className="text-gray-400 hover:text-gray-600"
                  disabled={isClearing}
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              
              <div className="mb-6">
                <p className="text-sm text-gray-600 mb-4">
                  Are you sure you want to clear the entire database? This action will permanently delete all {stats?.total_chunks || 0} document chunks and cannot be undone.
                </p>
                <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                  <p className="text-sm text-red-800">
                    <strong>Warning:</strong> This will remove all uploaded documents and their embeddings from the knowledge base.
                  </p>
                </div>
              </div>
              
              <div className="flex items-center justify-end space-x-3">
                <button
                  onClick={() => setShowClearDialog(false)}
                  disabled={isClearing}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  onClick={handleClearDatabase}
                  disabled={isClearing}
                  className="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-lg hover:bg-red-700 focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 flex items-center space-x-2"
                >
                  {isClearing ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span>Clearing...</span>
                    </>
                  ) : (
                    <>
                      <Trash2 className="h-4 w-4" />
                      <span>Clear Database</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StatsDisplay;



