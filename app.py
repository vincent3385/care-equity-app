import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import streamlit.components.v1 as components

# ----------------------------
# Page + styling
# ----------------------------
st.set_page_config(page_title="Care Equity", page_icon="🧬", layout="wide")

APP_CSS = """
<style>
/* Layout */
.block-container { padding-top: 1.25rem; max-width: 1400px; }
h1, h2, h3 { letter-spacing: -0.02em; }

/* Primary button */
.stButton > button {
  border-radius: 16px !important;
  padding: 0.75rem 1rem !important;
  border: 0 !important;
  font-weight: 700 !important;
}

/* Senior-friendly Help button */
.help-fixed {
  position: sticky;
  top: 0.75rem;
  z-index: 99;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0,0,0,0.06);
  padding: 0.75rem;
  border-radius: 18px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}
.help-title { font-size: 0.95rem; opacity: 0.85; margin-bottom: 0.5rem; }
.big-help button {
  width: 100% !important;
  background: #ff3b5c !important;
  color: white !important;
  font-size: 1.05rem !important;
  padding: 0.9rem 1.0rem !important;
  border-radius: 18px !important;
}
.big-help button:hover { filter: brightness(0.95); transform: scale(1.01); }

.secondary button {
  width: 100% !important;
  background: #2d6cdf !important;
  color: white !important;
  border-radius: 18px !important;
}

/* Card */
.card {
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: 18px;
  padding: 1rem;
  background: white;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}

/* Right column container */
.phone-card {
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: 18px;
  background: white;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  padding: 14px;
  position: sticky;
  top: 1rem;
}

.phone-card-title {
  font-weight: 800;
  margin: 4px 6px 10px 6px;
}

.phone-card-sub {
  margin: -6px 6px 12px 6px;
  opacity: 0.7;
  font-size: 0.9rem;
}
/* Phone mock */
.phone-wrap {
  display: flex;
  justify-content: center;
}
.phone {
  width: 345px;
  height: 720px;
  border-radius: 46px;
  background: #0b1220;
  padding: 14px;
  box-shadow: 0 25px 60px rgba(0,0,0,0.35);
  position: sticky;
  top: 1rem;
}
.screen {
  width: 100%;
  height: 100%;
  border-radius: 36px;
  background: #f8fafc;
  overflow: hidden;
  position: relative;
}
.notch {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  width: 140px;
  height: 26px;
  background: #0b1220;
  border-radius: 18px;
  opacity: 0.92;
}
.screen-inner {
  padding: 54px 16px 18px 16px;
  height: 100%;
  overflow: auto;
}
.phone-title { font-weight: 800; font-size: 1.1rem; margin-bottom: 0.25rem; }
.phone-sub { font-size: 0.9rem; opacity: 0.75; margin-bottom: 0.75rem; }
.avatar-row { display: flex; gap: 10px; margin: 10px 0 12px 0; overflow-x: auto; }
.avatar {
  min-width: 52px;
  height: 52px;
  border-radius: 18px;
  background: white;
  border: 1px solid rgba(0,0,0,0.08);
  display: grid;
  place-items: center;
  font-size: 1.3rem;
}
.task {
  background: white;
  border: 1px solid rgba(0,0,0,0.08);
  border-radius: 16px;
  padding: 10px 10px;
  margin-bottom: 10px;
}
.task-top { display: flex; justify-content: space-between; gap: 10px; }
.task-name { font-weight: 750; }
.badge {
  font-size: 0.78rem;
  padding: 4px 8px;
  border-radius: 999px;
  background: rgba(45,108,223,0.10);
  color: #2d6cdf;
  font-weight: 700;
}
.badge-done { background: rgba(34,197,94,0.12); color: #16a34a; }
.badge-alert { background: rgba(255,59,92,0.12); color: #ff3b5c; }
.task-meta { font-size: 0.85rem; opacity: 0.75; margin-top: 4px; display:flex; justify-content: space-between; }
.bottom-tabs {
  position: sticky;
  bottom: 0;
  background: rgba(248,250,252,0.95);
  border-top: 1px solid rgba(0,0,0,0.07);
  padding: 10px 10px;
  display: flex;
  justify-content: space-between;
  border-bottom-left-radius: 36px;
  border-bottom-right-radius: 36px;
}
.tabicon { font-size: 1.2rem; opacity: 0.85; }
.small { font-size: 0.82rem; opacity: 0.8; }
</style>
"""
st.markdown(APP_CSS, unsafe_allow_html=True)

