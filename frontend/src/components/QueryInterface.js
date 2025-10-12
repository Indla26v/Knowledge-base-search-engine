import React, { useState } from 'react';
import { Search, Send, Loader2 } from 'lucide-react';
import axios from 'axios';

const QueryInterface = ({ onQueryResult, onLoading }) => {
  const [question, setQuestion] = useState('');
  const [topK, setTopK] = useState(5);
  const [includeSources, setIncludeSources] = useState(true);
  const [isQuerying, setIsQuerying] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim() || isQuerying) return;

    setIsQuerying(true);
    onLoading(true);

    try {
      const formData = new FormData();
      formData.append('question', question);
      formData.append('top_k', topK.toString());
      formData.append('include_sources', includeSources.toString());

      const response = await axios.post('/query', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      onQueryResult(response.data);
    } catch (error) {
      console.error('Query error:', error);
      onQueryResult({
        answer: 'Error processing your question. Please try again.',
        sources: [],
        num_sources: 0,
        query: question
      });
    } finally {
      setIsQuerying(false);
      onLoading(false);
    }
  };

  const exampleQuestions = [
    "What is the main topic of the documents?",
    "Can you summarize the key points?",
    "What are the important findings?",
    "How does this relate to machine learning?",
    "What are the benefits mentioned?"
  ];

  const handleExampleClick = (example) => {
    setQuestion(example);
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border">
      <div className="p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Ask Questions
        </h2>
        <p className="text-sm text-gray-600 mb-6">
          Ask questions about your uploaded documents and get AI-powered answers 
          based on the content.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Question Input */}
          <div>
            <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
              Your Question
            </label>
            <div className="relative">
              <textarea
                id="question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask a question about your documents..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
                rows={3}
                disabled={isQuerying}
              />
              <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>

          {/* Advanced Options */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label htmlFor="topK" className="block text-sm font-medium text-gray-700 mb-2">
                Number of Sources
              </label>
              <select
                id="topK"
                value={topK}
                onChange={(e) => setTopK(parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                disabled={isQuerying}
              >
                <option value={3}>3 sources</option>
                <option value={5}>5 sources</option>
                <option value={10}>10 sources</option>
                <option value={15}>15 sources</option>
              </select>
            </div>

            <div className="flex items-center">
              <input
                id="includeSources"
                type="checkbox"
                checked={includeSources}
                onChange={(e) => setIncludeSources(e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                disabled={isQuerying}
              />
              <label htmlFor="includeSources" className="ml-2 block text-sm text-gray-700">
                Include source citations
              </label>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={!question.trim() || isQuerying}
            className="w-full flex items-center justify-center px-4 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isQuerying ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin mr-2" />
                Processing...
              </>
            ) : (
              <>
                <Send className="h-5 w-5 mr-2" />
                Ask Question
              </>
            )}
          </button>
        </form>

        {/* Example Questions */}
        <div className="mt-6">
          <h4 className="text-sm font-medium text-gray-700 mb-3">
            Example Questions:
          </h4>
          <div className="space-y-2">
            {exampleQuestions.map((example, index) => (
              <button
                key={index}
                onClick={() => handleExampleClick(example)}
                className="block w-full text-left px-3 py-2 text-sm text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                disabled={isQuerying}
              >
                "{example}"
              </button>
            ))}
          </div>
        </div>

        {/* Tips */}
        <div className="mt-6 bg-gray-50 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-900 mb-2">
            💡 Tips for better results:
          </h4>
          <ul className="text-sm text-gray-600 space-y-1">
            <li>• Be specific and clear in your questions</li>
            <li>• Ask about concepts, facts, or relationships</li>
            <li>• Try different phrasings if you don't get good results</li>
            <li>• Use keywords from your documents</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default QueryInterface;



