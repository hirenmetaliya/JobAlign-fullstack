// pages/AboutPage.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const AboutPage = () => {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="bg-indigo-600 text-white py-20">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">About JobAlign</h1>
            <p className="text-xl text-indigo-100">
              We're on a mission to help job seekers find their perfect career match through the power of AI.
            </p>
          </div>
        </div>
      </section>
      
      {/* Our Story */}
      <section className="py-20">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold mb-8 text-gray-800">Our Story</h2>
            <div className="prose prose-lg max-w-none text-gray-600">
              <p>
                JobAlign was founded in 2025 by Hiren Metaliya, a visionary full-stack developer who identified a critical gap in the job market. After experiencing the challenges of job hunting firsthand, Hiren recognized that traditional job search methods were inefficient and often led to mismatches between candidates' skills and job requirements.
              </p>
              <p>
                The inspiration for JobAlign came from Hiren's personal journey. As a recent graduate entering the competitive tech industry, he noticed how difficult it was for candidates to find roles that truly matched their skills and aspirations. The existing platforms were either too generic or too focused on specific industries, leaving many talented individuals struggling to find their perfect match.
              </p>
              <p>
                What started as a personal project to solve this problem quickly evolved into JobAlign. Hiren's technical expertise in full-stack development, combined with his understanding of the job market's pain points, enabled him to create a platform that uses advanced AI to bridge the gap between job seekers and employers. Today, JobAlign stands as a testament to how one person's vision and determination can transform an entire industry.
              </p>
            </div>
          </div>
        </div>
      </section>
      
      {/* Our Mission */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold mb-8 text-gray-800">Our Mission</h2>
            <div className="bg-white rounded-xl shadow-md p-8 border-l-4 border-indigo-600">
              <p className="text-xl text-gray-700 italic">
                "To create a job market where skills and potential are perfectly matched with opportunity, eliminating the noise and frustration from the job search process."
              </p>
            </div>
            <div className="mt-12 prose prose-lg max-w-none text-gray-600">
              <p>
                At JobAlign, we believe that finding the right job shouldn't be a matter of luck or connections. It should be a data-driven process that respects the unique skills and potential of each individual.
              </p>
              <p>
                Our mission extends beyond just matching skills to job descriptions. We aim to understand the human behind the resume – their career aspirations, work style preferences, and growth potential. This holistic approach allows us to make matches that lead to fulfilling, long-term career relationships.
              </p>
              <p>
                We're also committed to creating a level playing field where bias is minimized. Our AI algorithms are designed to focus on skills and potential rather than factors that could lead to discrimination in the hiring process.
              </p>
            </div>
          </div>
        </div>
      </section>
      
      {/* Our Team */}
      <section className="py-20">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold mb-12 text-gray-800">Our Team</h2>
            <div className="flex justify-center">
              <div className="text-center max-w-md">
                <img src="/src/assets/hiren.jpg" alt="Hiren Metaliya" className="w-55 h-55 rounded-full mx-auto mb-4 object-cover" />
                <h3 className="text-xl font-semibold text-gray-800">Hiren Metaliya</h3>
                <p className="text-indigo-600 mb-2">CEO & Founder</p>
                <p className="text-gray-600">Full stack developer graduated in 2025, passionate about solving real-world problems through technology.</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AboutPage;