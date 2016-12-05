from sugarloaf.models import Trail, Area

def get_or_create(session, model, **kwargs):
    """Get first instance of given model by kwargs or create a new one
    
    from http://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create"""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def get_or_create_trail(session, trail_name, area_name, trail_difficulty):
    trail = Trail.query.filter_by(name=trail_name).first()
    if trail:
        if trail.difficulty != trail_difficulty:
            trail.difficulty = trail_difficulty
            session.add(trail)
            session.commit()
        return trail
    else:
        area = get_or_create(session, Area, name=area_name)
        trail = Trail(name=trail_name, area=area)
        session.add(trail)
        session.commit()
        return trail