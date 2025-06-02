// pages/UploadPage.jsx
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ProcessSteps from '../components/ProcessSteps';

const UploadPage = () => {
  const { user } = useAuth();
  const [file, setFile] = useState(null);
  const [experience, setExperience] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const navigate = useNavigate();
  
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };
  
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };
  
  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };
  
  const handleFile = (file) => {
    setFile(file);
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    
    setUploading(true);
    
    try {
      const formData = new FormData();
      formData.append('resume', file);
      formData.append('experience', experience);

      const response = await fetch('http://localhost:8000/resume_parser/api/upload-resume/', {
        method: 'POST',
        body: formData,
        credentials: 'include',
      });

      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        console.error('Non-JSON response:', text);
        throw new Error('Server returned an invalid response. Please try again.');
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Upload failed');
      }

      const data = await response.json();
      setUploading(false);
      
      // Navigate to ResultsPage with the parsed data and experience
      navigate('/results', { state: { parsedData: data.data, experience } });
    } catch (error) {
      setUploading(false);
      console.error('Upload error details:', error);
      window.alert(`Error uploading resume: ${error.message}`);
    }
  };
  
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-6">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">Upload Your Resume</h1>
          <p className="text-gray-600 mb-8 text-center">
            Our AI will analyze your resume and match you with the most relevant job opportunities.
          </p>
          
          <div className="bg-white rounded-xl shadow-md p-6 mb-8">
            <form onSubmit={handleSubmit}>
              <div 
                className={`border-2 border-dashed rounded-lg p-10 text-center mb-6 ${dragActive ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300'}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                {file ? (
                  <div className="text-gray-800">
                    <svg className="w-12 h-12 mx-auto text-indigo-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p className="text-xl font-medium mb-1">{file.name}</p>
                    <p className="text-gray-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                  </div>
                ) : (
                  <div>
                    <svg className="w-12 h-12 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <p className="text-gray-800 mb-2">Drag and drop your resume here</p>
                    <p className="text-gray-500 mb-4">Supported formats: PDF, DOCX, DOC, RTF</p>
                    <label className="bg-indigo-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-700 transition duration-300 cursor-pointer">
                      Browse Files
                      <input type="file" className="hidden" onChange={handleChange} accept=".pdf,.docx,.doc,.rtf" />
                    </label>
                  </div>
                )}
              </div>
              
              {/* Experience Selection */}
              <div className="mb-6">
                <label htmlFor="experience" className="block text-sm font-medium text-gray-700 mb-2">
                  Years of Experience
                </label>
                <select
                  id="experience"
                  value={experience}
                  onChange={(e) => setExperience(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                  required
                >
                  <option value="">Select your experience</option>
                  <option value="0">0 years (Fresher)</option>
                  <option value="1">1 year</option>
                  <option value="2">2 years</option>
                  <option value="3">3 years</option>
                  <option value="4">4 years</option>
                  <option value="5">5 years</option>
                  <option value="6">6 years</option>
                  <option value="7">7 years</option>
                  <option value="8">8 years</option>
                  <option value="9">9 years</option>
                  <option value="10">10+ years</option>
                </select>
              </div>
              
              <div className="flex flex-col sm:flex-row items-center justify-between">
                {file && (
                  <button 
                    type="button" 
                    className="text-gray-600 mb-4 sm:mb-0"
                    onClick={() => setFile(null)}
                  >
                    Remove File
                  </button>
                )}
                <button 
                  type="submit"
                  className={`bg-indigo-600 text-white px-8 py-3 rounded-lg font-semibold text-lg hover:bg-indigo-700 transition duration-300 ${!file || !experience || uploading ? 'opacity-50 cursor-not-allowed' : ''} ${file ? 'sm:ml-auto' : 'w-full'}`}
                  disabled={!file || !experience || uploading}
                >
                  {uploading ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Processing...
                    </span>
                  ) : 'Upload Resume'}
                </button>
              </div>
            </form>
          </div>

          <div className="mt-16">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-800 mb-4">Simple 4-Step Process</h2>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                Get started in minutes and find your perfect job match.
              </p>
            </div>
            <ProcessSteps />
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;