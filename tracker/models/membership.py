from django.db import models
from django.contrib.auth.models import User
from .project import Project


class Role(models.TextChoices):
    """
    المعادل لـ Enum في PHP 8.1+:
    enum Role: string { case ADMIN = 'ADMIN'; case DEVELOPER = 'DEVELOPER'; case VIEWER = 'VIEWER'; }
    """
    ADMIN = 'ADMIN', 'Project Admin'
    DEVELOPER = 'DEVELOPER', 'Developer'
    VIEWER = 'VIEWER', 'Viewer'


class ProjectMember(models.Model):
    """
    جدول الـ Pivot للعضوية والصلاحيات
    المعادل في لارافيل: belongsToMany(User::class, 'project_members')->withPivot('role')
    """
    # $table->foreignId('project_id')->constrained()->cascadeOnDelete();
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='memberships'
    )

    # $table->foreignId('user_id')->constrained()->cascadeOnDelete();
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_memberships'
    )

    # عمود الرتبة باختيارات محددة
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.DEVELOPER
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_members'
        # منع تكرار نفس المستخدم في نفس المشروع (Composite Unique Key)
        # المعادل في لارافيل: $table->unique(['project_id', 'user_id']);
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'user'],
                name='unique_project_member'
            )
        ]

    def __str__(self):
        return f"{self.user.username} in {self.project.key} ({self.role})"

    @property
    def is_admin(self):
        """فحص هل العضو مدير للمشروع"""
        return self.role == Role.ADMIN or self.project.lead_id == self.user_id

    @property
    def can_edit_issues(self):
        """فحص هل يملك صلاحية تعديل التذاكر (Admin أو Developer فقط)"""
        return self.role in [Role.ADMIN, Role.DEVELOPER]