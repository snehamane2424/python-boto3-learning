import boto3
import yaml

# =========================
# CONFIGURATION
# =========================
DRY_RUN = True   #  True = Preview only | False = Apply changes

# 🛡️ Protected users (WILL NEVER BE DELETED)
PROTECTED_USERS = ["admin", "root-user", "Sneha M"]

# =========================
# INIT
# =========================
iam = boto3.client('iam')


def log(action, message):
    print(f"{action} | {message}")


def execute(func, *args, **kwargs):
    if DRY_RUN:
        log("DRY-RUN", f"{func.__name__} args={args} kwargs={kwargs}")
    else:
        return func(*args, **kwargs)


# =========================
# LOAD YAML
# =========================
with open('users.yml') as f:
    data = yaml.safe_load(f)

desired_users = {u['name']: u['group'] for u in data['users']}
desired_groups = set(desired_users.values())

# =========================
# EXISTING AWS STATE
# =========================
existing_users = [u['UserName'] for u in iam.list_users()['Users']]
existing_groups = [g['GroupName'] for g in iam.list_groups()['Groups']]

print("\n📊 CURRENT STATE")
print("AWS USERS:", existing_users)
print("YAML USERS:", list(desired_users.keys()))

# =========================
# CREATE / UPDATE
# =========================
for username, group in desired_users.items():

    if username not in existing_users:
        log("CREATE", f"user {username}")
        execute(iam.create_user, UserName=username)

    if group not in existing_groups:
        log("CREATE", f"group {group}")
        execute(iam.create_group, GroupName=group)

    # Fix group membership
    groups = iam.list_groups_for_user(UserName=username)['Groups'] if username in existing_users else []

    for g in groups:
        if g['GroupName'] != group:
            log("UPDATE", f"remove {username} from {g['GroupName']}")
            execute(iam.remove_user_from_group, GroupName=g['GroupName'], UserName=username)

    log("UPDATE", f"ensure {username} in {group}")
    execute(iam.add_user_to_group, GroupName=group, UserName=username)


# =========================
# FIND USERS TO DELETE
# =========================
users_to_delete = [
    user for user in existing_users
    if user not in desired_users and user not in PROTECTED_USERS
]

# =========================
# CONFIRMATION BEFORE DELETE
# =========================
if users_to_delete:
    print("\n USERS MARKED FOR DELETION:", users_to_delete)

    if not DRY_RUN:
        confirm = input("Type 'YES' to confirm deletion: ")

        if confirm != "YES":
            print("Deletion cancelled")
            users_to_delete = []

# =========================
# DELETE USERS (SAFE)
# =========================
for user in users_to_delete:

    log("DELETE", f"user {user}")

    # Remove from groups
    groups = iam.list_groups_for_user(UserName=user)['Groups']
    for g in groups:
        execute(iam.remove_user_from_group, GroupName=g['GroupName'], UserName=user)

    # Delete access keys
    keys = iam.list_access_keys(UserName=user)['AccessKeyMetadata']
    for key in keys:
        execute(iam.delete_access_key, UserName=user, AccessKeyId=key['AccessKeyId'])

    # Delete login profile
    try:
        execute(iam.delete_login_profile, UserName=user)
    except:
        pass

    execute(iam.delete_user, UserName=user)


# =========================
# DELETE UNUSED GROUPS
# =========================
groups_to_delete = [
    group for group in existing_groups
    if group not in desired_groups
]

if groups_to_delete:
    print("\n GROUPS MARKED FOR DELETION:", groups_to_delete)

    if not DRY_RUN:
        confirm = input("Type 'YES' to confirm group deletion: ")

        if confirm != "YES":
            print("Group deletion cancelled")
            groups_to_delete = []

for group in groups_to_delete:

    log("DELETE", f"group {group}")

    users = iam.get_group(GroupName=group)['Users']
    for u in users:
        execute(iam.remove_user_from_group, GroupName=group, UserName=u['UserName'])

    execute(iam.delete_group, GroupName=group)


print("EXISTING USERS:", existing_users)
print("YAML USERS:", list(desired_users.keys()))

# =========================
# FINAL MESSAGE
# =========================
if DRY_RUN:
    print("\n DRY-RUN COMPLETE (No changes made)")
else:
    print("\n CHANGES APPLIED SUCCESSFULLY")
