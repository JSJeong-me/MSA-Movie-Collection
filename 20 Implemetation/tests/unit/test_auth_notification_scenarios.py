from types import SimpleNamespace

from tests.helpers import load_service_module


async def _auth_flow():
    auth_repo_module = load_service_module("auth-service", "app.infrastructure.in_memory_auth_repository")
    auth_cmd_module = load_service_module("auth-service", "app.application.auth_command_service")
    auth_query_module = load_service_module("auth-service", "app.application.auth_query_service")

    repo = auth_repo_module.InMemoryAuthRepository()
    await repo.set_credential("u1", "pw1", role="user")

    cmd_service = auth_cmd_module.AuthCommandService(repo)
    query_service = auth_query_module.AuthQueryService(repo)

    login = await cmd_service.login_user(SimpleNamespace(user_id="u1", password="pw1"))
    verify = await query_service.verify_access_token(SimpleNamespace(access_token=login.get("access_token", "")))
    return login, verify


async def _notification_flow():
    repo_module = load_service_module("notification-service", "app.infrastructure.in_memory_notification_repository")
    dispatch_module = load_service_module("notification-service", "app.infrastructure.in_memory_notification_dispatcher")
    cmd_module = load_service_module("notification-service", "app.application.notification_command_service")
    query_module = load_service_module("notification-service", "app.application.notification_query_service")

    repo = repo_module.InMemoryNotificationRepository()
    dispatch = dispatch_module.InMemoryNotificationDispatcher()
    cmd_service = cmd_module.NotificationCommandService(dispatch, repo)
    query_service = query_module.NotificationQueryService(repo)

    await cmd_service.dispatch_notification(
        SimpleNamespace(notification_id="n1", user_id="u1", message="hello", channel="in-app")
    )
    logs = await query_service.get_my_notifications(SimpleNamespace(user_id="u1"))
    return logs


def test_scenario_login_and_token_verification(anyio_backend):
    import anyio

    login, verify = anyio.run(_auth_flow)
    assert login["success"] is True
    assert verify["valid"] is True
    assert verify["user_id"] == "u1"


def test_scenario_dispatch_notification_and_query_logs(anyio_backend):
    import anyio

    logs = anyio.run(_notification_flow)
    assert len(logs["items"]) == 1
    assert logs["items"][0]["message"] == "hello"
