def has_role(member, roles):
    return any(role.name in roles for role in member.roles)

def get_user_tier(member):
    if has_role(member, SPECIAL_ROLES):
        return 'special'
    elif has_role(member, [PAL_ROLE_NAME]):
        return 'pal'
    return 'regular'
