from django.contrib import admin
from .models import Project, ProjectMember, Issue, IssueActivityLog


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'lead', 'total_issues_count', 'open_issues_count', 'created_at')
    search_fields = ('name', 'key', 'lead__username')
    inlines = [ProjectMemberInline]


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('issue_key', 'title', 'project', 'issue_type', 'priority', 'status', 'assignee')
    list_filter = ('project', 'issue_type', 'priority', 'status')
    search_fields = ('issue_key', 'title', 'description', 'assignee__username')


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'role', 'joined_at')
    list_filter = ('role', 'project')
    search_fields = ('user__username', 'project__name')


@admin.register(IssueActivityLog)
class IssueActivityLogAdmin(admin.ModelAdmin):
    list_display = ('issue', 'user', 'action', 'old_status', 'new_status', 'created_at')
    list_filter = ('action', 'created_at')
    readonly_fields = ('issue', 'user', 'action', 'old_status', 'new_status', 'comment', 'created_at')