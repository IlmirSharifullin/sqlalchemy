global_init("db/mars_explorer.db")
db_sess = create_session()
jobs = db_sess.query(Jobs).all()
jobs_with_max_collabs = []
M = 0
for job in jobs:
    c = len(job.collaborators.split(', '))
    if M < c:
        jobs_with_max_collabs = [job]
        M = c
    elif M == c:
        jobs_with_max_collabs.append(job)
ans_teamleads = []
for job in jobs_with_max_collabs:
    user = db_sess.query(User).filter(User.id == job.team_leader).first()
    if user not in ans_teamleads:
        ans_teamleads.append(user)
        print(user.name, user.surname)