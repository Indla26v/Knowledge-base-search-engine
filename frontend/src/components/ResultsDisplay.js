import React, { useState } from 'react';
import { FileText, ExternalLink, Copy, CheckCircle } from 'lucide-react';

const ResultsDisplay = ({ result }) => {
  const [copiedText, setCopiedText] = useState('');

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopiedText(text);
      setTimeout(() => setCopiedText(''), 2000);
    });
  };

  if (!result) {
    return (
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="p-6">
          <div className="text-center text-gray-500">
            <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No Results Yet
            </h3>
            <p className="text-sm text-gray-600">
              Ask a question about your documents to see AI-powered answers here.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border">
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Answer
          </h3>
          <button
            onClick={() => copyToClipboard(result.answer)}
            className="flex items-center space-x-1 text-sm text-gray-500 hover:text-gray-700"
          >
            {copiedText === result.answer ? (
              <>
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>Copied!</span>
              </>
            ) : (
              <>
                <Copy className="h-4 w-4" />
                <span>Copy</span>
              </>
            )}
          </button>
        </div>

        {/* Answer */}
        <div className="bg-gray-50 rounded-lg p-4 mb-6">
          <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
            {result.answer}
          </p>
        </div>

        {/* Query Info */}
        <div className="mb-6">
          <div className="flex items-center space-x-4 text-sm text-gray-600">
            <span className="font-medium">Query:</span>
            <span className="italic">"{result.query}"</span>
          </div>
          <div className="flex items-center space-x-4 text-sm text-gray-600 mt-1">
            <span className="font-medium">Sources:</span>
            <span>{result.num_sources} documents</span>
          </div>
        </div>

        {/* Sources */}
        {result.sources && result.sources.length > 0 && (
          <div>
            <h4 className="text-md font-semibold text-gray-900 mb-3">
              Source Citations
            </h4>
            <div className="space-y-3">
              {result.sources.map((source, index) => (
                <div
                  key={index}
                  className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <FileText className="h-4 w-4 text-gray-400" />
                      <span className="text-sm font-medium text-gray-900">
                        {source.filename}
                      </span>
                      <span className="text-xs text-gray-500">
                        (Chunk {source.chunk_index + 1})
                      </span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                        {Math.round(source.similarity_score * 100)}% match
                      </span>
                      <button
                        onClick={() => copyToClipboard(source.text)}
                        className="text-gray-400 hover:text-gray-600"
                      >
                        {copiedText === source.text ? (
                          <CheckCircle className="h-4 w-4 text-green-500" />
                        ) : (
                          <Copy className="h-4 w-4" />
                        )}
                      </button>
                    </div>
                  </div>
                  <p className="text-sm text-gray-700 leading-relaxed">
                    {source.text}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* No Sources Message */}
        {result.sources && result.sources.length === 0 && (
          <div className="text-center py-4">
            <p className="text-sm text-gray-500">
              No source citations available for this answer.
            </p>
          </div>
        )}

        {/* Footer */}
        <div className="mt-6 pt-4 border-t border-gray-200">
          <p className="text-xs text-gray-500 text-center">
            Answer generated using RAG (Retrieval-Augmented Generation)
          </p>
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;
