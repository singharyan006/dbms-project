import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')


# ── Database Helper ──────────────────────────────────────────
def get_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'BankingSecuritySystem')
    )


# ── Auth Helpers ─────────────────────────────────────────────
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'user':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ═════════════════════════════════════════════════════════════
#  PUBLIC ROUTES
# ═════════════════════════════════════════════════════════════

@app.route('/')
def index():
    if session.get('role') == 'admin':
        return redirect(url_for('admin_overview'))
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'user')

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        if role == 'admin':
            # Admin login: match by name from ADMIN table, password is 'admin123' (demo)
            cursor.execute("SELECT * FROM ADMIN WHERE name = %s", (email,))
            admin = cursor.fetchone()
            if admin and password == 'admin123':
                session['admin_id'] = admin['admin_id']
                session['admin_name'] = admin['name']
                session['admin_role'] = admin['role']
                session['role'] = 'admin'
                cursor.close()
                conn.close()
                return redirect(url_for('admin_overview'))
            else:
                flash("Invalid admin credentials. Use admin name and password 'admin123'.", "error")
        else:
            cursor.execute("SELECT * FROM USER WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
            if user:
                if user['status'] != 'Active':
                    flash(f"Your account is {user['status']}. Contact admin.", "error")
                else:
                    session['user_id'] = user['user_id']
                    session['f_name'] = user['f_name']
                    session['l_name'] = user['l_name']
                    session['email'] = user['email']
                    session['role'] = 'user'

                    # Log session (trigger trg_login will auto-set login_time)
                    cursor.execute(
                        "INSERT INTO SESSION (login_time, user_id) VALUES (NOW(), %s)",
                        (user['user_id'],)
                    )
                    conn.commit()
                    session['session_id'] = cursor.lastrowid

                    cursor.close()
                    conn.close()
                    return redirect(url_for('dashboard'))
            else:
                flash("Invalid email or password.", "error")

        cursor.close()
        conn.close()

    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'session_id' in session and session.get('role') == 'user':
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE SESSION SET logout_time = NOW() WHERE session_id = %s",
                (session['session_id'],)
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception:
            pass

    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))


# ═════════════════════════════════════════════════════════════
#  USER ROUTES
# ═════════════════════════════════════════════════════════════

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    uid = session['user_id']

    # Stats using SQL functions
    cursor.execute("SELECT total_accounts(%s) AS cnt", (uid,))
    account_count = cursor.fetchone()['cnt']

    # Accounts
    cursor.execute("SELECT * FROM ACCOUNT WHERE user_id = %s", (uid,))
    accounts = cursor.fetchall()

    # Total balance
    cursor.execute("SELECT SUM(balance) AS total FROM ACCOUNT WHERE user_id = %s", (uid,))
    total_balance = cursor.fetchone()['total'] or 0

    # Transactions for user's accounts
    account_ids = [a['account_id'] for a in accounts]
    transactions = []
    total_txn_count = 0
    if account_ids:
        ph = ','.join(['%s'] * len(account_ids))
        cursor.execute(
            f"SELECT * FROM BANK_TRANSACTION WHERE account_id IN ({ph}) ORDER BY transaction_time DESC LIMIT 10",
            tuple(account_ids)
        )
        transactions = cursor.fetchall()

        # Total transaction count using function
        for aid in account_ids:
            cursor.execute("SELECT total_transactions(%s) AS cnt", (aid,))
            total_txn_count += cursor.fetchone()['cnt']

    cursor.close()
    conn.close()

    return render_template('dashboard.html',
                           accounts=accounts,
                           transactions=transactions,
                           account_count=account_count,
                           total_balance=total_balance,
                           total_txn_count=total_txn_count)


