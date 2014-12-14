from datetime import datetime
import json, sys, math, os, cPickle

WIDTH = 800
MARGIN = 100

def inside(bounds, p):
	if not (bounds[1][0] <= p[0] <= bounds[0][0]):
		return False
	if not (bounds[0][1] <= p[1] <= bounds[1][1]):
		return False
	return True

def delta(ls):
	
	ls.sort()
	half = int(len(ls) / 2.0)
	lower, upper = ls[:half], ls[half:]
	
	res = []
	for side, ps, mark in ((-1, lower, lower[-1]), (1, upper, upper[0])):
		
		if side < 0:
			ps = list(reversed(ps))
		
		scores = []
		for i, p in enumerate(ps):
			
			if p == mark:
				continue
			
			if i < len(ps) / 2:
				continue

			num = i ** 2
			den = abs(mark - p) ** 4
			score = num / den
			scores.append((i, score))
		
		derived = []
		for pair in zip(scores[:-1], scores[1:]):
			diff = pair[1][1] - pair[0][1]
			rel = abs(diff / pair[0][1])
			derived.append((rel, pair[0][0]))
		
		derived.sort(reverse=True)
		#for x in derived[:5]:
		#	print 'D', x
		#	for idx in range(x[1] - 2, x[1] + 3):
		#		if idx < len(ps):
		#			print '  ', ps[idx]
		
		prev = None
		for tip in derived:
			if prev is None or prev[1] > tip[1]:
				prev = tip
			elif prev[1] < tip[1]:
				break
		
		res.append(ps[prev[1]])
	
	return tuple(res)

def transform(bounds, target, p):
	sh = bounds[0][0] - bounds[1][0]
	ph = bounds[0][0] - p[0]
	rh = float(ph) / sh * target[1]
	sw = bounds[1][1] - bounds[0][1]
	pw = p[1] - bounds[0][1]
	rw = float(pw) / sw * target[0]
	return rw, rh

def read(fn):
	
	with open(fn) as f:
		print >> sys.stderr, 'loading JSON data...'
		src = json.load(f)
	
	data = []
	points = src['locations'] if 'locations' in src else src['data']['items']
	for item in points:
		dt = datetime.fromtimestamp(int(item['timestampMs']) / 1000.0)
		if 'latitudeE7' in item:
			vals = item['latitudeE7'], item['longitudeE7']
			data.append((dt, (vals[0] / 10000000.0, vals[1] / 10000000.0)))
		else:
			data.append((dt, (item['latitude'], item['longitude'])))
	
	data.sort()
	with open(fn + '.dat', 'wb') as f:
		print >> sys.stderr, 'writing cache...'
		cPickle.dump(data, f)
	
	return data

def paint(fn):
	
	if os.path.exists(fn + '.dat'):
		orig = os.stat(fn).st_mtime
		cache = os.stat(fn + '.dat').st_mtime
		if cache > orig:
			with open(fn + '.dat') as f:
				print >> sys.stderr, 'loading cached JSON data...'
				data = cPickle.load(f)
		else:
			data = read(fn)
	else:
		data = read(fn)
	
	print >> sys.stderr, '%s data points found' % len(data)
	ddiff = data[-1][0] - data[0][0]
	print >> sys.stderr, '%s days worth of data' % ddiff.days
	latr = delta([p[0] for dt, p in data])
	lonr = delta([p[1] for dt, p in data])
	bounds = (
		(latr[1], lonr[0]),
		(latr[0], lonr[1]),
	)
	
	aspect = (lonr[1] - lonr[0]) / (latr[1] - latr[0])
	print >> sys.stderr, 'aspect', aspect
	target = WIDTH, int(round(WIDTH / aspect))
	print >> sys.stderr, 'target', target
	margins = MARGIN, int(round(MARGIN / aspect))
	print >> sys.stderr, 'margins', margins
	full = target[0] + margins[0] * 2, target[1] + margins[1] * 2
	print ''.join([
		'<?xml version="1.0"?>\n',
		'<svg xmlns="http://www.w3.org/2000/svg" ',
		'width="%s" height="%s">\n' % full,
	])
	
	for dt, p in data:
		if not inside(bounds, p): continue
		coords = transform(bounds, target, p)
		coords = coords[0] + margins[0], coords[1] + margins[1]
		print ''.join([
			'  <circle r="1" cx="%s" cy="%s" ' % coords,
			'style="fill: rgb(0, 57, 163); fill-opacity: 0.3;" />',
		])
	
	print '</svg>'

if __name__ == '__main__':
	paint(sys.argv[1])
