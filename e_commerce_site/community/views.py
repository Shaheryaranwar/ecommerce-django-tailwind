from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectForm
from .models import PROJECT_CATEGORIES, Project, ProjectDocument, ProjectImage


def approved_required(view):
    @wraps(view)
    @login_required
    def wrapper(request, *args, **kwargs):
        profile = getattr(request.user, "profile", None)
        if profile is None or profile.status != "approved":
            messages.error(
                request, "Your account is not active yet. Please contact our team."
            )
            return redirect("core:home")
        return view(request, *args, **kwargs)

    return wrapper


def showcase(request):
    projects = (
        Project.objects.filter(status="approved")
        .select_related("user__profile")
        .prefetch_related("images")
    )
    active_category = request.GET.get("category", "")
    valid_categories = {value for value, _ in PROJECT_CATEGORIES}
    if active_category in valid_categories:
        projects = projects.filter(category=active_category)

    paginator = Paginator(projects, 9)
    pagination = paginator.get_page(request.GET.get("page"))
    query_string = request.GET.copy()
    query_string.pop("page", None)

    return render(
        request,
        "community/showcase.html",
        {
            "pagination": pagination,
            "query_string": query_string.urlencode(),
            "categories": PROJECT_CATEGORIES,
            "active_category": active_category,
        },
    )


def project_detail(request, pk):
    project = get_object_or_404(
        Project.objects.filter(status="approved")
        .select_related("user__profile")
        .prefetch_related("images", "documents"),
        pk=pk,
    )
    related = (
        Project.objects.filter(status="approved", category=project.category)
        .exclude(pk=project.pk)
        .prefetch_related("images")[:3]
    )
    return render(
        request,
        "community/project_detail.html",
        {"project": project, "related": related},
    )


def _save_project_files(request, project):
    for file in request.FILES.getlist("images"):
        ProjectImage.objects.create(project=project, image=file)
    document = request.FILES.get("document")
    if document:
        existing = project.documents.first()
        if existing:
            existing.delete()
        ProjectDocument.objects.create(project=project, title=document.name, file=document)


@approved_required
def dashboard(request):
    projects = request.user.projects.prefetch_related("images").order_by("-created_at")
    stats = {
        "total": projects.count(),
        "approved": projects.filter(status="approved").count(),
        "pending": projects.filter(status="pending").count(),
    }
    return render(
        request, "community/dashboard.html", {"projects": projects, "stats": stats}
    )


@approved_required
def project_add(request):
    form = ProjectForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.user = request.user
        project.save()
        _save_project_files(request, project)
        messages.success(
            request,
            "Project submitted for review. It will appear on the community page once approved.",
        )
        return redirect("community:dashboard")
    return render(
        request, "community/project_form.html", {"form": form, "is_edit": False}
    )


@approved_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    form = ProjectForm(request.POST or None, request.FILES or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        _save_project_files(request, project)
        if request.FILES:
            project.status = "pending"
            project.save(update_fields=["status", "updated_at"])
            messages.success(
                request, "Project updated and sent back for review."
            )
        else:
            messages.success(request, "Project updated.")
        return redirect("community:dashboard")
    return render(
        request,
        "community/project_form.html",
        {"form": form, "project": project, "is_edit": True},
    )


@approved_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted.")
    return redirect("community:dashboard")


@approved_required
def image_delete(request, pk):
    image = get_object_or_404(
        ProjectImage.objects.select_related("project"), pk=pk, project__user=request.user
    )
    if request.method == "POST":
        image.delete()
    return redirect("community:project_edit", pk=image.project.pk)