# ----------------------------
# Data model in session_state (simple + deploy-friendly)
# ----------------------------
def today_iso():
    return date.today().isoformat()

def dt_iso_now():
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"

if "members" not in st.session_state:
    st.session_state.members = [
        {"id": "m1", "name": "Vincent", "icon": "🐱"},
        {"id": "m2", "name": "Sibling", "icon": "🐶"},
        {"id": "m3", "name": "Mom", "icon": "🐼"},
        {"id": "m4", "name": "Dad", "icon": "🦊"},
    ]

if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"id": 1, "title": "Pharmacy pickup", "member_id": "m1", "status": "Done", "mins": 30, "due": today_iso(), "type": "Errand"},
        {"id": 2, "title": "Hospital trip", "member_id": "m2", "status": "To-do", "mins": 120, "due": (date.today()+timedelta(days=1)).isoformat(), "type": "Medical"},
        {"id": 3, "title": "Call insurance", "member_id": None, "status": "To-do", "mins": 40, "due": (date.today()+timedelta(days=2)).isoformat(), "type": "Finance"},
    ]

if "alerts" not in st.session_state:
    st.session_state.alerts = []  # list of dicts: {ts, type, message}

def member_map():
    return {m["id"]: m for m in st.session_state.members}

def tasks_df():
    mm = member_map()
    rows = []
    for t in st.session_state.tasks:
        mid = t.get("member_id")
        rows.append({
            "id": t["id"],
            "task": t["title"],
            "member": mm[mid]["name"] if mid in mm else "Unassigned",
            "status": t["status"],
            "mins": int(t.get("mins") or 0),
            "type": t.get("type") or "General",
            "due": t.get("due") or "",
        })
    return pd.DataFrame(rows)

def log_alert(kind: str, msg: str):
    st.session_state.alerts.insert(0, {"ts": dt_iso_now(), "kind": kind, "message": msg})

# ----------------------------
# Header
# ----------------------------
left_header, right_header = st.columns([2.2, 1])

with left_header:
    st.title("🧬 Care Equity Intelligence")
    st.caption("Balancing caregiving responsibilities automatically — with visible fairness, simple scheduling, and senior-friendly help requests.")

with right_header:
    df = tasks_df()
    total_mins = max(df["mins"].sum(), 1)
    vincent_mins = df.loc[df["member"] == "Vincent", "mins"].sum()
    vincent_share = int((vincent_mins / total_mins) * 100)

    # Quick metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Equity Score", "82/100", delta="+4%")
    with m2:
        st.metric("Vincent Load", f"{vincent_share}%", delta="High Load" if vincent_share >= 70 else "OK", delta_color="inverse" if vincent_share >= 70 else "normal")
    with m3:
        st.metric("Open Tasks", int((df["status"] != "Done").sum()))

st.divider()

# ----------------------------
# Main layout: App + Phone mock
# ----------------------------
app_col, phone_col = st.columns([2.0, 1.1])

