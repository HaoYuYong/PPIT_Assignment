import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from .models import User, JobPosition, AboutMe, Education, WorkExperience, Skills, JobScope, Favourite, Feedback
from django.views.decorators.http import require_http_methods
import sqlite3
from django.db import connection
from django.db import IntegrityError
# from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
import os
from django.core.mail import send_mail
from .serializers import UserSerializer
import random
from django.core.cache import cache
from django.contrib.auth.hashers import make_password

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'email', 'password', 'dob', 'phone', 
                             'address', 'security_question', 'security_answer', 'role']
            if not all(field in data for field in required_fields):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Check if email already exists
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM api_user WHERE email = ?", (data['email'],))
            if cursor.fetchone():
                conn.close()
                return JsonResponse({'error': 'Email already exists'}, status=400)
            conn.close()
            
            # Create user
            try:
                uid = User.create_user(data)
                return JsonResponse({
                    'status': 'success',
                    'uid': uid,
                    'message': 'User registered successfully'
                }, status=201)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def registerStaff(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'email', 'password', 'dob', 'phone', 
                             'address', 'security_question', 'security_answer', 'role']
            if not all(field in data for field in required_fields):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Check if email already exists
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM api_user WHERE email = ?", (data['email'],))
            if cursor.fetchone():
                conn.close()
                return JsonResponse({'error': 'Email already exists'}, status=400)
            conn.close()
            
            # Create user
            try:
                uid = User.create_user(data)
                return JsonResponse({
                    'status': 'success',
                    'uid': uid,
                    'message': 'User registered successfully'
                }, status=201)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            if 'email' not in data or 'password' not in data:
                return JsonResponse({'error': 'Email and password are required'}, status=400)
            
            # Find user by email
            try:
                user = User.objects.get(email=data['email'])
            except User.DoesNotExist:
                return JsonResponse({'error': 'Invalid email or password'}, status=401)
            
            # Check password
            if not check_password(data['password'], user.password):
                return JsonResponse({'error': 'Invalid email or password'}, status=401)
            
            # Create session
            request.session['user_id'] = user.uid
            request.session['user_role'] = user.role
            request.session['authenticated'] = True
            
            # Return user data (excluding sensitive fields)
            return JsonResponse({
                'status': 'success',
                'user': {
                    'uid': user.uid,
                    'name': user.name,
                    'email': user.email,
                    'role': user.role,
                    'phone': user.phone
                }
            }, status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
        

def get_profile(request):
    if request.method == 'GET':
        uid = request.GET.get('uid')
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name, email, dob, phone, address, role FROM api_user WHERE uid = %s", [uid])
                row = cursor.fetchone()
                
                if row:
                    profile_data = {
                        'name': row[0],
                        'email': row[1],
                        'dob': row[2],
                        'phone': row[3],
                        'address': row[4],
                        'role': row[5]
                    }
                    return JsonResponse(profile_data)
                else:
                    return JsonResponse({'error': 'User not found'}, status=404)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@require_http_methods(["PUT"])
def update_profile(request):
    try:
        data = json.loads(request.body)
        uid = data.get('uid')
        
        if not uid:
            return JsonResponse({'error': 'UID is required'}, status=400)
        
        try:
            user = User.objects.get(uid=uid)
            
            # Update fields if they exist in the request
            if 'name' in data:
                user.name = data['name']
            if 'phone' in data:
                user.phone = data['phone']
            if 'dob' in data:
                user.dob = data['dob']
            if 'address' in data:
                user.address = data['address']
            
            user.save()
            
            return JsonResponse({
                'uid': user.uid,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'dob': user.dob,
                'address': user.address,
                'role': user.role
            }, status=200)
            
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_job_positions(request):
    uid = request.GET.get('uid')
    if not uid:
        return JsonResponse({'error': 'UID is required'}, status=400)
    
    try:
        positions = JobPosition.objects.filter(user__uid=uid).values('id', 'position', 'created_at')
        return JsonResponse(list(positions), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_job_position(request):
    try:
        data = json.loads(request.body)
        uid = data.get('user')
        position = data.get('position')
        
        if not uid or not position:
            return JsonResponse(
                {'error': 'User UID and position are required'}, 
                status=400
            )
            
        try:
            user = User.objects.get(uid=uid)
            
            # Check if position already exists for this user
            if JobPosition.objects.filter(user=user, position=position).exists():
                return JsonResponse(
                    {'error': 'This position already exists for the user'},
                    status=400
                )
                
            job_position = JobPosition.objects.create(user=user, position=position)
            
            return JsonResponse({
                'id': job_position.id,
                'position': job_position.position,
                'created_at': job_position.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }, status=201)
            
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except IntegrityError:
            return JsonResponse(
                {'error': 'Database error - position may already exist'},
                status=400
            )
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse(
            {'error': f'Server error: {str(e)}'},
            status=500
        )

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_job_position(request, position_id):
    try:
        position = JobPosition.objects.get(id=position_id)
        position.delete()
        return JsonResponse({'success': True}, status=200)
    except JobPosition.DoesNotExist:
        return JsonResponse({'error': 'Position not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    


@csrf_exempt
@require_http_methods(["GET"])
def get_about_me(request):
    uid = request.GET.get('uid')
    if not uid:
        return JsonResponse({'error': 'UID is required'}, status=400)
    
    try:
        about_me = AboutMe.objects.filter(uid=uid).first()
        if about_me:
            return JsonResponse({
                'aid': about_me.aid,
                'uid': about_me.uid,
                'about': about_me.about,
                'created_at': about_me.created_at,
                'updated_at': about_me.updated_at
            })
        return JsonResponse({'about': ''})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def save_about_me(request):
    try:
        data = json.loads(request.body)
        uid = data.get('uid')
        about = data.get('about', '')
        
        if not uid:
            return JsonResponse({'error': 'UID is required'}, status=400)
        
        # Create or update
        about_me, created = AboutMe.objects.update_or_create(
            uid=uid,
            defaults={'about': about}
        )
        
        return JsonResponse({
            'aid': about_me.aid,
            'uid': about_me.uid,
            'about': about_me.about,
            'created_at': about_me.created_at,
            'updated_at': about_me.updated_at
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["GET", "POST"])
def about_me_handler(request):
    if request.method == 'GET':
        return get_about_me(request)
    elif request.method == 'POST':
        return save_about_me(request)

# Education Views
@csrf_exempt
@require_http_methods(["GET"])
def get_educations(request, uid):
    try:
        educations = Education.objects.filter(user__uid=uid).order_by('-created_at')
        data = [{
            'eid': education.eid,
            'school': education.school,
            'degree': education.degree,
            'field_of_study': education.field_of_study,
            'description': education.description,
            'created_at': education.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': education.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } for education in educations]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def add_education(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['uid', 'school', 'degree', 'field_of_study']
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Check if user exists
        try:
            user = User.objects.get(uid=data['uid'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        # Create education record
        education = Education.objects.create(
            user=user,
            school=data['school'],
            degree=data['degree'],
            field_of_study=data['field_of_study'],
            description=data.get('description', '')
        )
        
        return JsonResponse({
            'eid': education.eid,
            'message': 'Education added successfully',
            'education': {
                'eid': education.eid,
                'school': education.school,
                'degree': education.degree,
                'field_of_study': education.field_of_study,
                'description': education.description,
                'created_at': education.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': education.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_education(request, eid):
    try:
        data = json.loads(request.body)
        
        try:
            education = Education.objects.get(eid=eid)
        except Education.DoesNotExist:
            return JsonResponse({'error': 'Education not found'}, status=404)
        
        # Update fields if they exist in the request
        if 'school' in data:
            education.school = data['school']
        if 'degree' in data:
            education.degree = data['degree']
        if 'field_of_study' in data:
            education.field_of_study = data['field_of_study']
        if 'description' in data:
            education.description = data['description']
        
        education.save()
        
        return JsonResponse({
            'message': 'Education updated successfully',
            'education': {
                'eid': education.eid,
                'school': education.school,
                'degree': education.degree,
                'field_of_study': education.field_of_study,
                'description': education.description,
                'created_at': education.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': education.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_education(request, eid):
    try:
        education = Education.objects.get(eid=eid)
        education.delete()
        return JsonResponse({'message': 'Education deleted successfully'}, status=200)
    except Education.DoesNotExist:
        return JsonResponse({'error': 'Education not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def education_handler(request, uid=None, eid=None):
    if request.method == 'GET' and uid:
        return get_educations(request, uid)
    elif request.method == 'POST':
        return add_education(request)
    elif request.method == 'PUT' and eid:
        return update_education(request, eid)
    elif request.method == 'DELETE' and eid:
        return delete_education(request, eid)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# Work Experience Views
@csrf_exempt
@require_http_methods(["GET"])
def get_work_experiences(request, uid):
    try:
        experiences = WorkExperience.objects.filter(user__uid=uid).order_by('-created_at')
        data = [{
            'wid': experience.wid,
            'title': experience.title,
            'description': experience.description,
            'created_at': experience.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': experience.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } for experience in experiences]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def add_work_experience(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['uid', 'title']
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Check if user exists
        try:
            user = User.objects.get(uid=data['uid'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        # Create work experience record
        experience = WorkExperience.objects.create(
            user=user,
            title=data['title'],
            description=data.get('description', '')
        )
        
        return JsonResponse({
            'wid': experience.wid,
            'message': 'Work experience added successfully',
            'experience': {
                'wid': experience.wid,
                'title': experience.title,
                'description': experience.description,
                'created_at': experience.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': experience.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_work_experience(request, wid):
    try:
        data = json.loads(request.body)
        
        try:
            experience = WorkExperience.objects.get(wid=wid)
        except WorkExperience.DoesNotExist:
            return JsonResponse({'error': 'Work experience not found'}, status=404)
        
        # Update fields if they exist in the request
        if 'title' in data:
            experience.title = data['title']
        if 'description' in data:
            experience.description = data['description']
        
        experience.save()
        
        return JsonResponse({
            'message': 'Work experience updated successfully',
            'experience': {
                'wid': experience.wid,
                'title': experience.title,
                'description': experience.description,
                'created_at': experience.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': experience.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_work_experience(request, wid):
    try:
        experience = WorkExperience.objects.get(wid=wid)
        experience.delete()
        return JsonResponse({'message': 'Work experience deleted successfully'}, status=200)
    except WorkExperience.DoesNotExist:
        return JsonResponse({'error': 'Work experience not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def work_experience_handler(request, uid=None, wid=None):
    if request.method == 'GET' and uid:
        return get_work_experiences(request, uid)
    elif request.method == 'POST':
        return add_work_experience(request)
    elif request.method == 'PUT' and wid:
        return update_work_experience(request, wid)
    elif request.method == 'DELETE' and wid:
        return delete_work_experience(request, wid)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# Skills Views
@csrf_exempt
@require_http_methods(["GET"])
def get_skills(request, uid):
    try:
        skills = Skills.objects.filter(user__uid=uid).order_by('-created_at')
        data = [{
            'sid': skill.sid,
            'skill': skill.skill,
            'created_at': skill.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': skill.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } for skill in skills]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def add_skill(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['uid', 'skill']
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Check if user exists
        try:
            user = User.objects.get(uid=data['uid'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        # Create skill record
        skill = Skills.objects.create(
            user=user,
            skill=data['skill']
        )
        
        return JsonResponse({
            'sid': skill.sid,
            'message': 'Skill added successfully',
            'skill': {
                'sid': skill.sid,
                'skill': skill.skill,
                'created_at': skill.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': skill.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_skill(request, sid):
    try:
        data = json.loads(request.body)
        
        try:
            skill = Skills.objects.get(sid=sid)
        except Skills.DoesNotExist:
            return JsonResponse({'error': 'Skill not found'}, status=404)
        
        # Update fields if they exist in the request
        if 'skill' in data:
            skill.skill = data['skill']
        
        skill.save()
        
        return JsonResponse({
            'message': 'Skill updated successfully',
            'skill': {
                'sid': skill.sid,
                'skill': skill.skill,
                'created_at': skill.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': skill.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_skill(request, sid):
    try:
        skill = Skills.objects.get(sid=sid)
        skill.delete()
        return JsonResponse({'message': 'Skill deleted successfully'}, status=200)
    except Skills.DoesNotExist:
        return JsonResponse({'error': 'Skill not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def skills_handler(request, uid=None, sid=None):
    if request.method == 'GET' and uid:
        return get_skills(request, uid)
    elif request.method == 'POST':
        return add_skill(request)
    elif request.method == 'PUT' and sid:
        return update_skill(request, sid)
    elif request.method == 'DELETE' and sid:
        return delete_skill(request, sid)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
@require_http_methods(["GET"])
def get_job_scope(request):
    uid = request.GET.get('uid')
    if not uid:
        return JsonResponse({'error': 'UID is required'}, status=400)
    
    try:
        job_scope = JobScope.objects.filter(uid=uid).first()
        if job_scope:
            return JsonResponse({
                'jid': job_scope.jid,
                'uid': job_scope.uid,
                'scope': job_scope.scope,
                'created_at': job_scope.created_at,
                'updated_at': job_scope.updated_at
            })
        return JsonResponse({'scope': ''})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def save_job_scope(request):
    try:
        data = json.loads(request.body)
        uid = data.get('uid')
        scope = data.get('scope', '')
        
        if not uid:
            return JsonResponse({'error': 'UID is required'}, status=400)
        
        # Create or update
        job_scope, created = JobScope.objects.update_or_create(
            uid=uid,
            defaults={'scope': scope}
        )
        
        return JsonResponse({
            'jid': job_scope.jid,
            'uid': job_scope.uid,
            'scope': job_scope.scope,
            'created_at': job_scope.created_at,
            'updated_at': job_scope.updated_at
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def job_scope_handler(request):
    if request.method == 'GET':
        return get_job_scope(request)
    elif request.method == 'POST':
        return save_job_scope(request)
    
# To fetch companies with open position and job scopes
@csrf_exempt
@require_http_methods(["GET"])
def get_companies_with_positions_and_scopes(request):
    try:
        companies = User.objects.filter(role='company', is_visible=True)
 
        companies = companies.values('uid', 'name', 'email', 'phone', 'is_visible')
        
        company_data = []
        for company in companies:
            positions = JobPosition.objects.filter(user__uid=company['uid']).values('id', 'position')
            job_scope = JobScope.objects.filter(uid=company['uid']).first()
            about_info = AboutMe.objects.filter(uid=company['uid']).first()
            
            # Preserve newlines by replacing them with HTML line breaks
            scope = job_scope.scope if job_scope else ''
            scope = scope.replace('\n', '<br>') if scope else ''

            # Get about info
            about = about_info.about if about_info else ''
            about = about.replace('\n', '<br>') if about else ''
            
            company_data.append({
                'uid': company['uid'],
                'name': company['name'],
                'email': company['email'],
                'phone': company['phone'],
                'is_visible': company['is_visible'],
                'positions': list(positions),
                'scope': scope,
                'about': about
            })
            
        return JsonResponse(company_data, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
# Favourite
@csrf_exempt
@require_http_methods(["POST"])
def toggle_favourite(request):
    try:
        data = json.loads(request.body)
        user_uid = data.get('user_uid')
        company_uid = data.get('company_uid')
        
        if not user_uid or not company_uid:
            return JsonResponse({'error': 'Both user_uid and company_uid are required'}, status=400)
        
        try:
            user = User.objects.get(uid=user_uid)
            company = User.objects.get(uid=company_uid, role='company')
            
            # Check if favourite exists
            favourite, created = Favourite.objects.get_or_create(
                user=user,
                company=company
            )
            
            if not created:
                favourite.delete()
                return JsonResponse({'status': 'removed', 'message': 'Company removed from favourites'})
            
            return JsonResponse({'status': 'added', 'message': 'Company added to favourites'})
            
        except User.DoesNotExist:
            return JsonResponse({'error': 'User or Company not found'}, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_favourites(request):
    user_uid = request.GET.get('user_uid')
    if not user_uid:
        return JsonResponse({'error': 'user_uid is required'}, status=400)
    
    try:
        favourites = Favourite.objects.filter(user__uid=user_uid, company__is_visible=True).select_related('company')
        
        favourite_companies = []
        for fav in favourites:
            company = fav.company
            positions = JobPosition.objects.filter(user=company).values('id', 'position')
            job_scope = JobScope.objects.filter(uid=company.uid).first()
            about_info = AboutMe.objects.filter(uid=company.uid).first()
            
            scope = job_scope.scope if job_scope else ''
            scope = scope.replace('\n', '<br>') if scope else ''

            about = about_info.about if about_info else ''
            about = about.replace('\n', '<br>') if about else ''
            
            favourite_companies.append({
                'uid': company.uid,
                'name': company.name,
                'email': company.email,
                'phone': company.phone,
                'is_visible': company.is_visible,
                'positions': list(positions),
                'scope': scope,
                'about': about
            })
            
        return JsonResponse(favourite_companies, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["GET"])
def get_employees_with_details(request):
    try:
        # Get visibility filter from query params (default to True if not specified)
        visible_only = request.GET.get('visible_only', 'true').lower() == 'true'
        
        employees = User.objects.filter(role='employee')
        
        # Apply visibility filter if needed
        if visible_only:
            employees = employees.filter(is_visible=True)
        
        # Get basic employee info
        employees = employees.values('uid', 'name', 'email', 'phone', 'is_visible')     


        employee_data = []
        for employee in employees:
            positions = JobPosition.objects.filter(user__uid=employee['uid']).values('id', 'position')
            about_info = AboutMe.objects.filter(uid=employee['uid']).first()
            educations = Education.objects.filter(user__uid=employee['uid']).order_by('-created_at')
            experiences = WorkExperience.objects.filter(user__uid=employee['uid']).order_by('-created_at')
            skills = Skills.objects.filter(user__uid=employee['uid']).order_by('-created_at')
            
            # Get about info
            about = about_info.about if about_info else ''
            about = about.replace('\n', '<br>') if about else ''
            
            employee_data.append({
                'uid': employee['uid'],
                'name': employee['name'],
                'email': employee['email'],
                'phone': employee['phone'],
                'is_visible': employee['is_visible'],
                'positions': list(positions),
                'about': about,
                'educations': list(educations.values()),
                'work_experiences': list(experiences.values()),
                'skills': list(skills.values())
            })
            
        return JsonResponse(employee_data, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["GET"])
def get_employee_favourites(request):
    company_uid = request.GET.get('company_uid')
    if not company_uid:
        return JsonResponse({'error': 'company_uid is required'}, status=400)
    
    try:
        favourites = Favourite.objects.filter(company__uid=company_uid, user__is_visible=True).select_related('user')
        
        favourite_employees = []
        for fav in favourites:
            employee = fav.user
            positions = JobPosition.objects.filter(user=employee).values('id', 'position')
            about_info = AboutMe.objects.filter(uid=employee.uid).first()
            educations = Education.objects.filter(user=employee).order_by('-created_at')
            experiences = WorkExperience.objects.filter(user=employee).order_by('-created_at')
            skills = Skills.objects.filter(user=employee).order_by('-created_at')
            
            about = about_info.about if about_info else ''
            about = about.replace('\n', '<br>') if about else ''
            
            favourite_employees.append({
                'uid': employee.uid,
                'name': employee.name,
                'email': employee.email,
                'phone': employee.phone,
                'is_visible': employee.is_visible,
                'positions': list(positions),
                'about': about,
                'educations': list(educations.values()),
                'work_experiences': list(experiences.values()),
                'skills': list(skills.values())
            })
            
        return JsonResponse(favourite_employees, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def toggle_employee_favourite(request):
    try:
        data = json.loads(request.body)
        company_uid = data.get('company_uid')
        employee_uid = data.get('employee_uid')
        
        if not company_uid or not employee_uid:
            return JsonResponse({'error': 'Both company_uid and employee_uid are required'}, status=400)
        
        try:
            company = User.objects.get(uid=company_uid, role='company')
            employee = User.objects.get(uid=employee_uid, role='employee')
            
            # Check if favourite exists
            favourite, created = Favourite.objects.get_or_create(
                user=employee,
                company=company
            )
            
            if not created:
                favourite.delete()
                return JsonResponse({'status': 'removed', 'message': 'Employee removed from favourites'})
            
            return JsonResponse({'status': 'added', 'message': 'Employee added to favourites'})
            
        except User.DoesNotExist:
            return JsonResponse({'error': 'Company or Employee not found'}, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#AI API
genai.configure(api_key="AIzaSyDFDX44M45otQWVR1eSMigLxwUZSfX90aM")

model = genai.GenerativeModel("gemini-2.0-flash")

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')

            response = model.generate_content(message)
            reply = response.text.strip()

            return JsonResponse({'reply': reply})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST allowed'}, status=405)

@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        #Check if its in our database
        if not email:
            return JsonResponse({'error': 'Email required'}, status=400)
        
        #Generate 6 digit random number
        code = str(random.randint(100000, 999999))
        #save to database for 10minutes
        cache.set(f'reset_code_{email}', code, timeout=600)
        #send email
        send_mail(
            subject='JobConnect Reset Code',
            message=f'Your verification code is: {code}',
            from_email='jobconnectstaff@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def password_reset(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        new_password = data.get('new_password')

        if not email or not new_password:
            return JsonResponse({'error': 'Email and new_password are required'}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)

        user.password = make_password(new_password)
        user.save()

        return JsonResponse({'message': 'Password updated successfully'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
def verify_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        code = data.get('code')

        stored_code = cache.get(f'reset_code_{email}')
        if stored_code and stored_code == code:
            return JsonResponse({'message': 'Code verified'})
        else:
            return JsonResponse({'error': 'Invalid code'}, status=400)

    
@api_view(['PUT'])
def update_visibility(request):
    try:
        uid = request.data.get('uid', None)
        is_visible = request.data.get('is_visible', None)
         
        if not uid or is_visible is None:
            return Response({'error': 'UID and visibility status are required'}, status=400)
             
        user = User.objects.filter(uid=uid).first()
        if not user:
            return Response({'error': 'User not found'}, status=404)
             
        user.is_visible = is_visible
        user.save()
         
        return Response({'success': True, 'is_visible': user.is_visible})
         
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def submit_feedback(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['uid', 'f_title', 'f_description']
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Create feedback
        feedback = Feedback.objects.create(
            uid=data['uid'],
            f_title=data['f_title'],
            f_description=data['f_description'],
            status='new'  # Default status
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Feedback submitted successfully',
            'feedback': {
                'bid': feedback.bid,
                'f_title': feedback.f_title,
                'status': feedback.status,
                'created_at': feedback.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_user_feedback(request):
    uid = request.GET.get('uid')
    if not uid:
        return JsonResponse({'error': 'UID is required'}, status=400)
    
    try:
        feedbacks = Feedback.objects.filter(uid=uid).order_by('-created_at')
        data = [{
            'bid': feedback.bid,
            'f_title': feedback.f_title,
            'f_description': feedback.f_description,
            'status': feedback.status,
            'reply': feedback.reply,
            'staff_id': feedback.staff_id,
            'created_at': feedback.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': feedback.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } for feedback in feedbacks]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
#EmployeeList
class EmployeeListView(APIView):
    def get(self, request):
        employees = User.objects.filter(role='employee')
        serializer = UserSerializer(employees, many=True)
        return Response(serializer.data)
    
class EmployeeDeleteView(APIView):
    def delete(self, request, pk):
        try:
            employee = User.objects.get(pk=pk, role='employee')
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
    
#EmployerList
class EmployerListView(APIView):
    def get(self, request):
        employer = User.objects.filter(role='company')
        serializer = UserSerializer(employer, many=True)
        return Response(serializer.data)
        
class EmployerDeleteView(APIView):
    def delete(self, request, pk):
        try:
            employer = User.objects.get(pk=pk, role='company')
            employer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "Employer not found"}, status=status.HTTP_404_NOT_FOUND)

#StaffList
class StaffListView(APIView):
    def get(self, request):
        staff = User.objects.filter(role='staff')
        serializer = UserSerializer(staff, many=True)
        return Response(serializer.data)
    
class StaffDeleteView(APIView):
    def delete(self, request, pk):
        try:
            staff = User.objects.get(pk=pk, role='staff')
            staff.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "Employer not found"}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@require_http_methods(["GET"])
def get_all_feedback(request):
    try:
        feedbacks = Feedback.objects.all().order_by('-created_at')
        data = [{
            'bid': feedback.bid,
            'uid': feedback.uid,
            'f_title': feedback.f_title,
            'f_description': feedback.f_description,
            'status': feedback.status,
            'reply': feedback.reply,
            'staff_id': feedback.staff_id,
            'created_at': feedback.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': feedback.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } for feedback in feedbacks]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_staff_feedback(request):
    staff_id = request.GET.get('staff_id')
    if not staff_id:
        return JsonResponse({'error': 'staff_id is required'}, status=400)
    
    try:
        feedbacks = Feedback.objects.filter(staff_id=staff_id).order_by('-created_at')
        data = [{
            'bid': feedback.bid,
            'uid': feedback.uid,
            'f_title': feedback.f_title,
            'f_description': feedback.f_description,
            'status': feedback.status,
            'reply': feedback.reply,
            'staff_id': feedback.staff_id,
            'created_at': feedback.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': feedback.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } for feedback in feedbacks]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def assign_feedback(request):
    try:
        data = json.loads(request.body)
        bid = data.get('bid')
        staff_id = data.get('staff_id')
        
        if not bid or not staff_id:
            return JsonResponse({'error': 'Both bid and staff_id are required'}, status=400)
        
        try:
            feedback = Feedback.objects.get(bid=bid)
            feedback.staff_id = staff_id
            feedback.status = 'assigned'
            feedback.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Feedback assigned successfully',
                'feedback': {
                    'bid': feedback.bid,
                    'staff_id': feedback.staff_id,
                    'status': feedback.status
                }
            })
            
        except Feedback.DoesNotExist:
            return JsonResponse({'error': 'Feedback not found'}, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def submit_reply(request):
    try:
        data = json.loads(request.body)
        bid = data.get('bid')
        reply = data.get('reply')
        status = data.get('status', 'resolved')
        
        if not bid or not reply:
            return JsonResponse({'error': 'Both bid and reply are required'}, status=400)
        
        try:
            feedback = Feedback.objects.get(bid=bid)
            feedback.reply = reply
            feedback.status = status
            feedback.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Reply submitted successfully',
                'feedback': {
                    'bid': feedback.bid,
                    'reply': feedback.reply,
                    'status': feedback.status,
                    'updated_at': feedback.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
            
        except Feedback.DoesNotExist:
            return JsonResponse({'error': 'Feedback not found'}, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_staff_list(request):
    try:
        staff_members = User.objects.filter(role='staff').values('uid', 'name')
        return JsonResponse(list(staff_members), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)