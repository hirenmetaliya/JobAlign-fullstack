// // ResultsPage.jsx
// import React, { useState, useEffect } from 'react';
// import { useLocation, useNavigate } from 'react-router-dom';
// import { useAuth } from '../context/AuthContext';

// const ResultsPage = () => {
//   const { user, authToken } = useAuth();
//   const location = useLocation();
//   const navigate = useNavigate();
//   const [matches, setMatches] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);
//   const [maxMatches, setMaxMatches] = useState(10); // Default to free plan

//   useEffect(() => {
//     const fetchMatches = async () => {
//       try {
//         const { parsedData, experience } = location.state;
        
//         console.log('Auth token:', authToken); // Debug log
        
//         const response = await fetch('http://localhost:8000/jobs/api/match-jobs/', {
//           method: 'POST',
//           headers: {
//             'Content-Type': 'application/json',
//             'Authorization': `Bearer ${authToken}`,
//           },
//           body: JSON.stringify({
//             skills: parsedData.skills,
//             experience: experience
//           }),
//           credentials: 'include'
//         });

//         if (!response.ok) {
//           if (response.status === 401) {
//             throw new Error('Please log in to view job matches');
//           }
//           throw new Error('Failed to fetch job matches');
//         }

//         const data = await response.json();
//         setMatches(data.matches);
//         setMaxMatches(data.max_matches);
//         setLoading(false);
//       } catch (err) {
//         setError(err.message);
//         setLoading(false);
//       }
//     };

//     if (!authToken) {
//       setError('Please log in to view job matches');
//       setLoading(false);
//       return;
//     }

//     fetchMatches();
//   }, [location.state, authToken]);

//   if (loading) {
//     return (
//       <div className="min-h-screen bg-gray-50 flex items-center justify-center">
//         <div className="text-center">
//           <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
//           <p className="mt-4 text-gray-600">Finding your perfect job matches...</p>
//         </div>
//       </div>
//     );
//   }

//   if (error) {
//     return (
//       <div className="min-h-screen bg-gray-50 flex items-center justify-center">
//         <div className="text-center">
//           <p className="text-red-600 mb-4">{error}</p>
//           <button 
//             onClick={() => navigate('/upload')}
//             className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition"
//           >
//             Try Again
//           </button>
//         </div>
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-gray-50 py-12">
//       <div className="container mx-auto px-6">
//         <div className="max-w-6xl mx-auto">
//           <h1 className="text-3xl font-bold text-gray-800 mb-6">Your Job Matches</h1>
//           <p className="text-gray-600 mb-8">
//             We found {matches.length} matches based on your skills and experience.
//             {maxMatches !== Infinity && ` Showing ${matches.length} of up to ${maxMatches} matches.`}
//           </p>

//           <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
//             {matches.map((match, index) => (
//               <div key={index} className="bg-white rounded-xl shadow-md p-6">
//                 <div className="flex justify-between items-start mb-4">
//                   <div>
//                     <h2 className="text-xl font-semibold text-gray-800">{match.job_position}</h2>
//                     <p className="text-gray-600">{match.company}</p>
//                   </div>
//                   <div className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm font-medium">
//                     {match.match_percentage}% Match
//                   </div>
//                 </div>
                
//                 <div className="mt-6">
//                   <a 
//                     href={match.apply_url}
//                     target="_blank"
//                     rel="noopener noreferrer"
//                     className="w-full block text-center bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700 transition"
//                   >
//                     Apply Now
//                   </a>
//                 </div>
//               </div>
//             ))}
//           </div>

//           {matches.length === 0 && (
//             <div className="text-center py-12">
//               <p className="text-gray-600 mb-4">No matches found. Try updating your skills or experience.</p>
//               <button 
//                 onClick={() => navigate('/upload')}
//                 className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition"
//               >
//                 Upload New Resume
//               </button>
//             </div>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ResultsPage; 

// ResultsPage.jsx
import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ResultsPage = () => {
  const { user, authToken } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [maxMatches, setMaxMatches] = useState(10); // Default to free plan

  const parsedData = location.state?.parsedData || {};
  const experience = location.state?.experience || "";

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        const response = await fetch('http://localhost:8000/jobs/api/match-jobs/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`,
          },
          body: JSON.stringify({
            skills: parsedData.skills,
            experience: experience
          }),
          credentials: 'include'
        });

        if (!response.ok) {
          if (response.status === 401) {
            throw new Error('Please log in to view job matches');
          }
          throw new Error('Failed to fetch job matches');
        }

        const data = await response.json();
        setMatches(data.matches);
        setMaxMatches(data.max_matches);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    if (!authToken) {
      setError('Please log in to view job matches');
      setLoading(false);
      return;
    }

    fetchMatches();
  }, [parsedData, experience, authToken]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Finding your perfect job matches...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button 
            onClick={() => navigate('/upload')}
            className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // Helper: Parse data from comma-separated string
  const getList = (str) => str?.split(',').map(item => item.trim());

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-6 max-w-6xl">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Your Job Matches</h1>

        {/* ========== Parsed Resume Info Section ========== */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-10">
          <h2 className="text-2xl font-semibold text-blue-700 mb-4">Resume Summary</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            {parsedData.email && (
              <div>
                <h3 className="text-lg font-medium text-gray-700">Email</h3>
                <p className="text-gray-600">{parsedData.email}</p>
              </div>
            )}
            {parsedData.phone && (
              <div>
                <h3 className="text-lg font-medium text-gray-700">Phone</h3>
                <p className="text-gray-600">{parsedData.phone}</p>
              </div>
            )}
            {experience && (
              <div>
                <h3 className="text-lg font-medium text-gray-700">Experience</h3>
                <p className="text-gray-600">{experience}</p>
              </div>
            )}
          </div>

          {parsedData.skills && (
            <div className="mb-4">
              <h3 className="text-lg font-medium text-gray-700">Skills</h3>
              <ul className="list-disc list-inside text-gray-600">
                {getList(parsedData.skills).map((skill, idx) => (
                  <li key={idx}>{skill}</li>
                ))}
              </ul>
            </div>
          )}

          {parsedData.education && (
            <div>
              <h3 className="text-lg font-medium text-gray-700">Education</h3>
              <ul className="list-disc list-inside text-gray-600">
                {getList(parsedData.education).map((degree, idx) => (
                  <li key={idx}>{degree}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* ========== Job Matches Section ========== */}
        <p className="text-gray-600 mb-8">
          We found {matches.length} matches based on your skills and experience.
          {maxMatches !== Infinity && ` Showing ${matches.length} of up to ${maxMatches} matches.`}
        </p>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {matches.map((match, index) => (
            <div key={index} className="bg-white rounded-xl shadow-md p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h2 className="text-xl font-semibold text-gray-800">{match.job_position}</h2>
                  <p className="text-gray-600">{match.company}</p>
                </div>
                <div className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm font-medium">
                  {match.match_percentage}% Match
                </div>
              </div>

              <div className="mt-6">
                <a 
                  href={match.apply_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full block text-center bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700 transition"
                >
                  Apply Now
                </a>
              </div>
            </div>
          ))}
        </div>

        {matches.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-600 mb-4">No matches found. Try updating your skills or experience.</p>
            <button 
              onClick={() => navigate('/upload')}
              className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition"
            >
              Upload New Resume
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsPage;