@app.route('/deposit', methods=['POST'])
@login_required
def deposit():
    account_id = request.form.get('account_id', type=int)
    amount = request.form.get('amount', type=float)

    if not account_id or not amount:
        flash("Invalid input.", "error")
        return redirect(url_for('dashboard'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Verify account belongs to user
    cursor.execute("SELECT * FROM ACCOUNT WHERE account_id = %s AND user_id = %s",
                   (account_id, session['user_id']))
    account = cursor.fetchone()
    if not account:
        flash("Account not found.", "error")
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))

    try:
        # Insert transaction (trigger trg_check_amount will reject amount <= 0)
        cursor.execute(
            "INSERT INTO BANK_TRANSACTION (amount, transaction_time, account_id) VALUES (%s, NOW(), %s)",
            (amount, account_id)
        )
        # Update balance
        cursor.execute(
            "UPDATE ACCOUNT SET balance = balance + %s WHERE account_id = %s",
            (amount, account_id)
        )
        conn.commit()
        flash(f"Successfully deposited ${amount:,.2f}.", "success")
    except mysql.connector.Error as e:
        conn.rollback()
        flash(f"Deposit failed: {e.msg}", "error")

    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))


@app.route('/withdraw', methods=['POST'])
@login_required
def withdraw():
    account_id = request.form.get('account_id', type=int)
    amount = request.form.get('amount', type=float)

    if not account_id or not amount:
        flash("Invalid input.", "error")
        return redirect(url_for('dashboard'))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Verify account belongs to user
    cursor.execute("SELECT * FROM ACCOUNT WHERE account_id = %s AND user_id = %s",
                   (account_id, session['user_id']))
    account = cursor.fetchone()
    if not account:
        flash("Account not found.", "error")
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))

    if amount > float(account['balance']):
        flash("Insufficient balance.", "error")
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))

    try:
        # Insert transaction (trigger trg_check_amount will reject amount <= 0)
        cursor.execute(
            "INSERT INTO BANK_TRANSACTION (amount, transaction_time, account_id) VALUES (%s, NOW(), %s)",
            (amount, account_id)
        )
        # Update balance (CHECK constraint will reject negative result)
        cursor.execute(
            "UPDATE ACCOUNT SET balance = balance - %s WHERE account_id = %s",
            (amount, account_id)
        )
        conn.commit()
        flash(f"Successfully withdrew ${amount:,.2f}.", "success")
    except mysql.connector.Error as e:
        conn.rollback()
        flash(f"Withdrawal failed: {e.msg}", "error")

    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))


@app.route('/profile')
@login_required
def profile():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    uid = session['user_id']

    # User info
    cursor.execute("SELECT * FROM USER WHERE user_id = %s", (uid,))
    user = cursor.fetchone()

    # Use SQL functions
    cursor.execute("SELECT user_status(%s) AS status", (uid,))
    status = cursor.fetchone()['status']

    cursor.execute("SELECT total_accounts(%s) AS cnt", (uid,))
    account_count = cursor.fetchone()['cnt']

    # Accounts summary via view
    cursor.execute("SELECT * FROM user_accounts WHERE f_name = %s", (user['f_name'],))
    accounts_summary = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('profile.html', user=user, status=status,
                           account_count=account_count, accounts_summary=accounts_summary)


@app.route('/sessions')
@login_required
def user_sessions():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM SESSION WHERE user_id = %s ORDER BY login_time DESC",
        (session['user_id'],)
    )
    sessions_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('sessions.html', sessions_list=sessions_list)


# ═════════════════════════════════════════════════════════════
#  ADMIN ROUTES
# ═════════════════════════════════════════════════════════════

@app.route('/admin')
@admin_required
def admin_overview():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Summary stats
    cursor.execute("SELECT COUNT(*) AS cnt FROM USER")
    total_users = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) AS cnt FROM ACCOUNT")
    total_accounts = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) AS cnt FROM BANK_TRANSACTION")
    total_transactions = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) AS cnt FROM SECURITY_EVENT")
    total_events = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) AS cnt FROM SESSION WHERE logout_time IS NULL")
    active_sessions = cursor.fetchone()['cnt']

    cursor.execute("SELECT SUM(balance) AS total FROM ACCOUNT")
    total_system_balance = cursor.fetchone()['total'] or 0

    # Recent high-risk events (from view)
    cursor.execute("SELECT * FROM high_risk")
    high_risk_events = cursor.fetchall()

    # Recent transactions
    cursor.execute("""
        SELECT T.*, A.user_id, U.f_name, U.l_name
        FROM BANK_TRANSACTION T
        JOIN ACCOUNT A ON T.account_id = A.account_id
        JOIN USER U ON A.user_id = U.user_id
        ORDER BY T.transaction_time DESC LIMIT 5
    """)
    recent_transactions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin.html',
                           total_users=total_users,
                           total_accounts=total_accounts,
                           total_transactions=total_transactions,
                           total_events=total_events,
                           active_sessions=active_sessions,
                           total_system_balance=total_system_balance,
                           high_risk_events=high_risk_events,
                           recent_transactions=recent_transactions)


