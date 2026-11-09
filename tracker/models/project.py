from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """
    موديل المشروع (Project Workspace)
    المعادل في لارافيل: App\Models\Project
    """
    # $table->string('name', 100);
    name = models.CharField(max_length=100)

    # $table->string('key', 10)->unique(); (مثل: JIRA أو PROJ)
    key = models.CharField(
        max_length=10,
        unique=True,
        help_text="بادئة مفتاح المشروع بالأحرف الكبيرة (مثل: PROJ أو JIRA)"
    )

    # $table->text('description')->nullable();
    description = models.TextField(blank=True, null=True)

    # $table->foreignId('lead_id')->constrained('users');
    lead = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='led_projects',
        help_text="مدير أو منشئ المشروع"
    )

    # عدادات يتم تحديثها تلقائياً (Cached Counters)
    total_issues_count = models.PositiveIntegerField(default=0)
    open_issues_count = models.PositiveIntegerField(default=0)

    # $table->timestamps();
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects'  # اسم الجدول في قاعدة البيانات
        ordering = ['-created_at']  # الترتيب الافتراضي من الأحدث للأقدم
        indexes = [
            models.Index(fields=['key']),  # إنشاء Index على عمود الـ key للبحث السريع
        ]

    def __str__(self):
        # المعادل لدالة __toString() في PHP
        # يحدد كيف يظهر اسم المشروع في لوحة التحكم (Admin) والـ Terminal
        return f"{self.name} ({self.key})"

    def save(self, *args, **kwargs):
        # تحويل المفتاح إلى أحرف كبيرة دائماً قبل الحفظ تلقائياً (مثل: jira -> JIRA)
        self.key = self.key.upper().strip()
        super().save(*args, **kwargs)