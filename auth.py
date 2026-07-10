import bcrypt
from database import get_connection


def register(fullname, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    try:

        cursor.execute(
            """
            INSERT INTO users(fullname,email,password)
            VALUES(?,?,?)
            """,
            (fullname, email, hashed_password)
        )

        conn.commit()

        return True

    except Exception:

        return False

    finally:

        conn.close()


def login(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        stored_password = user[0]

        if bcrypt.checkpw(
                password.encode("utf-8"),
                stored_password
        ):
            return True

    return False