@app.route('/admin/activity')
@admin_required
def admin_activity():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Build a unified activity feed from multiple tables
    activities = []

    # Transactions
    cursor.execute("""
        SELECT T.transaction_id, T.amount, T.transaction_time AS ts,
               U.f_name, U.l_name, A.account_id, A.account_type
        FROM BANK_TRANSACTION T
        JOIN ACCOUNT A ON T.account_id = A.account_id
        JOIN USER U ON A.user_id = U.user_id
        ORDER BY T.transaction_time DESC LIMIT 50
    """)
    for row in cursor.fetchall():
        activities.append({
            'time': row['ts'],
            'type': 'Transaction',
            'icon': '💰',
            'color': 'green',
            'title': f"Transaction #{row['transaction_id']}",
            'detail': f"{row['f_name']} {row['l_name']} — ${row['amount']:,.2f} on {row['account_type']} account #{row['account_id']}"
        })

    # Sessions (logins)
    cursor.execute("""
        SELECT S.session_id, S.login_time AS ts, S.logout_time,
               U.f_name, U.l_name, U.user_id
        FROM SESSION S
        JOIN USER U ON S.user_id = U.user_id
        ORDER BY S.login_time DESC LIMIT 50
    """)
    for row in cursor.fetchall():
        activities.append({
            'time': row['ts'],
            'type': 'Login',
            'icon': '🔐',
            'color': 'blue',
            'title': f"Session #{row['session_id']}",
            'detail': f"{row['f_name']} {row['l_name']} logged in" + (
                f" — logged out at {row['logout_time'].strftime('%H:%M')}" if row['logout_time'] else " — still active"
            )
        })

    # Security events
    cursor.execute("""
        SELECT SE.event_id, SE.event_type, SE.description, SE.risk_level,
               SE.session_id, A.name AS admin_name
        FROM SECURITY_EVENT SE
        JOIN ADMIN A ON SE.admin_id = A.admin_id
        JOIN SESSION S ON SE.session_id = S.session_id
    """)
    for row in cursor.fetchall():
        risk_colors = {'High': 'red', 'Medium': 'yellow', 'Low': 'slate'}
        activities.append({
            'time': datetime.now(),  # events don't have timestamps in schema
            'type': f"Security ({row['risk_level']})",
            'icon': '⚠️',
            'color': risk_colors.get(row['risk_level'], 'slate'),
            'title': row['event_type'],
            'detail': f"{row['description']} — Session #{row['session_id']} — Reviewed by {row['admin_name']}"
        })

    # Sort by time descending
    activities.sort(key=lambda x: x['time'] if x['time'] else datetime.min, reverse=True)

    cursor.close()
    conn.close()

    return render_template('admin_activity.html', activities=activities)


@app.route('/admin/users')
@admin_required
def admin_users():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT U.*,
               (SELECT total_accounts(U.user_id)) AS account_count,
               (SELECT COUNT(*) FROM SESSION S WHERE S.user_id = U.user_id) AS session_count
        FROM USER U ORDER BY U.user_id
    """)
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_users.html', users=users)


@app.route('/admin/toggle-user', methods=['POST'])
@admin_required
def toggle_user():
    user_id = request.form.get('user_id', type=int)
    new_status = request.form.get('new_status', '').strip()

    if user_id and new_status in ('Active', 'Blocked', 'Suspended'):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE USER SET status = %s WHERE user_id = %s", (new_status, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash(f"User #{user_id} status changed to {new_status}.", "success")
    else:
        flash("Invalid request.", "error")

    return redirect(url_for('admin_users'))


@app.route('/admin/sessions')
@admin_required
def admin_sessions():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT S.*, U.f_name, U.l_name, U.email
        FROM SESSION S
        JOIN USER U ON S.user_id = U.user_id
        ORDER BY S.login_time DESC
    """)
    sessions_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_sessions.html', sessions_list=sessions_list)