# Senior-friendly help strip (always visible)
with app_col:
    st.markdown('<div class="help-fixed">', unsafe_allow_html=True)
    st.markdown('<div class="help-title">🆘 Need help right now? (Easy button for seniors)</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1.3, 1])
    with c1:
        st.markdown('<div class="big-help">', unsafe_allow_html=True)
        if st.button("🚨 REQUEST EMERGENCY HELP", key="help_emergency"):
            log_alert("Emergency", "Emergency help requested — notify family now.")
            st.toast("Emergency alert sent to family!", icon="⚠️")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="secondary">', unsafe_allow_html=True)
        if st.button("➕ Request Help Task", key="help_task"):
            st.session_state["open_help_modal"] = True
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("open_help_modal"):
        with st.expander("Request a Help Task (fills the dashboard)", expanded=True):
            title = st.selectbox("What do you need?", ["Groceries", "Pharmacy pickup", "Ride to appointment", "Call doctor", "Other"])
            mins = st.number_input("Estimated minutes", min_value=10, max_value=360, value=30, step=5)
            due = st.date_input("Due date", value=date.today())
            if st.button("Post Help Request"):
                new_id = max([t["id"] for t in st.session_state.tasks] + [0]) + 1
                st.session_state.tasks.append({
                    "id": new_id,
                    "title": title,
                    "member_id": None,
                    "status": "To-do",
                    "mins": int(mins),
                    "due": due.isoformat(),
                    "type": "Help Request",
                })
                log_alert("Help Request", f"Help requested: {title} (due {due.isoformat()})")
                st.session_state["open_help_modal"] = False
                st.success("Help request posted!")
                st.rerun()

    # ----------------------------
    # Tabs like a real family app
    # ----------------------------
    tabs = st.tabs(["🏠 Family", "📅 Calendar", "✅ Tasks", "🎁 Rewards", "🔔 Alerts"])

    # --- Family tab ---
    with tabs[0]:
        st.subheader("Family members")
        mm = member_map()

        cols = st.columns(len(st.session_state.members))
        for i, m in enumerate(st.session_state.members):
            with cols[i]:
                st.markdown(f'<div class="card" style="text-align:center;">'
                            f'<div style="font-size:2rem;">{m["icon"]}</div>'
                            f'<div style="font-weight:800;">{m["name"]}</div>'
                            f'<div style="opacity:0.75; font-size:0.9rem;">{m["id"]}</div>'
                            f'</div>', unsafe_allow_html=True)

        st.markdown("### Workload overview")
        df = tasks_df()
        grp = df.groupby("member", as_index=False)["mins"].sum().sort_values("mins", ascending=False)
        st.bar_chart(grp.set_index("member"))

    # --- Calendar tab ---
    with tabs[1]:
        st.subheader("Calendar")
        df = tasks_df().copy()
        df["due"] = pd.to_datetime(df["due"], errors="coerce")
        df = df.sort_values("due")

        view = st.radio("View", ["Agenda", "Week"], horizontal=True)

        if view == "Agenda":
            pick = st.date_input("Show tasks on date", value=date.today())
            day = pd.to_datetime(pick)
            day_df = df[df["due"] == day]
            if day_df.empty:
                st.info("No tasks due that day.")
            else:
                st.dataframe(day_df[["task", "member", "status", "mins", "type"]], hide_index=True, use_container_width=True)

        else:
            start = st.date_input("Week starting", value=date.today() - timedelta(days=date.today().weekday()))
            start_dt = pd.to_datetime(start)
            days = [start_dt + timedelta(days=i) for i in range(7)]
            day_cols = st.columns(7)
            for i, d in enumerate(days):
                with day_cols[i]:
                    st.markdown(f"**{d.strftime('%a')}**<br><span class='small'>{d.strftime('%b %d')}</span>", unsafe_allow_html=True)
                    ddf = df[df["due"] == d]
                    if ddf.empty:
                        st.caption("—")
                    else:
                        for _, r in ddf.iterrows():
                            st.markdown(f"- {r['task']} ({r['member']})")

    # --- Tasks tab ---
    with tabs[2]:
        st.subheader("Tasks")
        df = tasks_df()

        f1, f2, f3 = st.columns([1.2, 1, 1])
        with f1:
            who = st.selectbox("Filter by member", ["All"] + sorted(df["member"].unique().tolist()))
        with f2:
            status = st.selectbox("Status", ["All", "To-do", "Done"])
        with f3:
            sort = st.selectbox("Sort", ["Due date", "Minutes", "Member"])

        fdf = df.copy()
        if who != "All":
            fdf = fdf[fdf["member"] == who]
        if status != "All":
            fdf = fdf[fdf["status"] == status]
        if sort == "Due date":
            fdf = fdf.sort_values("due")
        elif sort == "Minutes":
            fdf = fdf.sort_values("mins", ascending=False)
        else:
            fdf = fdf.sort_values("member")

        st.dataframe(fdf, hide_index=True, use_container_width=True)

        st.markdown("### Add a new task")
        with st.form("add_task"):
            t_title = st.text_input("Task name", placeholder="Cook dinner")
            t_due = st.date_input("Due date", value=date.today())
            t_type = st.selectbox("Type", ["Medical", "Errand", "Home", "Finance", "Emotional", "General"])
            t_mins = st.number_input("Minutes", min_value=10, max_value=600, value=30, step=5)
            member_names = ["Unassigned"] + [m["name"] for m in st.session_state.members]
            t_member = st.selectbox("Assign to", member_names)
            submitted = st.form_submit_button("Create task")

        if submitted:
            if not t_title.strip():
                st.error("Please enter a task name.")
            else:
                mm = member_map()
                name_to_id = {m["name"]: m["id"] for m in st.session_state.members}
                new_id = max([t["id"] for t in st.session_state.tasks] + [0]) + 1
                st.session_state.tasks.append({
                    "id": new_id,
                    "title": t_title.strip(),
                    "member_id": None if t_member == "Unassigned" else name_to_id[t_member],
                    "status": "To-do",
                    "mins": int(t_mins),
                    "due": t_due.isoformat(),
                    "type": t_type,
                })
                st.success("Task created.")
                st.rerun()

        st.markdown("### Mark done / update")
        ids = [t["id"] for t in st.session_state.tasks]
        if not ids:
            st.info("No tasks yet.")
        else:
            pick_id = st.selectbox("Select task", ids)
            task = next(t for t in st.session_state.tasks if t["id"] == pick_id)
            mm = member_map()
            name_to_id = {m["name"]: m["id"] for m in st.session_state.members}
            current_member = mm[task["member_id"]]["name"] if task.get("member_id") in mm else "Unassigned"

            u1, u2, u3 = st.columns(3)
            with u1:
                new_status = st.selectbox("Status", ["To-do", "Done"], index=0 if task["status"] == "To-do" else 1)
            with u2:
                new_member = st.selectbox("Assigned to", ["Unassigned"] + [m["name"] for m in st.session_state.members],
                                          index=(0 if current_member == "Unassigned" else 1 + [m["name"] for m in st.session_state.members].index(current_member)))
            with u3:
                new_mins = st.number_input("Minutes", min_value=10, max_value=600, value=int(task.get("mins") or 30), step=5)

            if st.button("Save changes"):
                task["status"] = new_status
                task["member_id"] = None if new_member == "Unassigned" else name_to_id[new_member]
                task["mins"] = int(new_mins)
                st.success("Updated.")
                st.rerun()

    # --- Rewards tab ---
    with tabs[3]:
        st.subheader("Rewards (simple gamification)")
        df = tasks_df()
        done = df[df["status"] == "Done"].copy()
        if done.empty:
            st.info("Mark some tasks done to earn points.")
        else:
            done["points"] = (done["mins"] / 10).round().astype(int).clip(lower=1)
            pts = done.groupby("member", as_index=False)["points"].sum().sort_values("points", ascending=False)
            st.dataframe(pts, hide_index=True, use_container_width=True)
            st.caption("Points are just a fun proxy (1 point ≈ 10 minutes).")

    # --- Alerts tab ---
    with tabs[4]:
        st.subheader("Alerts & Help Requests")
        if not st.session_state.alerts:
            st.info("No alerts yet.")
        else:
            for a in st.session_state.alerts[:20]:
                badge = "badge"
                if a["kind"].lower().startswith("emergency"):
                    badge = "badge badge-alert"
                elif "help" in a["kind"].lower():
                    badge = "badge"
                st.markdown(
                    f"<div class='card' style='margin-bottom:10px;'>"
                    f"<div style='display:flex; justify-content:space-between; gap:10px;'>"
                    f"<div><span class='{badge}'>{a['kind']}</span></div>"
                    f"<div class='small'>{a['ts']}</div>"
                    f"</div>"
                    f"<div style='margin-top:8px; font-weight:700;'>{a['message']}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

# ----------------------------
# Phone mock (functional mirror)
# ----------------------------
# ----------------------------
# Phone mock (functional mirror)
# ----------------------------
with phone_col:
    dfp = tasks_df().copy()
    dfp["due"] = pd.to_datetime(dfp["due"], errors="coerce")

    # Put To-do first, then Done
    dfp["status_sort"] = dfp["status"].apply(lambda s: 0 if str(s).lower().startswith("to") else 1)
    dfp = dfp.sort_values(["status_sort", "due"], na_position="last")

    PHONE_CSS = """
    <style>
      :root { --card: #ffffff; --border: rgba(0,0,0,0.08); --muted: rgba(0,0,0,0.65); }
      body { margin: 0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto; background: transparent; }
      .card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 14px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.06);
      }
      .card-title { font-weight: 850; margin: 2px 4px 6px 4px; }
      .card-sub { margin: 0 4px 12px 4px; color: var(--muted); font-size: 0.92rem; }

      .phone-wrap { display:flex; justify-content:center; }
      .phone {
        width: 320px; height: 680px;
        border-radius: 44px;
        background: #0b1220;
        padding: 14px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.30);
      }
      .screen {
        width:100%; height:100%;
        border-radius: 34px;
        background:#f8fafc;
        overflow:hidden;
        position:relative;
      }
      .notch {
        position:absolute; top:10px; left:50%; transform:translateX(-50%);
        width:132px; height:24px; background:#0b1220; border-radius:16px; opacity:0.92;
      }
      .screen-inner { padding: 52px 14px 16px 14px; height:100%; overflow:auto; box-sizing:border-box; }
      .phone-title { font-weight:850; font-size:1.05rem; margin-bottom:0.25rem; }
      .phone-sub { font-size:0.9rem; opacity:0.75; margin-bottom:0.65rem; }

      .avatar-row { display:flex; gap:10px; margin:10px 0 12px 0; overflow-x:auto; padding-bottom:2px; }
      .avatar {
        min-width:50px; height:50px; border-radius:16px; background:white;
        border:1px solid rgba(0,0,0,0.08);
        display:grid; place-items:center; font-size:1.25rem;
      }

      .task {
        background:white; border:1px solid rgba(0,0,0,0.08);
        border-radius: 14px;
        padding: 10px;
        margin-bottom: 10px;
      }
      .task-top { display:flex; justify-content:space-between; gap:10px; align-items:flex-start; }
      .task-name { font-weight:800; line-height:1.15; }
      .badge {
        font-size:0.78rem; padding:4px 8px; border-radius:999px;
        background:rgba(45,108,223,0.10); color:#2d6cdf; font-weight:800;
        white-space:nowrap;
      }
      .badge-done { background:rgba(34,197,94,0.12); color:#16a34a; }
      .badge-alert { background:rgba(255,59,92,0.12); color:#ff3b5c; }
      .task-meta {
        font-size:0.84rem; opacity:0.75; margin-top:6px;
        display:flex; justify-content:space-between; gap:10px;
      }

      .bottom-tabs {
        position: sticky; bottom: 0;
        background: rgba(248,250,252,0.96);
        border-top: 1px solid rgba(0,0,0,0.07);
        padding: 10px;
        display:flex; justify-content:space-between;
        border-bottom-left-radius: 34px;
        border-bottom-right-radius: 34px;
      }
      .tab { text-align:center; width:20%; }
      .tabicon { font-size:1.15rem; opacity:0.9; }
      .small { font-size:0.78rem; opacity:0.82; margin-top:2px; }
    </style>
    """

    avatars = "".join(
        [f"<div class='avatar' title='{m['name']}'>{m['icon']}</div>" for m in st.session_state.members]
    )

    phone_tasks = []
    for _, r in dfp.head(8).iterrows():
        badge_cls = "badge" if str(r["status"]).lower() != "done" else "badge badge-done"
        due_txt = r["due"].strftime("%a %b %d") if pd.notnull(r["due"]) else ""
        phone_tasks.append(
            f"""
            <div class="task">
              <div class="task-top">
                <div class="task-name">{r['task']}</div>
                <div class="{badge_cls}">{r['status']}</div>
              </div>
              <div class="task-meta">
                <div>{r['member']} • {r['type']}</div>
                <div>{int(r['mins'])} min • {due_txt}</div>
              </div>
            </div>
            """
        )
    phone_tasks_html = "\n".join(phone_tasks)

    help_badge = ""
    if any(str(a["kind"]).lower().startswith("emergency") for a in st.session_state.alerts[:5]):
        help_badge = "<span class='badge badge-alert'>EMERGENCY ACTIVE</span>"

    phone_html = f"""
    {PHONE_CSS}
    <div class="card">
      <div class="card-title">Mobile preview</div>
      <div class="card-sub">What your family sees on a phone</div>

      <div class="phone-wrap">
        <div class="phone">
          <div class="screen">
            <div class="notch"></div>
            <div class="screen-inner">
              <div class="phone-title">Tasks {help_badge}</div>
              <div class="phone-sub">Family dashboard • quick view</div>

              <div class="avatar-row">{avatars}</div>

              {phone_tasks_html}

              <div class="bottom-tabs">
                <div class="tab"><div class="tabicon">🏠</div><div class="small">Family</div></div>
                <div class="tab"><div class="tabicon">📅</div><div class="small">Calendar</div></div>
                <div class="tab"><div class="tabicon">✅</div><div class="small">Tasks</div></div>
                <div class="tab"><div class="tabicon">🎁</div><div class="small">Rewards</div></div>
                <div class="tab"><div class="tabicon">🔔</div><div class="small">Alerts</div></div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
    """

    components.html(phone_html, height=820, scrolling=False)