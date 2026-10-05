import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_commerce_site.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.contrib.auth.models import User

from accounts.models import Profile
from community.models import Project

c = Client(SERVER_NAME="localhost")
failures = []

User.objects.filter(username="tester1").delete()


def check(label, condition):
    print(("PASS " if condition else "FAIL ") + label)
    if not condition:
        failures.append(label)


# 1. Register a new user
r = c.post(
    "/account/register/",
    {
        "username": "tester1",
        "email": "tester1@example.com",
        "password1": "Str0ngPass!234",
        "password2": "Str0ngPass!234",
    },
)
check("register redirects to login", r.status_code == 302 and r.url == "/account/login/")
user = User.objects.get(username="tester1")
check("profile status is pending", user.profile.status == "pending")

# 2. Login blocked while pending
r = c.post("/account/login/", {"username": "tester1", "password": "Str0ngPass!234"})
check("pending login blocked (no redirect)", r.status_code == 200)
check("pending message shown", b"awaiting approval" in r.content)

# 3. Admin approves
user.profile.status = "approved"
user.profile.save()

# 4. Login now works
r = c.post("/account/login/", {"username": "tester1", "password": "Str0ngPass!234"})
check("approved login works", r.status_code == 302)

# 5. Dashboard accessible
r = c.get("/community/dashboard/")
check("dashboard 200", r.status_code == 200)

# 6. Add project with image upload
png = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00"
    b"\x00\x00\x03\x00\x01\x83\xd3\x87B\x00\x00\x00\x00IEND\xaeB`\x82"
)
r = c.post(
    "/community/project/add/",
    {
        "title": "Test project",
        "category": "diy",
        "description": "A project created by the automated test flow.",
        "images": SimpleUploadedFile("proof.png", png, content_type="image/png"),
    },
)
check("project add redirects to dashboard", r.status_code == 302 and r.url == "/community/dashboard/")
project = Project.objects.get(title="Test project")
check("project status pending", project.status == "pending")
check("image attached", project.images.count() == 1)

# 7. Not on showcase while pending
r = c.get("/community/")
check("pending project hidden from showcase", b"Test project" not in r.content)

# 8. Approve project -> visible
project.status = "approved"
project.save()
r = c.get("/community/")
check("approved project on showcase", b"Test project" in r.content)

r = c.get(f"/community/project/{project.pk}/")
check("project detail 200", r.status_code == 200)

# 9. Edit + delete
r = c.post(f"/community/project/{project.pk}/edit/", {"title": "Test project edited", "category": "diy", "description": "updated"})
check("project edit redirects", r.status_code == 302)
project.refresh_from_db()
check("edit resets to pending on text change? (no files)", project.title == "Test project edited")

r = c.post(f"/community/project/{project.pk}/delete/")
check("project delete redirects", r.status_code == 302)
check("project deleted", not Project.objects.filter(pk=project.pk).exists())

# cleanup
user.delete()
print("\n" + ("ALL PASSED" if not failures else f"FAILURES: {failures}"))
sys.exit(0 if not failures else 1)
