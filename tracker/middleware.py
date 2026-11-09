import time
from django.db import connection
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Project, ProjectMember


class RequestTimingMiddleware:
    """
    Middleware 1: قياس أداء السيرفر واستعلامات الداتابيز
    المعادل في لارافيل لـ Global Performance Middleware
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # قبل تشغيل الكنترولر
        start_time = time.perf_counter()
        initial_queries = len(connection.queries)

        response = self.get_response(request)  # $next($request)

        # بعد تشغيل الكنترولر
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        total_queries = len(connection.queries) - initial_queries

        # حقن النتيجة في ترويسة الـ HTTP Response
        response['X-Response-Time-Ms'] = str(duration_ms)
        response['X-DB-Queries'] = str(total_queries)

        return response


class ProjectContextMiddleware:
    """
    Middleware 2: حقن المشروع النشط ورتبة المستخدم تلقائياً
    المعادل في لارافيل لـ Route Model Binding + Context Resolver
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        process_view هي ميزة قوية في جانجو!
        تنفذ بعد تحديد الراوت وقبل تنفيذ دالة الـ View مباشرة،
        وتعطيك الـ parameters القادمة من الـ URL داخل view_kwargs
        """
        # إذا كان الرابط يحتوي على project_key (مثل /projects/JIRA/...)
        project_key = view_kwargs.get('project_key')
        
        if project_key:
            # 1. جلب المشروع تلقائياً
            project = get_object_or_404(Project, key=project_key.upper())
            request.project = project  # الآن أي View تستطيع كتابة: request.project مباشرة!

            # 2. فحص رتبة وصلاحية المستخدم الحالي في هذا المشروع
            if request.user.is_authenticated:
                if request.user.is_superuser or project.lead_id == request.user.id:
                    request.user_role = 'ADMIN'
                else:
                    member = ProjectMember.objects.filter(project=project, user=request.user).first()
                    request.user_role = member.role if member else None
            else:
                request.user_role = None

        return None  # إرجاع None يعني: "الطلب سليم، دع جانجو يكمل طريقه للـ View"

    def __call__(self, request):
        return self.get_response(request)