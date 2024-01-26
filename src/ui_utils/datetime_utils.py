from datetime import datetime


def estimate_time_delta(time_delta: int, limit: tuple, intervals: tuple):
	est = time_delta // limit[0]
	ret = f'about {est} {intervals[0] + "s" if est > 1 else intervals[0]}' 
	left = est - est * limit[0]
	if left > limit[1] - 1:
		left = left // limit[1]
		ret += f' and {left} {intervals[1] + "s" if left > 1 else intervals[1]} ago'
	else:
		ret += " ago."
	return ret


def estimate_time_delta_from_now(date_str: str):
	d1 = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
	d2 = datetime.now()
	diff = d2 - d1
	if diff.days > 364:
		return estimate_time_delta(diff.days, (365, 30), ("year", "month"))
	elif diff.days > 29:
		return estimate_time_delta(diff.days, (30, 7), ("month", "week"))
	elif diff.days > 6:
		return estimate_time_delta(diff.days, (7, 1), ("week", "day"))
	elif diff.days > 1:
		return f'about {diff.days} days ago.'
	elif diff.seconds > 3599:
		return estimate_time_delta(diff.seconds, (3600, 60), ("hour", "minute"))
	elif diff.seconds > 59:
		minutes = diff.seconds // 60
		return f'about {minutes} {"minutes ago." if minutes > 1 else "minute ago."}'
	else:
		return f'''{"about " + str(diff.seconds) + " seconds ago."
			   if diff.seconds > 10 else "just now."}'''