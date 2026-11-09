from django.db import models
from django.contrib.auth.models import User
from .project import Project


class IssueType(models.TextChoices):
    BUG = 'BUG', 'Bug'
    TASK = 'TASK', 'Task'
    STORY = 'STORY', 'User Story'


class IssuePriority(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    CRITICAL = 'CRITICAL', 'Critical'


class IssueStatus(models.TextChoices):
    TODO = 'TODO', 'To Do'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
    READY_FOR_TESTING = 'READY_FOR_TESTING', 'Ready for Testing'
    DONE = 'DONE', 'Done'


class Issue(models.Model):
    """
    موديل التذكرة / المهمة (Issue / Task)
    المعادل في لارافيل: App\Models\Issue
    """
    # $table->foreignId('project_id')->constrained()->cascadeOnDelete();
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='issues'
    )

    # مفتاح التذكرة المميز (مثل: JIRA-12)
    issue_key = models.CharField(
        max_length=20,
        unique=True,
        help_text="المعرف الفريد للتذكرة مثل: JIRA-12"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    # الأعمدة ذات الخيارات المحددة (Enums)
    issue_type = models.CharField(
        max_length=20,
        choices=IssueType.choices,
        default=IssueType.TASK
    )
    priority = models.CharField(
        max_length=20,
        choices=IssuePriority.choices,
        default=IssuePriority.MEDIUM
    )
    status = models.CharField(
        max_length=20,
        choices=IssueStatus.choices,
        default=IssueStatus.TODO,
        db_index=True  # Index لأننا سنفلتر كثيراً بالـ status في لوحة الكانبان
    )

    # الشخص الذي أنشأ التذكرة (لا نسمح بحذف حسابه إذا كان له تذاكر PROTECT)
    reporter = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='reported_issues'
    )

    # المطور المسندة إليه المهمة (يمكن أن تكون فارغة NULL)
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_issues'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'issues'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'status']),  # سرعة استعلام الكانبان بورد
            models.Index(fields=['assignee', 'status']),
        ]

    def __str__(self):
        return f"[{self.issue_key}] {self.title}"

    def save(self, *args, **kwargs):
        # توليد مفتاح التذكرة تلقائياً عند الإنشاء لأول مرة (مثل: JIRA-1)
        if not self.issue_key:
            count = Issue.objects.filter(project=self.project).count() + 1
            self.issue_key = f"{self.project.key}-{count}"
        super().save(*args, **kwargs)


class IssueActivityLog(models.Model):
    """
    سجل تتبع الحركات والتغييرات على التذكرة
    المعادل في لارافيل: Spatie Activitylog / Model Observer
    """
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name='activity_logs'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(max_length=80)
    old_status = models.CharField(max_length=20, null=True, blank=True)
    new_status = models.CharField(max_length=20, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'issue_activity_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.issue.issue_key}] {self.action} at {self.created_at}"