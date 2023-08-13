import json

from discord import SyncWebhook
from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest, PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from common.config import *
from common.utils import HTTPResponseHXRedirect
from management.models import Announcement
from mastodon.api import *
from takahe.utils import Takahe

from .account import *
from .data import *
from .forms import ReportForm
from .models import APIdentity, Preference, Report, User


def render_user_not_found(request, user_name=""):
    sec_msg = _("😖哎呀，这位用户好像还没有加入本站，快去联邦宇宙呼唤TA来注册吧！")
    msg = _("未找到用户") + user_name
    return render(
        request,
        "common/error.html",
        {
            "msg": msg,
            "secondary_msg": sec_msg,
        },
    )


def render_user_blocked(request):
    msg = _("没有访问该用户主页的权限")
    return render(
        request,
        "common/error.html",
        {
            "msg": msg,
        },
    )


def query_identity(request, handle):
    try:
        i = APIdentity.get_by_handler(handle)
        return redirect(i.url)
    except APIdentity.DoesNotExist:
        if len(handle.split("@")) == 3:
            Takahe.fetch_remote_identity(handle)
            return render(
                request, "users/fetch_identity_pending.html", {"handle": handle}
            )
        else:
            return render_user_not_found(request, handle)


def fetch_refresh(request):
    handle = request.GET.get("handle", "")
    try:
        i = APIdentity.get_by_handler(handle)
        return HTTPResponseHXRedirect(i.url)
    except:
        retry = int(request.GET.get("retry", 0)) + 1
        if retry > 10:
            return render(request, "users/fetch_identity_failed.html")
        else:
            return render(
                request,
                "users/fetch_identity_refresh.html",
                {"handle": handle, "retry": retry, "delay": retry * 2},
            )


@login_required
def follow(request, user_name):
    if request.method != "POST":
        raise BadRequest()
    user = User.get(user_name)
    if request.user.follow(user):
        return render(request, "users/profile_actions.html", context={"user": user})
    else:
        raise BadRequest()


@login_required
def unfollow(request, user_name):
    if request.method != "POST":
        raise BadRequest()
    user = User.get(user_name)
    if request.user.unfollow(user):
        return render(request, "users/profile_actions.html", context={"user": user})
    else:
        raise BadRequest()


@login_required
def mute(request, user_name):
    if request.method != "POST":
        raise BadRequest()
    user = User.get(user_name)
    if request.user.mute(user):
        return render(request, "users/profile_actions.html", context={"user": user})
    else:
        raise BadRequest()


@login_required
def unmute(request, user_name):
    if request.method != "POST":
        raise BadRequest()
    user = User.get(user_name)
    if request.user.unmute(user):
        return render(request, "users/profile_actions.html", context={"user": user})
    else:
        raise BadRequest()


@login_required
def block(request, user_name):
    if request.method != "POST":
        raise BadRequest()
    user = User.get(user_name)
    if request.user.block(user):
        return render(request, "users/profile_actions.html", context={"user": user})
    else:
        raise BadRequest()


@login_required
def unblock(request, user_name):
    if request.method != "POST":
        raise BadRequest()
    user = User.get(user_name)
    if request.user.unblock(user):
        return render(request, "users/profile_actions.html", context={"user": user})
    else:
        raise BadRequest()


@login_required
def follow_locked(request, user_name):
    user = User.get(user_name)
    return render(request, "users/follow_locked.html", context={"user": user})


@login_required
def set_layout(request):
    if request.method == "POST":
        layout = json.loads(request.POST.get("layout"))
        if request.POST.get("name") == "profile":
            request.user.preference.profile_layout = layout
            request.user.preference.save(update_fields=["profile_layout"])
            return redirect(request.user.url)
        elif request.POST.get("name") == "discover":
            request.user.preference.discover_layout = layout
            request.user.preference.save(update_fields=["discover_layout"])
            return redirect(reverse("catalog:discover"))
    raise BadRequest()


@login_required
def report(request):
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        if user_id:
            user = get_object_or_404(User, pk=user_id)
            form = ReportForm(initial={"reported_user": user})
        else:
            form = ReportForm()
        return render(
            request,
            "users/report.html",
            {
                "form": form,
            },
        )
    elif request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.is_read = False
            form.instance.submit_user = request.user
            form.save()
            dw = settings.DISCORD_WEBHOOKS.get("user-report")
            if dw:
                webhook = SyncWebhook.from_url(dw)  # type: ignore
                webhook.send(
                    f"New report from {request.user} about {form.instance.reported_user} : {form.instance.message}"
                )
            return redirect(reverse("common:home"))
        else:
            return render(
                request,
                "users/report.html",
                {
                    "form": form,
                },
            )
    else:
        raise BadRequest()


@login_required
def manage_report(request):
    if not request.user.is_staff:
        raise PermissionDenied()
    if request.method == "GET":
        reports = Report.objects.all()
        for r in reports.filter(is_read=False):
            r.is_read = True
            r.save()
        return render(
            request,
            "users/manage_report.html",
            {
                "reports": reports,
            },
        )
    else:
        raise BadRequest()


@login_required
def mark_announcements_read(request):
    if request.method == "POST":
        try:
            request.user.read_announcement_index = Announcement.objects.latest("pk").pk
            request.user.save(update_fields=["read_announcement_index"])
        except ObjectDoesNotExist:
            # when there is no annoucenment
            pass
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
