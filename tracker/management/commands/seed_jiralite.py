from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import (
    Project, ProjectMember, Role, 
    Issue, IssueType, IssuePriority, IssueStatus, 
    IssueActivityLog
)


class Command(BaseCommand):
    """
    Database Seeder لـ JiraLite
    المعادل في لارافيل: DatabaseSeeder.php -> php artisan db:seed
    يتم تشغيله عبر: python manage.py seed_jiralite
    """
    help = "يقوم بملء قاعدة بيانات MySQL ببيانات تجريبية للمشاريع والتذاكر"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("🌱 جاري ملء قاعدة البيانات (Seeding)..."))

        # 1. إنشاء مستخدمين تجريبيين
        # (المعادل لـ User::firstOrCreate)
        admin_user, _ = User.objects.get_or_create(
            username='admin_boss',
            defaults={'email': 'boss@jiralite.dev', 'is_staff': True}
        )
        admin_user.set_password('admin12345')
        admin_user.save()

        dev_user, _ = User.objects.get_or_create(
            username='dev_alex',
            defaults={'email': 'alex@jiralite.dev'}
        )
        dev_user.set_password('password123')
        dev_user.save()

        qa_user, _ = User.objects.get_or_create(
            username='qa_sara',
            defaults={'email': 'sara@jiralite.dev'}
        )
        qa_user.set_password('password123')
        qa_user.save()

        viewer_user, _ = User.objects.get_or_create(
            username='viewer_omar',
            defaults={'email': 'omar@jiralite.dev'}
        )
        viewer_user.set_password('password123')
        viewer_user.save()

        self.stdout.write(self.style.SUCCESS("✓ تم إنشاء المستخدمين: admin_boss, dev_alex, qa_sara, viewer_omar"))

        # 2. إنشاء مشروع تجريبي
        project, _ = Project.objects.get_or_create(
            key='JIRA',
            defaults={
                'name': 'JiraLite Core Platform',
                'description': 'مشروع تطوير منصة إدارة المهام السريعة بنظام الكانبان.',
                'lead': admin_user,
            }
        )

        # 3. تعيين الأعضاء والرتب (RBAC Pivot)
        ProjectMember.objects.get_or_create(project=project, user=admin_user, defaults={'role': Role.ADMIN})
        ProjectMember.objects.get_or_create(project=project, user=dev_user, defaults={'role': Role.DEVELOPER})
        ProjectMember.objects.get_or_create(project=project, user=qa_user, defaults={'role': Role.DEVELOPER})
        ProjectMember.objects.get_or_create(project=project, user=viewer_user, defaults={'role': Role.VIEWER})

        # 4. إنشاء تذاكر بالحالات الخمسة التي وضعتها أنت
        i1, _ = Issue.objects.get_or_create(
            issue_key='JIRA-1',
            defaults={
                'project': project,
                'title': 'تصميم واجهة لوحة الكانبان بواسطة Tailwind CSS',
                'description': 'بناء الأعمدة الخمسة مع خاصية السحب والإفلات.',
                'issue_type': IssueType.STORY,
                'priority': IssuePriority.HIGH,
                'status': IssueStatus.IN_PROGRESS,
                'reporter': admin_user,
                'assignee': dev_user,
            }
        )

        i2, _ = Issue.objects.get_or_create(
            issue_key='JIRA-2',
            defaults={
                'project': project,
                'title': 'بناء Middleware لحساب زمن الاستجابة وعدد الاستعلامات',
                'description': 'إضافة Header لحساب Response Time بالمللي ثانية.',
                'issue_type': IssueType.TASK,
                'priority': IssuePriority.MEDIUM,
                'status': IssueStatus.UNDER_REVIEW,
                'reporter': dev_user,
                'assignee': admin_user,
            }
        )

        i3, _ = Issue.objects.get_or_create(
            issue_key='JIRA-3',
            defaults={
                'project': project,
                'title': 'اختبار قيود الصلاحيات: منع Viewer من تعديل التذكرة',
                'description': 'التأكد من أن المستخدم برتبة Viewer لا يمكنه سحب التذكرة.',
                'issue_type': IssueType.BUG,
                'priority': IssuePriority.CRITICAL,
                'status': IssueStatus.READY_FOR_TESTING,
                'reporter': admin_user,
                'assignee': qa_user,
            }
        )

        i4, _ = Issue.objects.get_or_create(
            issue_key='JIRA-4',
            defaults={
                'project': project,
                'title': 'إعداد قاعدة بيانات MySQL مع الـ Migrations',
                'description': 'تم ربط MySQL وتوليد المفاتيح الأجنبية بنجاح.',
                'issue_type': IssueType.TASK,
                'priority': IssuePriority.LOW,
                'status': IssueStatus.DONE,
                'reporter': admin_user,
                'assignee': dev_user,
            }
        )

        i5, _ = Issue.objects.get_or_create(
            issue_key='JIRA-5',
            defaults={
                'project': project,
                'title': 'إضافة نظام الإشعارات الفورية عند تغيير حالة التذكرة',
                'description': 'إرسال إشعار للمطور عند نقل تذكرته إلى Ready for Testing.',
                'issue_type': IssueType.STORY,
                'priority': IssuePriority.MEDIUM,
                'status': IssueStatus.TODO,
                'reporter': admin_user,
                'assignee': None,
            }
        )

        # تحديث عدادات المشروع
        project.total_issues_count = project.issues.count()
        project.open_issues_count = project.issues.exclude(status=IssueStatus.DONE).count()
        project.save()

        # 5. إضافة سجل تغيير تجريبي (Activity Log)
        IssueActivityLog.objects.get_or_create(
            issue=i1,
            action="نقل الحالة إلى قيد التنفيذ",
            defaults={'user': dev_user, 'old_status': 'TODO', 'new_status': 'IN_PROGRESS'}
        )

        self.stdout.write(self.style.SUCCESS("✓ تم إنشاء المشروع و 5 تذاكر بكل الحالات بنجاح!"))
        self.stdout.write(self.style.SUCCESS("🎉 اكتمل الـ Seeding بنجاح تام!"))