@app.route('/admin/transactions')
@admin_required
def admin_transactions():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Use the transaction_view + join user info
    cursor.execute("""
        SELECT TV.account_id, TV.amount, TV.transaction_time,
               A.account_type, A.balance, U.f_name, U.l_name
        FROM transaction_view TV
        JOIN ACCOUNT A ON TV.account_id = A.account_id
        JOIN USER U ON A.user_id = U.user_id
        ORDER BY TV.transaction_time DESC
    """)
    transactions = cursor.fetchall()

    # Aggregate stats
    cursor.execute("SELECT SUM(amount) AS total, AVG(amount) AS avg_amt, MAX(amount) AS max_amt FROM BANK_TRANSACTION")
    stats = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('admin_transactions.html', transactions=transactions, stats=stats)


@app.route('/admin/request-logs')
@admin_required
def admin_request_logs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT RL.session_id, RL.request_id, RL.request_time, RL.url_accessed, RL.method,
               D.browser, D.os,
               IP.ip_address, IP.city, IP.country,
               R.referrer_url,
               U.f_name, U.l_name
        FROM REQUEST_LOG RL
        JOIN SESSION S     ON RL.session_id  = S.session_id
        JOIN USER U        ON S.user_id      = U.user_id
        JOIN DEVICE D      ON RL.device_id   = D.device_id
        JOIN IP_ADDRESS IP ON RL.ip_id        = IP.ip_id
        LEFT JOIN REFERRER R ON RL.referrer_id = R.referrer_id
        ORDER BY RL.request_time DESC
    """)
    logs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_requests.html', logs=logs)


@app.route('/admin/events')
@admin_required
def admin_events():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    risk_filter = request.args.get('risk', 'all')

    if risk_filter in ('Low', 'Medium', 'High'):
        cursor.execute("""
            SELECT SE.*, A.name AS admin_name, U.f_name, U.l_name
            FROM SECURITY_EVENT SE
            JOIN ADMIN A ON SE.admin_id = A.admin_id
            JOIN SESSION S ON SE.session_id = S.session_id
            JOIN USER U ON S.user_id = U.user_id
            WHERE SE.risk_level = %s
            ORDER BY SE.event_id DESC
        """, (risk_filter,))
    else:
        cursor.execute("""
            SELECT SE.*, A.name AS admin_name, U.f_name, U.l_name
            FROM SECURITY_EVENT SE
            JOIN ADMIN A ON SE.admin_id = A.admin_id
            JOIN SESSION S ON SE.session_id = S.session_id
            JOIN USER U ON S.user_id = U.user_id
            ORDER BY SE.event_id DESC
        """)

    events = cursor.fetchall()

    # Get admins for the "log new event" form
    cursor.execute("SELECT * FROM ADMIN")
    admins = cursor.fetchall()

    # Get active sessions for the form
    cursor.execute("SELECT session_id FROM SESSION ORDER BY session_id DESC")
    session_ids = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_events.html', events=events, admins=admins,
                           session_ids=session_ids, risk_filter=risk_filter)


@app.route('/admin/log-event', methods=['POST'])
@admin_required
def log_event():
    event_type = request.form.get('event_type', '').strip()
    description = request.form.get('description', '').strip()
    risk_level = request.form.get('risk_level', '').strip()
    session_id = request.form.get('session_id', type=int)
    admin_id = request.form.get('admin_id', type=int)

    if event_type and risk_level and session_id and admin_id:
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO SECURITY_EVENT (event_type, description, risk_level, session_id, admin_id) VALUES (%s, %s, %s, %s, %s)",
                (event_type, description, risk_level, session_id, admin_id)
            )
            conn.commit()
            flash("Security event logged successfully.", "success")
        except mysql.connector.Error as e:
            conn.rollback()
            flash(f"Failed to log event: {e.msg}", "error")
        cursor.close()
        conn.close()
    else:
        flash("All fields are required.", "error")

    return redirect(url_for('admin_events'))


# ═════════════════════════════════════════════════════════════
if __name__ == '__main__':
    app.run(debug=True, port=5000)
