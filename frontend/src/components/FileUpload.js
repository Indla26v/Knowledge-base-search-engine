import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import axios from 'axios';

const FileUpload = ({ onStatsUpdate, onLoading }) => {
  const [uploadResults, setUploadResults] = useState([]);
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    setIsUploading(true);
    onLoading(true);

    const formData = new FormData();
    acceptedFiles.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadResults(response.data.results);
      
      // Update stats after successful upload
      if (onStatsUpdate) {
        try {
          const statsResponse = await axios.get('/stats');
          onStatsUpdate(statsResponse.data);
        } catch (error) {
          console.error('Error fetching stats:', error);
        }
      }
    } catch (error) {
      console.error('Upload error:', error);
      setUploadResults([{
        filename: 'Upload Error',
        status: 'error',
        message: error.response?.data?.detail || 'Upload failed'
      }]);
    } finally {
      setIsUploading(false);
      onLoading(false);
    }
  }, [onStatsUpdate, onLoading]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt']
    },
    multiple: true
  });

  const clearResults = () => {
    setUploadResults([]);
  };

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Upload Documents
          </h2>
          <p className="text-sm text-gray-600 mb-6">
            Upload PDF or TXT files to add them to your knowledge base. 
            Documents will be processed and indexed for search.
          </p>

          <div
            {...getRootProps()}
            className={`upload-area border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${
              isDragActive
                ? 'border-blue-400 bg-blue-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <input {...getInputProps()} />
            <div className="space-y-4">
              {isUploading ? (
                <Loader2 className="h-12 w-12 text-blue-600 mx-auto animate-spin" />
              ) : (
                <Upload className="h-12 w-12 text-gray-400 mx-auto" />
              )}
              <div>
                <p className="text-lg font-medium text-gray-900">
                  {isUploading
                    ? 'Processing files...'
                    : isDragActive
                    ? 'Drop files here'
                    : 'Drag & drop files here, or click to select'}
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  Supports PDF and TXT files
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Upload Results */}
      {uploadResults.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border">
          <div className="p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Upload Results
              </h3>
              <button
                onClick={clearResults}
                className="text-sm text-gray-500 hover:text-gray-700"
              >
                Clear
              </button>
            </div>

            <div className="space-y-3">
              {uploadResults.map((result, index) => (
                <div
                  key={index}
                  className="flex items-start space-x-3 p-3 rounded-lg border"
                >
                  <div className="flex-shrink-0">
                    {result.status === 'success' ? (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    ) : (
                      <AlertCircle className="h-5 w-5 text-red-500" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2">
                      <FileText className="h-4 w-4 text-gray-400" />
                      <p className="text-sm font-medium text-gray-900">
                        {result.filename}
                      </p>
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          result.status === 'success'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {result.status}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mt-1">
                      {result.message}
                    </p>
                    {result.chunks_created && (
                      <p className="text-xs text-gray-500 mt-1">
                        Created {result.chunks_created} chunks
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="bg-blue-50 rounded-lg p-4">
        <h4 className="text-sm font-medium text-blue-900 mb-2">
          How it works:
        </h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Documents are automatically processed and split into chunks</li>
          <li>• Each chunk is converted to embeddings for semantic search</li>
          <li>• Chunks are stored in a vector database for fast retrieval</li>
          <li>• You can then ask questions about your uploaded documents</li>
        </ul>
      </div>
    </div>
  );
};

export default FileUpload;



