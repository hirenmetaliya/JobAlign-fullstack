from django.http import JsonResponse
from .models import JobListing
import json
import os
import re
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import google.generativeai as genai
from .models import SubscriptionPlan, UserSubscription, JobMatch
import logging
import traceback
import random

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)
# Use the correct model name
model = genai.GenerativeModel("gemini-1.5-pro")

def job_listings_api(request):
    listings = JobListing.objects.values('id', 'title', 'company', 'location', 'description', 'required_skills', 'source')
    return JsonResponse(list(listings), safe=False)

class MatchJobsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_max_matches(self, user):
        try:
            subscription = UserSubscription.objects.get(user=user, is_active=True)
            return subscription.plan.max_matches
        except UserSubscription.DoesNotExist:
            return 10  # Default to free plan

    def determine_potential_roles(self, skills):
        """Use Gemini to determine potential roles based on skills."""
        try:
            # Convert skills list to string if it's a list
            skills_text = ', '.join(skills) if isinstance(skills, list) else str(skills)
            
            prompt = f"""
            TASK: Convert these technical skills into job roles.
            SKILLS: {skills_text}

            RULES:
            1. Return ONLY a comma-separated list of job roles
            2. Do not include any other text
            3. Each role should be a standard tech industry job title
            4. Include both specific and general roles
            5. Maximum 5 roles

            EXAMPLE:
            Input: "Python, Django, HTML, CSS, JavaScript"
            Output: "Web Developer,Full Stack Developer,Python Developer,Backend Developer,Frontend Developer"

            YOUR RESPONSE MUST BE ONLY THE COMMA-SEPARATED LIST OF ROLES.
            """
            
            response = model.generate_content(prompt)
            text = response.text.strip()
            logger.info(f"Raw Gemini response for roles: {text}")
            
            # Clean and validate the response
            roles = [role.strip() for role in text.split(',') if role.strip()]
            
            # If no roles found, try a fallback approach
            if not roles:
                logger.warning("No roles found in primary response, trying fallback...")
                # Fallback: Use a simpler prompt
                fallback_prompt = f"""
                List job roles for someone with these skills: {skills_text}
                Format: role1,role2,role3
                """
                fallback_response = model.generate_content(fallback_prompt)
                fallback_text = fallback_response.text.strip()
                logger.info(f"Fallback response: {fallback_text}")
                roles = [role.strip() for role in fallback_text.split(',') if role.strip()]
            
            # If still no roles, use a basic set based on common skills
            if not roles:
                logger.warning("No roles found in fallback, using basic role mapping...")
                basic_roles = self.get_basic_roles(skills)
                roles = basic_roles
            
            logger.info(f"Final roles determined: {roles}")
            return roles
            
        except Exception as e:
            logger.error(f"Error determining potential roles: {str(e)}")
            logger.error(traceback.format_exc())
            # Return basic roles as last resort
            return self.get_basic_roles(skills)

    def get_basic_roles(self, skills):
        """Fallback method to determine basic roles based on common skill patterns."""
        skills_lower = [skill.lower() for skill in skills]
        roles = set()
        
        # Web Development roles
        web_skills = {'html', 'css', 'javascript', 'js', 'react', 'angular', 'vue'}
        if any(skill in web_skills for skill in skills_lower):
            roles.update(['Web Developer', 'Frontend Developer'])
        
        # Backend roles
        backend_skills = {'python', 'django', 'flask', 'node', 'express', 'java', 'spring'}
        if any(skill in backend_skills for skill in skills_lower):
            roles.update(['Backend Developer', 'Python Developer', 'Node.js Developer'])
        
        # Full Stack roles
        if len(roles) >= 2:  # If we have both frontend and backend roles
            roles.add('Full Stack Developer')
        
        # Database roles
        db_skills = {'sql', 'mysql', 'postgresql', 'mongodb', 'database'}
        if any(skill in db_skills for skill in skills_lower):
            roles.add('Database Developer')
        
        return list(roles) if roles else ['Software Developer']  # Default role if nothing else matches

    def get_role_variations(self, role):
        """Get variations and synonyms for a given role."""
        variations = {
            'Web Developer': ['Web Developer', 'Website Developer', 'Web Programmer', 'Web Engineer', 'Web Application Developer'],
            'Frontend Developer': ['Frontend Developer', 'Front-end Developer', 'Front End Developer', 'UI Developer', 'Frontend Engineer', 'UI Engineer', 'JavaScript Developer'],
            'Backend Developer': ['Backend Developer', 'Back-end Developer', 'Back End Developer', 'Backend Engineer', 'Server-side Developer', 'API Developer'],
            'Full Stack Developer': ['Full Stack Developer', 'Full-Stack Developer', 'Full Stack Engineer', 'Full-Stack Engineer', 'Full Stack Web Developer'],
            'Python Developer': ['Python Developer', 'Python Engineer', 'Python Programmer', 'Django Developer', 'Flask Developer', 'Python Backend Developer'],
            'Node.js Developer': ['Node.js Developer', 'Node Developer', 'Node Engineer', 'Node Programmer', 'Express Developer', 'JavaScript Backend Developer']
        }
        return variations.get(role, [role])

    def check_role_match(self, potential_roles, job_position):
        """Check if a job position matches any of the potential roles."""
        try:
            job_position_lower = job_position.lower()
            
            # First try direct matching with variations
            for role in potential_roles:
                for variation in self.get_role_variations(role):
                    if variation.lower() in job_position_lower or job_position_lower in variation.lower():
                        logger.info(f"Direct match found: {job_position} matches {variation}")
                        return 100.0

            # If no direct match, try to use Gemini (but don't fail if it's not available)
            try:
                roles_text = ', '.join(potential_roles)
                prompt = f"""
                Compare these potential roles with a job position and determine if there's a match.
                
                Potential Roles: {roles_text}
                Job Position: {job_position}

                Instructions:
                1. Be lenient in matching - consider related roles and variations
                2. If the job position is in the same domain as any role, consider it a match
                3. Return a number between 0 and 100:
                   - 100 for exact matches
                   - 80-90 for very close matches
                   - 60-70 for related roles
                   - 40-50 for same domain but different focus
                   - 0 for completely unrelated

                Return ONLY the number.
                """
                
                response = model.generate_content(prompt)
                text = response.text.strip()
                logger.info(f"Gemini response for {job_position}: {text}")
                
                number_match = re.search(r'\d+', text)
                if number_match:
                    match_percentage = float(number_match.group())
                    if match_percentage >= 40:
                        return match_percentage
            except Exception as e:
                logger.warning(f"Gemini API error, falling back to basic matching: {str(e)}")
                # Fallback to basic matching if Gemini fails
                if any(role.lower() in job_position_lower for role in potential_roles):
                    return 80.0  # High confidence for partial matches
                return 0

            return 0
        except Exception as e:
            logger.error(f"Error checking role match: {str(e)}")
            logger.error(traceback.format_exc())
            return 0

    def post(self, request):
        try:
            logger.info("Incoming request data: %s", request.data)
            
            # Get data from request
            resume_skills = request.data.get('skills', [])
            if not resume_skills:
                return Response({
                    'error': 'No skills provided',
                    'detail': 'Resume skills are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            experience = request.data.get('experience', 0)
            user = request.user
            
            # Log user info safely
            user_email = getattr(user, 'email', 'Anonymous')
            logger.info(f"Processing request for user: {user_email}")
            logger.info(f"Skills: {resume_skills}")
            logger.info(f"Experience: {experience}")

            # First, determine potential roles based on skills
            potential_roles = self.determine_potential_roles(resume_skills)
            if not potential_roles:
                return Response({
                    'error': 'Could not determine potential roles',
                    'detail': 'Unable to analyze skills'
                }, status=status.HTTP_400_BAD_REQUEST)

            logger.info(f"Determined potential roles: {potential_roles}")

            # Load scraped jobs
            jobs_file = os.path.join(settings.BASE_DIR, 'scraper', 'scraped_jobs.json')
            if not os.path.exists(jobs_file):
                logger.error(f"Jobs file not found at: {jobs_file}")
                return Response({
                    'error': 'Jobs data not found',
                    'detail': 'The jobs database is currently unavailable'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            try:
                with open(jobs_file, 'r', encoding='utf-8') as f:
                    jobs = json.load(f)
                logger.info(f"Successfully loaded {len(jobs)} jobs")
                # Log the first few job positions to verify data
                logger.info("Sample job positions:")
                for job in jobs[:5]:
                    logger.info(f"- {job.get('Job Position', 'No position')}")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in jobs file: {str(e)}")
                return Response({
                    'error': 'Invalid jobs data',
                    'detail': 'Error reading jobs database'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Calculate matches based on potential roles
            matches = []
            for job in jobs:
                try:
                    job_position = job.get('Job Position', '')
                    if not job_position:
                        continue

                    match_percentage = self.check_role_match(potential_roles, job_position)
                    if match_percentage > 0:
                        matches.append({
                            'job_position': job_position,
                            'company': job.get('Company', 'Unknown Company'),
                            'match_percentage': round(match_percentage, 1),
                            'apply_url': job.get('Source URL', '#')
                        })
                except Exception as e:
                    logger.error(f"Error processing job {job.get('Job Position', 'unknown')}: {str(e)}")
                    continue

            if not matches:
                logger.warning("No matches found for roles: %s", potential_roles)
                return Response({
                    'matches': [],
                    'total_matches': 0,
                    'max_matches': self.get_max_matches(user),
                    'message': 'No matching jobs found',
                    'potential_roles': potential_roles,
                    'sample_jobs': [job.get('Job Position', '') for job in jobs[:5]]
                }, status=status.HTTP_200_OK)

            # Sort matches by percentage
            matches.sort(key=lambda x: x['match_percentage'], reverse=True)

            # Limit matches based on subscription
            max_matches = self.get_max_matches(user)
            matches = matches[:max_matches]

            return Response({
                'matches': matches,
                'total_matches': len(matches),
                'max_matches': max_matches,
                'potential_roles': potential_roles
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("Unexpected error: %s", traceback.format_exc())
            return Response({
                'error': 'An unexpected error occurred',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)