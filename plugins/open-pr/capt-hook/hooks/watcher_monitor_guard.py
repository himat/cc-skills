from __future__ import annotations

from captain_hook import Allow, BaseHookEvent, Block, CustomCondition, Event, Input, Tool, hook
from captain_hook.types import TOOL_EVENTS

WATCHER = "open-pr:pr-watcher"
POLL = "bash /p/open-pr/scripts/pr-poll.sh acme/widgets 7 /tmp/cache/pr/7.json"


class InWatcher(CustomCondition):
    valid_events = TOOL_EVENTS

    def check(self, evt: BaseHookEvent) -> bool:
        return evt.parent_agent_type == WATCHER


hook(
    Event.PreToolUse,
    only_if=[Tool("Monitor"), InWatcher()],
    message=(
        "The watcher runs as an in-process teammate, which no Monitor event wakes. "
        "Run `PR_POLL_WINDOW=40 <poll:>` as foreground Bash with `timeout: 60000` and rerun it on `DONE window-elapsed`."
    ),
    block=True,
    tests={
        Input(tool="Monitor", agent_type=WATCHER, tool_input={"command": POLL}): Block(pattern="PR_POLL_WINDOW=40"),
        Input(tool="Monitor", tool_input={"command": POLL}): Allow(),
        Input(tool="Monitor", agent_type="general-purpose", tool_input={"command": POLL}): Allow(),
    },
)
